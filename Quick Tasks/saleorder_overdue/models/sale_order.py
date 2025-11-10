from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    overdue = fields.Boolean(related="partner_id.is_saleorder_overdue")

    def _action_confirm(self):
        if not self.partner_id.last_sales_date:
            self.partner_id.last_sales_date = self.date_order
            return

        days_since_last_order = (datetime.now() - self.partner_id.last_sales_date).days

        if days_since_last_order >= 90:
            raise ValidationError(
                "There is a 90 days overdue for the selected customer."
            )
