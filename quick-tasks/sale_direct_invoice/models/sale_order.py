from odoo import Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_create_invoice(self):
        wizard = self.env["sale.advance.payment.inv"].create(
            {
                "advance_payment_method": "delivered",
                "sale_order_ids": [Command.link(self.id)],
            }
        )
        action = wizard.create_invoices()
        return action
