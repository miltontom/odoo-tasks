from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    basic_bom_ids = fields.One2many("basic.bom", "product_id")
