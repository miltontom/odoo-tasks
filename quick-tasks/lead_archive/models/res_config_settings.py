from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _name = "res.config.settings"
    _inherit = "res.config.settings"

    threshold = fields.Char()

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env["ir.config_parameter"].sudo()
        threshold = icp_sudo.get_param("res.config.settings.threshold")
        res.update(
            threshold=threshold,
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param("res.config.settings.threshold", self.threshold)
        print(icp.get_param("res.config.settings.threshold"))

        return res
