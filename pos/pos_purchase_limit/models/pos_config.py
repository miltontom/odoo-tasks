from odoo import fields, models

class PosConfig(models.Model):
    _inherit = "pos.config"

    customer_purchase_limit = fields.Boolean()