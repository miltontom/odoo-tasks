from odoo import fields, models


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    requisition_dept_manager = fields.Many2one("res.users")
    requisition_head = fields.Many2one("res.users")

    def action_requisition_request(self):
        """
        target
        new - opens like a wizard
        current - regular form view
        fullscreen - as in the name
        main - regular form view without breadcrumbs
        inline - ??
        """
        return {
            "type": "ir.actions.act_window",
            "name": "Requests",
            "res_model": "requisition.request",
            "view_mode": "form",
            "target": "inline",
            "context": {"default_employee_id": self.id},
        }
