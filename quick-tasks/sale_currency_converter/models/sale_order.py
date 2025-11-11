from odoo import api, Command, fields, models
from odoo.fields import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    _currency_id = fields.Many2one(
        "res.currency", readonly=False, domain="[('id', '!=', currency_id)]"
    )
    converted_price = fields.Monetary(
        compute="_compute_converted_price", currency_field="_currency_id"
    )

    @api.depends("_currency_id")
    def _compute_converted_price(self):
        amount = self.amount_total
        self.converted_price = self.env.company.currency_id._convert(
            amount, self._currency_id
        )
