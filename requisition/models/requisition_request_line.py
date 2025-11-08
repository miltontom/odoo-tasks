from odoo import api, fields, models


class RequisitionRequestLine(models.Model):
    _name = "requisition.request.line"

    product_id = fields.Many2one("product.product", required=True)
    route = fields.Selection(
        [("purchase", "Purchase Order"), ("internal", "Internal Transfer")],
        required=True,
    )
    vendor_ids = fields.Many2many(
        "product.supplierinfo", domain="[('product_tmpl_id', '=', product_id)]"
    )
    requisition_request_id = fields.Many2one(
        "requisition.request", "requisition_request_line_id"
    )

    src_location_id = fields.Many2one(
        "stock.location", domain="[('usage', '=', 'internal')]"
    )
    dest_location_id = fields.Many2one(
        "stock.location", domain="[('usage', '=', 'internal')]"
    )
