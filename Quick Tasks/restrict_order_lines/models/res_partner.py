from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    restrict_order_lines = fields.Boolean()
    restrict_count = fields.Integer()
