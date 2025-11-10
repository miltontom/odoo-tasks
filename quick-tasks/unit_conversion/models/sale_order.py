from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    quantity = fields.Float()
    from_unit = fields.Many2one("uom.uom")
    from_unit_categ_id = fields.Many2one(
        "uom.category", compute="_compute_from_unit_categ_id"
    )
    to_unit = fields.Many2one(
        "uom.uom",
        domain="[('category_id', '=', from_unit_categ_id), ('id', '!=', from_unit)]",
    )
    converted_quantity = fields.Float()

    @api.depends("from_unit")
    def _compute_from_unit_categ_id(self):
        self.from_unit_categ_id = self.from_unit.category_id.id

    def action_convert_quantity(self):
        self.write(
            {
                "converted_quantity": self.from_unit._compute_quantity(
                    self.quantity, self.to_unit
                )
            }
        )
