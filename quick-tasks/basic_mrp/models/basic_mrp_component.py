from odoo import fields, models


class BasicMrpComponent(models.Model):
    _name = "basic.mrp.component"

    is_quantity_available = fields.Boolean(compute="_compute_is_quantity_available")
    basic_mrp_id = fields.Many2one("basic.mrp")
    product_id = fields.Many2one("product.product")
    quantity = fields.Integer()

    def _compute_is_quantity_available(self):
        for line in self:
            if line.product_id.qty_available >= line.quantity:
                line.is_quantity_available = True
            else:
                line.is_quantity_available = False
