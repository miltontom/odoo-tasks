import logging

from odoo import fields, api, models
from datetime import datetime


class Lead(models.Model):
    _inherit = "crm.lead"

    def action_check_time_difference(self):
        records = self.env["crm.lead"].search([])

        for rec in records:
            recent_activity = self.env["mail.activity"].search(
                [("res_model", "=", "crm.lead"), ("res_id", "=", rec.id)],
                limit=1,
                order="create_date DESC",
            )

            current_time = datetime.now()
            activity_created_time = recent_activity.create_date

            if activity_created_time:
                threshold_minutes = int(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("res.config.settings.threshold")
                )

                time_diff_minutes = (current_time - activity_created_time).seconds / 60

                if time_diff_minutes > threshold_minutes:
                    rec.sudo().action_archive()
