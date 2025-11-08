from odoo import fields, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    requisition_request_line_id = fields.Many2one("requisition.request.line")
