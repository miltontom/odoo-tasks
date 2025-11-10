from odoo import fields, models


class HRLeave(models.Model):
    _inherit = "hr.leave"

    # application fields
    acting_person_id = fields.Many2one("hr.employee", string="Acting Person")
    is_leaving_country = fields.Boolean()
    backdated_reason = fields.Char()
    leave_block_exemption_reason = fields.Char()
    exit_country_block_exemption_reason = fields.Char()

    # planner fields
    leave_reason = fields.Char()

    # also valid
    # def action_go_back(self):
    #     return self.env.ref("hr_holidays.hr_leave_action_my").read()[0]
