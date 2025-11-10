from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _name = "res.config.settings"
    _inherit = "res.config.settings"

    location_id = fields.Many2one(
        "stock.location",
        string="Warehouse Location",
        domain=[("usage", "=", "internal")],
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        icp_sudo = self.env["ir.config_parameter"].sudo()
        param = icp_sudo.get_param("res.config.settings.location_id")
        location_id = int(param.strip("[]")) if param else False
        res.update(location_id=location_id)
        return res

    def set_values(self):
        res = super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "res.config.settings.location_id", self.location_id.ids
        )
        return res
