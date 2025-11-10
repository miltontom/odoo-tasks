from odoo import http
from odoo.http import route
from odoo.http import request
import json


class Main(http.Controller):
    @route("/get/company_currency", type="json", auth="user")
    def get_company_currency(self):
        currency = request.env.company.currency_id

        return json.dumps(currency.symbol)
