import hashlib
import requests

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class HaveIBeenPwnedValidator(object):

    HIBPWNED_API_URL = 'https://api.pwnedpasswords.com/pwnedpassword/'
    HIBPWNED_HEADERS = {
        'User-Agent': 'Django-HIBPwned'
    }

    def _get_hash(self, password):
        return  hashlib.sha1(password.encode('UTF-8')).hexdigest()

    def validate(self, password, user=None):
        password_hash = self._get_hash(password)
        url = f'{self.HIBPWNED_API_URL}{password_hash}'
        response = requests.get(url, headers=self.HIBPWNED_HEADERS)
        if response.status_code == requests.codes.ok:
            raise ValidationError(
                _("This password has previously appeared in a data breach. Please choose more secure alternative."),
                code='password_pwned',
            )

    def get_help_text(self):
        return _(
            "Your password will be checked against existing data breaches."
        )
