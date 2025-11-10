import logging
import pprint

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class MultiSafepayController(http.Controller):
    _return_url = "/payment/multisafepay/return"
    _webhook_url = "/payment/multisafepay/webhook"

    @http.route(
        _return_url,
        type="http",
        auth="public",
        methods=["GET", "POST"],
        csrf=False,
        save_session=False,
    )
    def multisafepay_return(self, **data):
        _logger.info(
            "handling redirection from MultiSafepay with data:\n%s",
            pprint.pformat(data),
        )
        request.env["payment.transaction"].sudo()._handle_notification_data(
            "multisafepay", data
        )
        return request.redirect("/payment/status")

    @http.route(_webhook_url, type="http", auth="public", methods=["POST"], csrf=False)
    def multisafepay_webhook(self, **data):
        _logger.info(
            "notification received from MultiSafepay with data:\n%s",
            pprint.pformat(data),
        )
        try:
            request.env["payment.transaction"].sudo()._handle_notification_data(
                "multisafepay", data
            )
        except ValidationError:
            _logger.exception(
                "unable to handle the notification data; skipping to acknowledge"
            )
        return "" 
