from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_change_units_to_dozen(self):
        dozens_unit = self.env["uom.uom"].search([("name", "=", "Dozens")])

        draft_records = self.filtered(lambda s: s.state == "draft")
        draft_records.mapped("order_line").filtered(
            lambda s: s.product_uom.name == "Units"
        ).write({"product_uom": dozens_unit.id})
