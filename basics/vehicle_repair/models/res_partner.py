from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    repairs_count = fields.Integer(
        string="Repair count", compute="_compute_repairs_count"
    )
    vehicle_repair_ids = fields.One2many("vehicle.repair", "name_id")
    state = fields.Selection(
        [("non_service", "Non-Service"), ("service", "Service")], default="non_service"
    )

    def action_archive(self):
        for rec in self:
            rec.vehicle_repair_ids.write({"active": False})
        return super(ResPartner, self).action_archive()

    def action_unarchive(self):
        for record in self:
            archived_records = self.env["vehicle.repair"].search(
                [("name_id", "=", record.id), ("active", "=", False)]
            )
            archived_records.write({"active": True})
        return super(ResPartner, self).action_unarchive()

    def _compute_repairs_count(self):
        self.repairs_count = len(self.vehicle_repair_ids)

    def action_view_repairs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Repairs",
            "view_mode": "list,form",
            "res_model": "vehicle.repair",
            "domain": [("name_id", "=", self.id)],
            "context": "{'create': False}",
        }

    def action_create_repair_request(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Repairs",
            "view_mode": "form",
            "res_model": "vehicle.repair",
            "context": {"default_name_id": self.id},
        }
