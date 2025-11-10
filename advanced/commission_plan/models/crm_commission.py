from odoo import fields, models


class Commission(models.Model):
    _name = "crm.commission"
    _description = "CRM Commission"
    _rec_name = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    date_from = fields.Date()
    date_to = fields.Date()
    commission_type = fields.Selection(
        [("product", "Product Wise"), ("revenue", "Revenue Wise")]
    )
    commission_product_ids = fields.One2many("crm.commission.product", "commission_id")
    commission_revenue_id = fields.Many2one("crm.commission.revenue")
    commission_revenue_type = fields.Selection(
        related="commission_revenue_id.type", readonly=False, store=True
    )
    percent_rate = fields.Float(
        related="commission_revenue_id.percent_rate", readonly=False, store=True
    )

    percent_rate_first = fields.Float(
        related="commission_revenue_id.percent_rate_first", readonly=False, store=True
    )

    percent_rate_second = fields.Float(
        related="commission_revenue_id.percent_rate_second", readonly=False, store=True
    )

    min_amount = fields.Float(
        related="commission_revenue_id.min_amount", readonly=False, store=True
    )
