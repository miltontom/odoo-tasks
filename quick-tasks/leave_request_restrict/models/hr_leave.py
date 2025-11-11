from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.fields import datetime
from dateutil.relativedelta import relativedelta


class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    def _check_validity(self):
        recent_request = self.search(
            [
                ("employee_id", "=", self.employee_id.id),
                ("holiday_status_id", "=", self.holiday_status_id.id),
                ("id", "!=", self.id),
            ],
            limit=1,
            order="create_date DESC",
        )

        if recent_request:
            date_from_last_request = recent_request.create_date + relativedelta(days=30)
            if datetime.now() <= date_from_last_request:
                raise ValidationError("You can only request after 30 days")
        super()._check_validity()
