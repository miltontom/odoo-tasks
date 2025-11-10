import logging

from pprint import pprint, pformat

from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_multisafepay.controllers.main import MultiSafepayController
from .. import utils as payment_utils


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != "multisafepay":
            return res

        payload = self._multisafepay_prepare_order_payload()
        _logger.info("sending '/order' request for link creation:\n%s", pformat(payload))
        order_data = self.provider_id._multisafepay_make_request(
            "/v1/json/orders", payload
        )
        self.provider_reference = order_data.get("data").get("order_id")

        return {"payment_url": order_data["data"]["payment_url"]}

    def _multisafepay_prepare_order_payload(self):
        partner_first_name, partner_last_name = payment_utils.split_partner_name(
            self.partner_name
        )
        base_url = self.get_base_url()
        redirect_url = urls.url_join(base_url, MultiSafepayController._return_url)
        webhook_url = urls.url_join(base_url, MultiSafepayController._webhook_url)
        cancel_url = urls.url_join(base_url, "/shop/cart")

        payload = {
            "type": "redirect",
            "order_id": self.reference,
            "gateway": "",
            "currency": self.currency_id.name,
            "amount": self.amount,
            "description": f"{self.company_id.name}: {self.reference}",
            "payment_options": {
                "notification_url": f"{webhook_url}?ref={self.reference}",
                "notification_method": "POST",
                "redirect_url": f"{redirect_url}?ref={self.reference}",
                "cancel_url": cancel_url,
                "close_window": True,
            },
            "customer": {
                "locale": self.partner_lang,
                "ip_address": "123.123.123.123",
                "first_name": partner_first_name,
                "last_name": partner_last_name,
                "company_name": "Test Company Name",
                "address1": self.partner_address,
                "zip_code": self.partner_zip,
                "city": self.partner_city,
                "country": self.partner_country_id.code,
                "phone": self.partner_phone,
                "email": self.partner_email,
            },
        }

        return payload

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != "multisafepay" or len(tx) == 1:
            return tx

        tx = self.search(
            [
                ("reference", "=", notification_data.get("ref")),
                ("provider_code", "=", "multisafepay"),
            ]
        )
        if not tx:
            raise ValidationError(
                "MultiSafepay: "
                + _(
                    "No transaction found matching reference %s.",
                    notification_data.get("ref"),
                )
            )
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != "multisafepay":
            return
        
        payment_data = self.provider_id._multisafepay_make_request(f"/v1/json/orders/{self.provider_reference}", method="GET")
        
        payment_status = payment_data.get('data').get('status')

        if payment_status == 'initialized':
            self._set_pending()
        elif payment_status == 'completed':
            self._set_done()
        elif payment_status in ('void', 'cancelled', 'expired'):
            self._set_canceled("MultiSafepay: " + _("Cancelled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "MultiSafepay: " + _("Received data with invalid payment status: %s", payment_status)
            )
        
