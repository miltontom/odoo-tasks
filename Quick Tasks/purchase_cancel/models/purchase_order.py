from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_id = fields.Many2one("sale.order")

    def button_confirm(self):
        res = self.search([("sale_order_id", "=", self.sale_order_id.id)]).filtered(
            lambda x: x.id != self.id
        )

        for r in res:
            r.button_cancel()
        super().button_confirm()
