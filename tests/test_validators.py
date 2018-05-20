from haveibeenpwned.validators import HaveIBeenPwnedValidator
from unittest.mock import patch, Mock

from django.core.exceptions import ValidationError
from django.test import TestCase


class HaveIBeenPwnedValidatorTest(TestCase):

    @patch('hashlib.sha1')
    def test_get_password_hash_uses_sha1(self, mock_sha1):
        HaveIBeenPwnedValidator()._get_hash('test')
        self.assertTrue(mock_sha1.called)

    @patch('haveibeenpwned.validators.HaveIBeenPwnedValidator._get_hash')
    @patch('requests.get')
    def test_validate_not_raise_on_proper_password(self, mock_get, mock_get_hash):
        mock_get_hash.return_value = 'testhash'
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        self.assertIsNone(HaveIBeenPwnedValidator().validate('test'))

    @patch('haveibeenpwned.validators.HaveIBeenPwnedValidator._get_hash')
    @patch('requests.get')
    def test_validate_raise_on_proper_password(self, mock_get, mock_get_hash):
        mock_get_hash.return_value = 'testhash'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        expected_error = "This password has previously appeared in a data breach. Please choose more secure alternative."

        with self.assertRaises(ValidationError) as e:
            HaveIBeenPwnedValidator().validate('test')
        self.assertEqual(e.exception.messages, [expected_error])
        self.assertEqual(e.exception.error_list[0].code, 'password_pwned')

    @patch('haveibeenpwned.validators.HaveIBeenPwnedValidator._get_hash')
    @patch('requests.get')
    def test_validate_api_called_with_proper_params(self, mock_get, mock_get_hash):
        mock_get_hash.return_value = 'testhash'
        mock_response = Mock()
        mock_response.status_code = 400
        HaveIBeenPwnedValidator().validate('test') # should not raise

        self.assertTrue(mock_get.called)
        self.assertIsNone(mock_get.assert_called_with(
            f'{HaveIBeenPwnedValidator.HIBPWNED_API_URL}{mock_get_hash.return_value}',
            headers = HaveIBeenPwnedValidator.HIBPWNED_HEADERS
        ))

    def test_help_text(self):
        self.assertEqual(
            HaveIBeenPwnedValidator().get_help_text(),
            "Your password will be checked against existing data breaches."
        )
