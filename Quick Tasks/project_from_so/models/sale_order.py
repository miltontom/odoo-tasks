from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_project_id = fields.Many2one(
        "project.project", domain="[('partner_id', '=', partner_id)]"
    )

    project_empty = fields.Boolean(compute="_compute_project_empty")
    task_id = fields.Many2one("project.task")
    subtask_count = fields.Integer(related="task_id.subtask_count")

    @api.depends("partner_project_id")
    def _compute_project_empty(self):
        self.project_empty = self.partner_project_id.task_count == 0

    def action_create_task(self):
        task_id = self.env["project.task"].create(
            {
                "project_id": self.partner_project_id.id,
                "name": f"SO/{self.id} - {self.partner_id.name}",
                "description": f"Order Date - {self.date_order}<br/>Total Order Lines - {len(self.order_line)}<br/>Total Amount - {sum(self.order_line.mapped('price_subtotal'))}",
                "user_ids": [self.user_id.id],
            }
        )

        self.task_id = task_id.id

        sorted_order_line = sorted(
            self.order_line, key=lambda self: self.price_subtotal, reverse=True
        )

        for line in sorted_order_line:
            self.env["project.task"].create(
                {
                    "project_id": self.partner_project_id.id,
                    "parent_id": task_id.id,
                    "name": f"{line.product_template_id.name} - Qty: {line.product_uom_qty} Amount: {line.price_subtotal}",
                }
            )

    def action_view_created_task(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Task",
            "view_mode": "form",
            "res_model": "project.task",
            "res_id": self.task_id.id,
            "target": "current",
        }
