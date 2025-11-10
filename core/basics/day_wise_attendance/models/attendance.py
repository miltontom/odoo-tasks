import datetime

from odoo import models, fields

class Attendance(models.Model):
    _name = "attendance"
    _description = "Day wise attendance list"

    employee_id = fields.Many2one("hr.employee")
    active = fields.Boolean(default=True)
    date = fields.Date(default=datetime.date.today())

    def generate_absentees(self):
        in_attendance = self.env['hr.attendance'].search([]).mapped('employee_id.id')
        absentees = self.env['hr.employee'].search([('id', 'not in', in_attendance)])

        for absentee in absentees:
            exists = self.env['attendance'].search([('employee_id', '=', absentee.id)])
            if not exists:
                self.env['attendance'].create({'employee_id': absentee.id})
            else:
                to_unlink = self.env['attendance'].search([('employee_id', 'in', in_attendance)])
                for rec in to_unlink:
                    rec.unlink()

