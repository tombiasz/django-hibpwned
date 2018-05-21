import hashlib
import requests
import urllib.parse

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class HaveIBeenPwnedValidator(object):

    HIBPWNED_API_URL = 'https://api.pwnedpasswords.com/range/'
    HIBPWNED_HEADERS = {
        'User-Agent': 'Django-HIBPwned'
    }

    def get_hash(self, password):
        return  hashlib.sha1(password.encode('UTF-8')).hexdigest().upper()

    def get_api_url(self, document):
        return urllib.parse.urljoin(self.HIBPWNED_API_URL, document)

    def partition_hash(self, hash):
        return hash[:5], hash[5:]

    def api_response_iter(self, content):
        for entry in content.splitlines():
            hash_suffix, *_ = entry.partition(b':')
            yield hash_suffix.decode('UTF-8')

    def validate(self, password, user=None):
        hash = self.get_hash(password)
        prefix, suffix = self.partition_hash(hash)
        url = self.get_api_url(prefix)
        response = requests.get(url, headers=self.HIBPWNED_HEADERS)

        if (response.status_code == requests.codes.ok and
           suffix in self.api_response_iter(response.content)):
            raise ValidationError(
                _("This password has previously appeared in a data breach. Please choose more secure alternative."),
                code='password_pwned',
            )

    def get_help_text(self):
        return _(
            "Your password will be checked against existing data breaches."
        )
