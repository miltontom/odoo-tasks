from odoo import api, Command, fields, models


class RequisitionRequest(models.Model):
    _name = "requisition.request"
    _order = "state"
    _rec_name = "employee_id"

    employee_id = fields.Many2one(
        "hr.employee", required=True, default=lambda self: self.env.user.employee_id
    )
    lines = fields.One2many("requisition.request.line", "requisition_request_id")
    state = fields.Selection(
        [
            ("confirm", "To Approve"),
            ("validate1", "Second Approval"),
            ("validate", "Approved"),
            ("reject", "Rejected"),
        ]
    )

    def action_confirm(self):
        self.state = "confirm"

    def action_approve(self):
        self.state = "validate1"

    def action_reject(self):
        self.state = "reject"

    def action_validate(self):
        self.state = "validate"

        PurchaseOrder = self.env["purchase.order"]
        InternalTransfer = self.env["stock.picking"]

        for line in self.lines:
            if line.route == "purchase":
                order_lines = [Command.create({"product_id": line.product_id.id})]
                for vendor in line.vendor_ids:
                    PurchaseOrder.create(
                        {"order_line": order_lines, "partner_id": vendor.partner_id.id}
                    )

            if line.route == "internal":
                move_lines = [
                    Command.create(
                        {
                            "name": "Internal Transfer (Requisition)",
                            "product_id": line.product_id.id,
                        }
                    )
                ]
                InternalTransfer.create(
                    {
                        "move_ids": move_lines,
                        "picking_type_code": "internal",
                        "picking_type_id": self.env.ref(
                            "stock.picking_type_internal"
                        ).id,
                        "location_id": line.src_location_id.id,
                        "location_dest_id": line.dest_location_id.id,
                    }
                )
