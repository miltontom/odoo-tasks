from odoo import fields, models


class HRLeaveType(models.Model):
    _inherit = "hr.leave.type"

    allow_extra_leaves = fields.Boolean()
