from odoo import Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[("paid_at_counter", "Paid at counter")])
    pos_session_id = fields.Many2one(
        "pos.session", default=lambda self: self._default_pos_session()
    )
    pos_order_id = fields.Many2one("pos.order")

    remaining_amount = fields.Float()

    def _default_pos_session(self):
        most_recent_session = self.env["pos.session"].search(
            [], limit=1, order="start_at DESC"
        )
        return most_recent_session

    def _action_confirm(self):
        order_lines = []
        for line in self.order_line:
            order_lines.append(
                Command.create(
                    {
                        "product_id": line.product_id.id,
                        "qty": line.product_uom_qty,
                        "price_unit": line.price_unit,
                        "price_subtotal": line.price_subtotal,
                        "price_subtotal_incl": line.price_subtotal,
                    }
                )
            )
        vals = {
            "name": self.name,
            "session_id": self.pos_session_id.id,
            "user_id": self.pos_session_id.user_id.id,
            "partner_id": self.partner_id.id,
            "state": "draft",
            "lines": order_lines,
            "amount_tax": self.amount_tax,
            "amount_total": self.amount_total,
            "amount_paid": 0,
            "amount_return": 0,
        }
        self.remaining_amount = self.amount_total
        pos_order = self.env["pos.order"].create(vals)
        self.pos_order_id = pos_order.id

    def action_pay_at_counter(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "make.pos.order.wizard",
            "view_mode": "form",
            "view_type": "form",
            "target": "new",
            "context": {
                "partner_id": self.partner_id.id,
                "amount_total": self.amount_total,
                "shop_id": self.pos_session_id.config_id.id,
                "session_id": self.pos_session_id.id,
                "order_lines": self.order_line.ids,
                "amount_tax": self.amount_tax,
                "ref": self.name,
            },
        }
