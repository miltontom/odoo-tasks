from odoo import fields, models
from pprint import pprint


class SaleOrder(models.Model):
    _inherit = "sale.order"

    manuf_order_id = fields.Many2one("mrp.production")
    purchase_order_id = fields.Many2one("purchase.order")

    def action_confirm(self):
        super().action_confirm()
        for line in self.order_line:
            res = line.product_id.create_order(
                {"sale_order_id": self.id, "partner_id": self.partner_id.id}
            )

            if res[0]:
                self.manuf_order_id = res[1]
            else:
                self.purchase_order_id = res[1]

    def action_view_created_mo(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Order",
            "view_mode": "form",
            "res_model": "mrp.production" if self.manuf_order_id else "purchase.order",
            "res_id": (
                self.manuf_order_id.id
                if self.manuf_order_id
                else self.purchase_order_id.id
            ),
            "target": "current",
        }
