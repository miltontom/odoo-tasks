from odoo import fields, models


class CommissionRevenue(models.Model):
    _name = "crm.commission.revenue"
    _description = "CRM Commission Revenue Type"

    type = fields.Selection([("straight", "Straight"), ("graduated", "Graduated")])
    percent_rate = fields.Float()
    percent_rate_first = fields.Float()
    percent_rate_second = fields.Float()
    min_amount = fields.Float()
