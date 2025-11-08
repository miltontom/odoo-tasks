from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    threshold = fields.Integer(string="Manuf. Threshold")
