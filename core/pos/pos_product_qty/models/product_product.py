from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = ["product.product"]

    pos_quantity = fields.Integer(compute="_compute_pos_quantity")

    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ["qty_available", "pos_quantity"]
        return result

    def _compute_pos_quantity(self):
        icp_sudo = self.env["ir.config_parameter"].sudo()
        print("icp", icp_sudo.get_param("res.config.settings.location_id"))
        param = icp_sudo.get_param("res.config.settings.location_id")
        location_id = eval(param) if param else -1
        print(location_id)

        for product in self:
            quant = self.env['stock.quant'].search([('product_id', '=', product.id), ('location_id', '=', location_id)])
            product.pos_quantity = quant.quantity
