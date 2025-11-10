from odoo import api, fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    state = fields.Selection(
        [("onboard", "Onboarding"), ("offboard", "Offboarding")], default="onboard"
    )

    @api.onchange("resource_calendar_id")
    def _onchange_resource_calendar_id(self):
        for rec in self:
            if not rec.resource_calendar_id:
                rec.state = "offboard"
                rec.action_archive()
            else:
                rec.state = "onboard"
                rec.action_unarchive()
