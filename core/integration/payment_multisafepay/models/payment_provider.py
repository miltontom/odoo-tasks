import logging
import pprint
import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("multisafepay", "MultiSafepay")],
        ondelete={"multisafepay": "set default"},
    )

    multisafepay_key_secret = fields.Char()

    def _multisafepay_make_request(self, endpoint, payload=None, method='POST'):
        base_url = self._multisafepay_get_api_url()
        url = f"{base_url}{endpoint}?api_key={self.multisafepay_key_secret}"
        headers = {"Content-Type": "application/json", "accept": "application/json"}

        try:
            # response = requests.post(url, headers=headers, json=payload, timeout=10)
            response = requests.request(method, url, headers=headers, json=payload, timeout=10)

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                pl = payload
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(pl)
                )
                msg = response.json()
                raise ValidationError(
                    "MultiSafepay: "
                    + _(
                        "The communication with the API failed.\nDetails: %s (%s)",
                        msg.get("error_info"),
                        msg.get("error_code"),
                    )
                )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "MultiSafepay: " + _("Could not establish the connection to the API.")
            )
        return response.json()

    def _multisafepay_get_api_url(self):
        return "https://testapi.multisafepay.com"
