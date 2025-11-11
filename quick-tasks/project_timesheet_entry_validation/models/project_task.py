from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.constrains("user_ids")
    def _check_user_ids(self):
        if len(self.user_ids) > 1:
            raise ValidationError("You can only select one assignee")

    @api.onchange("timesheet_ids")
    def _onchange_timesheet_ids(self):
        dates = self.timesheet_ids.grouped(lambda x: x.date)

        for date in dates:
            emp_hours_per_day = dates[
                date
            ].employee_id.resource_calendar_id.hours_per_day
            hours_worked_for_the_day = sum(dates[date].mapped("unit_amount"))

            if hours_worked_for_the_day > emp_hours_per_day:
                raise ValidationError(f"Overtime on {date.strftime("%m/%d/%Y")}")
