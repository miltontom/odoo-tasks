from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    price = fields.Float()
    tax_ids = fields.Many2many("account.tax")
    tax_inc_price = fields.Float()

    def action_calculate_tax_inc_price(self):
        res = self.tax_ids._get_tax_details(self.price, 1)
        self.write({"tax_inc_price": res.get("total_included")})
