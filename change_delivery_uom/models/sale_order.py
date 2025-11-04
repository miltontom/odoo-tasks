from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    change_delivery_uom = fields.Boolean()
