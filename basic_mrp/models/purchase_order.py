from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    basic_mrp_id = fields.Many2one("basic.mrp")
