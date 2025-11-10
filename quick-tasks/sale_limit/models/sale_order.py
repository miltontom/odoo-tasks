from odoo import models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        sale_manager_id = (
            self.env["crm.team"]
            .search(
                [
                    ("id", "=", self.team_id.id),
                ]
            )
            .user_id.id
        )

        if sale_manager_id == self.env.user.id:
            return

        SALE_LIMIT = 50_000
        currency_sym = self.env.company.currency_id.symbol

        if self.amount_total >= SALE_LIMIT:
            raise UserError(
                f"Total cannot exceed the maximum ({currency_sym}{SALE_LIMIT:,}) set for a sale order."
            )
