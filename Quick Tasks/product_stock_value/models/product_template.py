from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    stock_value = fields.Float(compute="_compute_stock_value")

    # method 1
    def _compute_stock_value(self):
        self.stock_value = self.standard_price * self.qty_available

    # method 2
    # def _compute_stock_value(self):
    #     res = self.env["stock.valuation.layer"].search(
    #         [("product_id", "=", self.product_variant_id.id)]
    #     )
    #     self.stock_value = sum(res.mapped("value"))
