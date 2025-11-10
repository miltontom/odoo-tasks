from odoo import fields, models, api

class SOOrderLine(models.Model):
    _name = "so.order.line"

    multi_so_inv_id = fields.Many2one("multi.so.inv")
    product_id = fields.Many2one("product.product")
    product_uom_qty = fields.Float("Quantity")
    price_unit = fields.Float("Unit Price")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    price_subtotal = fields.Monetary("Amount", currency_field="currency_id")
    total_amount = fields.Float(compute="_compute_total_amount")


    @api.depends('price_subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum([r.price_subtotal for r in self])

