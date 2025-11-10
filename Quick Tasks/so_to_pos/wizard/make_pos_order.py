from datetime import datetime

from odoo import Command
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class MakePosOrder(models.TransientModel):
    _name = "make.pos.order.wizard"

    sale_order_id = fields.Many2one("sale.order")
    payment_line_ids = fields.One2many("payment.line", "make_pos_order_id")
    total_amount = fields.Float(compute="_compute_total_amount")
    remaining_amount = fields.Float(compute="_compute_remaining_amount")
    shop_id = fields.Many2one("pos.config", compute="_compute_shop_id")

    @api.depends("payment_line_ids")
    def _compute_shop_id(self):
        self.shop_id = self._context.get("shop_id")

    @api.depends("payment_line_ids")
    def _compute_total_amount(self):
        self.total_amount = self._context.get("amount_total")

    @api.depends("payment_line_ids")
    def _compute_remaining_amount(self):
        sale_order = self.env["sale.order"].browse(self._context.get("active_id"))

        total = sale_order.remaining_amount
        for line in self.payment_line_ids:
            if total > 0:
                total -= line.amount_paid
            else:
                raise UserError("You have nothing to pay.")

        self.remaining_amount = total

    def action_confirm_payment(self):
        if not self.payment_line_ids:
            raise ValidationError("Please provide at least one payment method.")

        sale_order = self.env["sale.order"].browse(self._context.get("active_id"))

        if self.remaining_amount == 0:
            sale_order.pos_order_id.state = "paid"
            sale_order.state = "paid_at_counter"
        else:
            sale_order.write({"remaining_amount": self.remaining_amount})

        payment_lines = []
        for line in self.payment_line_ids:
            payment_lines.append(
                Command.create(
                    {
                        "payment_date": datetime.now(),
                        "payment_method_id": line.payment_method_id.id,
                        "amount": line.amount_paid,
                    }
                )
            )
        sale_order.pos_order_id.write({"payment_ids": payment_lines})
