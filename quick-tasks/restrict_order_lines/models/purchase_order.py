from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        if self.partner_id.restrict_order_lines:
            restriction_count = self.partner_id.restrict_count
            if len(self.order_line) > restriction_count:
                raise ValidationError(
                    f"The order lines is restricted to {restriction_count} items for the selected vendor '{self.partner_id.name}'"
                )
        return super().button_confirm()

    @api.onchange("order_line")
    def check_order_line_len(self):
        if (
            len(self.order_line) > self.partner_id.restrict_count
            and self.partner_id.restrict_order_lines
        ):
            raise ValidationError(
                f"The order lines is restricted to {self.partner_id.restrict_count} items for the selected vendor '{self.partner_id.name}'"
            )
