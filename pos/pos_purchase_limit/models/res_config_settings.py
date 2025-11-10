from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _name = "res.config.settings"
    _inherit = "res.config.settings"

    customer_purchase_limit = fields.Boolean(string="Customer Purchase Limit", related="pos_config_id.customer_purchase_limit", readonly=False)

    pos_config_id = fields.Many2one(
        'pos.config',
        string="POS Configuration")
