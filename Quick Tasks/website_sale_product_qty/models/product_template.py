from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    ws_location_product_qty = fields.Float(compute="_compute_ws_location_product_qty")

    def _compute_ws_location_product_qty(self):
        icp_sudo = self.env["ir.config_parameter"].sudo()
        param = icp_sudo.get_param("res.config.settings.location_id")
        location_id = int(param.strip("[]")) if param else 0

        for rec in self:
            res = self.env["stock.quant"].search(
                [
                    ("location_id", "=", location_id),
                    ("product_id", "=", rec.product_variant_id.id),
                ]
            )
            rec.ws_location_product_qty = res.quantity
