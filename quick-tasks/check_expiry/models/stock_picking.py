from odoo import models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for r in self.move_line_ids:
            if (
                self.scheduled_date
                and r.expiration_date
                and self.scheduled_date >= r.expiration_date
            ):
                raise ValidationError("Seems like on the product(s) have been expired")
        return super().button_validate()
