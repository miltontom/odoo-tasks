from odoo import fields, models


class BasicBomComponent(models.Model):
    _name = "basic.bom.component"

    bom_id = fields.Many2one("basic.bom")
    product_id = fields.Many2one("product.product")
    quantity = fields.Integer()
