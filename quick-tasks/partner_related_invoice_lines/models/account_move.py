from odoo import api, Command, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    related_invoice_ids = fields.One2many(
        "related.invoice.line",
        "account_move_id",
        compute="_compute_related_invoice_ids",
        store=True,
    )

    related_invoices_count = fields.Integer(compute="_compute_related_invoices_count")

    @api.depends("related_invoice_ids")
    def _compute_related_invoices_count(self):
        self.related_invoices_count = len(self.related_invoice_ids)

    @api.depends("partner_id")
    def _compute_related_invoice_ids(self):
        res = self.search(
            [
                ("partner_id", "=", self.partner_id.id),
                ("state", "=", "posted"),
                ("move_type", "=", "out_invoice"),
            ]
        )

        invoice_line_ids = res.mapped("invoice_line_ids")
        lines = [
            Command.create(
                {
                    "product_id": line.product_id.id,
                    "quantity": line.quantity,
                    "price": line.price_unit,
                    "price_subtotal": line.price_subtotal,
                }
            )
            for line in invoice_line_ids
        ]
        self.related_invoice_ids = [Command.clear()] + lines

    def action_add_all(self):
        related_lines = self.env["related.invoice.line"].search(
            [("account_move_id", "=", self.id)]
        )
        lines = [
            Command.create(
                {
                    "product_id": line.product_id.id,
                    "quantity": line.quantity,
                }
            )
            for line in related_lines
        ]

        self.invoice_line_ids = lines
        self.related_invoice_ids = [Command.clear()]
