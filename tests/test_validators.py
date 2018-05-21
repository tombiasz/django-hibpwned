import random
from haveibeenpwned.validators import HaveIBeenPwnedValidator
from unittest.mock import patch, Mock

from django.core.exceptions import ValidationError
from django.test import TestCase


class HaveIBeenPwnedValidatorTest(TestCase):

    def setUp(self):
        self.validator = HaveIBeenPwnedValidator()

    def test_get_password_hash_return_uppercase_string(self):
        hash = self.validator.get_hash('test')
        self.assertTrue(hash.isupper())

    @patch('hashlib.sha1')
    def test_get_password_hash_uses_sha1(self, mock_sha1):
        self.validator.get_hash('test')
        self.assertTrue(mock_sha1.called)

    def test_get_api_url_return_proper_url(self):
        document = 'test'
        expected = f'{self.validator.HIBPWNED_API_URL}{document}'
        actual = self.validator.get_api_url(document)
        self.assertTrue(expected == actual)

    def test_partion_hash_return_properly_splited_value(self):
        expected_prefix, expected_suffix = 'aaaaa', 'bbbbbbbbbbbbbbb'
        hash = f'{expected_prefix}{expected_suffix}'
        actual_prefix, actual_suffix = self.validator.partition_hash(hash)
        self.assertTrue(expected_prefix == actual_prefix)
        self.assertTrue(expected_suffix == actual_suffix)

    def test_api_response_iter_return_properly_parsed_content(self):
        hashes = ['aaaaaaaaaa', 'bbbbbbbbbb', 'cccccccccc']
        content_formatted = '\r\n'.join([f'{h}:1337' for h in hashes])
        response_content = content_formatted.encode()  # must be byte string
        returned = list(self.validator.api_response_iter(response_content))
        self.assertTrue(hashes == returned)

    @patch('haveibeenpwned.validators.HaveIBeenPwnedValidator.get_hash')
    @patch('requests.get')
    def test_validate_not_raise_on_proper_password(self, mock_get, mock_get_hash):
        mock_get_hash.return_value = 'testhash'
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response
        self.assertIsNone(self.validator.validate('test'))

    @patch('haveibeenpwned.validators.HaveIBeenPwnedValidator.get_hash')
    @patch('requests.get')
    def test_validate_raise_on_proper_password(self, mock_get, mock_get_hash):
        mock_get_hash.return_value = 'aaaaabbbbbb'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'bbbbbb:3\r\n'
        mock_get.return_value = mock_response
        expected_error = "This password has previously appeared in a data breach. Please choose more secure alternative."
        with self.assertRaises(ValidationError) as e:
            self.validator.validate('test')
        self.assertEqual(e.exception.messages, [expected_error])
        self.assertEqual(e.exception.error_list[0].code, 'password_pwned')

    @patch('haveibeenpwned.validators.HaveIBeenPwnedValidator.get_hash')
    @patch('requests.get')
    def test_validate_api_called_with_proper_params(self, mock_get, mock_get_hash):
        mock_get_hash.return_value = 'testhash'
        mock_response = Mock()
        mock_response.status_code = 400
        hash_prefix = mock_get_hash.return_value[:5]
        self.validator.validate('test') # should not raise
        self.assertTrue(mock_get.called)
        self.assertIsNone(mock_get.assert_called_with(
            f'{HaveIBeenPwnedValidator.HIBPWNED_API_URL}{hash_prefix}',
            headers = HaveIBeenPwnedValidator.HIBPWNED_HEADERS
        ))

    def test_help_text(self):
        self.assertEqual(
            self.validator.get_help_text(),
            "Your password will be checked against existing data breaches."
        )
