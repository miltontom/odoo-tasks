from odoo import fields, models


class TeamMember(models.Model):
    _inherit = "crm.team.member"

    commission_id = fields.Many2one("crm.commission")
    first_target_achieved = fields.Boolean()
