from odoo import models, api


class VehicleRepairReportTemplates(models.AbstractModel):
    _name = "report.vehicle_repair.vehicle_repair_report_template"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = data.get("records")

        return {
            "doc_ids": docids,
            "doc_model": "vehicle.repair",
            "docs": docs,
            "data": data,
        }
