from odoo import fields, models


class CommissionProduct(models.Model):
    _name = "crm.commission.product"
    _description = "CRM Commission Product Type"

    commission_id = fields.Many2one("crm.commission")
    percent_rate = fields.Float()
    max_amount = fields.Float()
    product_id = fields.Many2one("product.product")
    categ_id = fields.Many2one(related="product_id.categ_id")
