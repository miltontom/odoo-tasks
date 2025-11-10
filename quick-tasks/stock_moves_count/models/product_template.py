from odoo import fields, models
from datetime import datetime
from datetime import timedelta


class ProductTemplate(models.Model):
    _inherit = "product.template"

    moves_count = fields.Integer(compute="_compute_moves_count")

    def _compute_moves_count(self):
        last_week = datetime.now() - timedelta(days=7)
        print("lastweek", last_week)

        res = self.env["stock.move.line"].search(
            [
                ("product_id", "=", self.product_variant_id.id),
                ("date", ">=", last_week),
                ("state", "=", "done"),
            ]
        )
        for p in self:
            p.moves_count = len(res)
