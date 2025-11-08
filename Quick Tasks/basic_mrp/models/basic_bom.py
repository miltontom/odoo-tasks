from odoo import fields, models


class BasicBom(models.Model):
    _name = "basic.bom"
    _rec_name = "product_id"

    product_id = fields.Many2one("product.product", required=True)
    quantity = fields.Integer()
    component_ids = fields.One2many("basic.bom.component", "bom_id")
