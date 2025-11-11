from odoo import Command, fields, models


class RelatedInvoiceLine(models.Model):
    _name = "related.invoice.line"

    account_move_id = fields.Many2one("account.move")
    product_id = fields.Many2one("product.product")
    quantity = fields.Float()
    price = fields.Float()
    price_subtotal = fields.Float()

    def action_add_to_invoice_lines(self):
        self.account_move_id.invoice_line_ids = [
            Command.create(
                {"product_id": self.product_id.id, "quantity": self.quantity}
            )
        ]
        self.unlink()
