from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    delivery_uom = fields.Many2one(
        "uom.uom", domain="[('category_id', '=', uom_category_id)]"
    )
