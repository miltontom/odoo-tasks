from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_progress = fields.Integer(
        string="Progress (%)", compute="_compute_project_progress"
    )

    @api.depends("task_count")
    def _compute_project_progress(self):
        completed_tasks = self.env["project.task"].search_count(
            [("project_id", "=", self.id), ("is_closed", "=", True)]
        )

        print("completed", completed_tasks, "total", self.task_count)
        self.project_progress = (completed_tasks / self.task_count) * 100

