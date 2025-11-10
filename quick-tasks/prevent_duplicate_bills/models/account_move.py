from odoo import api, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        duplicate_vendor_bills = (
            self.env["account.move"]
            .search([("move_type", "=", "in_invoice")])
            .filtered(
                lambda self: self.ref == vals_list[0].get("ref")
                and self.partner_id.id == vals_list[0].get("partner_id")
                and self.amount_total
                == vals_list[0].get("tax_totals").get("total_amount")
            )
        )

        if duplicate_vendor_bills:
            raise ValidationError(
                "A vendor bill with the same reference, vendor and total amount already exists."
            )

        return super().create(vals_list)
