from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    last_sales_date = fields.Datetime()
    is_saleorder_overdue = fields.Boolean(default=False)
