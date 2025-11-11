from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.onchange("remaining_hours")
    def _onchange_remaining_hours(self):
        if self.remaining_hours < 0:
            raise ValidationError("Time entered is greater than the allocated time")
