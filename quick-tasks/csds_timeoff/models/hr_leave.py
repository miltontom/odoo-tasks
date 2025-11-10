from odoo import fields, models


class HRLeave(models.Model):
    _inherit = "hr.leave"

    def _check_validity(self):
        leave_type = self.holiday_status_id
        if leave_type.allow_extra_leaves:
            return
        return super()._check_validity()
