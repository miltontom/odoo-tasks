import json

from odoo import http
from odoo.http import request
from odoo.tools.json import json_default


class VehicleRepairMenuController(http.Controller):
    @http.route("/vehicle_repair/request", type="http", auth="user", website=True)
    def vehicle_repair(self, **kwargs):
        """Render the form"""

        customers = request.env["res.partner"].search([])
        vehicle_model_categ = request.env["fleet.vehicle.model.category"].search([])
        vehicle_model = request.env["fleet.vehicle.model"].search([])
        options = {
            "model_categ": vehicle_model_categ,
            "model": vehicle_model,
            "customer": customers,
        }
        return request.render("vehicle_repair.vehicle_repair_website_page", options)

    @http.route(
        "/vehicle_repair/request/submit", type="http", auth="user", website=True
    )
    def vehicle_repair_submit_form(self, **post):
        """Create a record in the backend on clicking submit"""

        customer_id = (
            request.env["res.partner"].search([("name", "=", post.get("customer"))]).id
        )
        service_advisor_id = request.env.user.id
        vehicle_type_id = (
            request.env["fleet.vehicle.model.category"]
            .search([("name", "=", post.get("model_category"))])
            .id
        )
        vehicle_model_id = (
            request.env["fleet.vehicle.model"]
            .search([("name", "=", post.get("model"))])
            .id
        )

        vals = {
            "customer_id": customer_id,
            "service_advisor_id": service_advisor_id,
            "vehicle_type_id": vehicle_type_id,
            "vehicle_model_id": vehicle_model_id,
        }

        if self.record_exists(vals):
            return request.render("vehicle_repair.duplicate_record_error")

        request.env["vehicle.repair"].sudo().create(
            {
                "name_id": customer_id,
                "service_advisor_id": service_advisor_id,
                "vehicle_type_id": vehicle_type_id,
                "vehicle_model_id": vehicle_model_id,
            }
        )
        return request.redirect("/contactus-thank-you")

    @http.route("/vehicle_repair/top_repairs", type="json", auth="user", website=True)
    def top_repairs(self):
        records = request.env["vehicle.repair"].search([])

        record_list = []
        for r in records:
            record_list.append(
                {
                    "id": r.id,
                    "repair_order": r.name,
                    "customer": r.name_id.name,
                    "image": r.image,
                }
            )

        json_data = json.dumps(record_list, default=json_default)

        return json_data

    @http.route(
        "/vehicle_repair/top_repairs/view_card/<string:id>", type="http", auth="user"
    )
    def view_card_info(self, **kwargs):
        # url = f"/web#id={record.id}&model=vehicle.repair&action=vehicle_repair.vehicle_repair_action&view_type=form"
        url = f"/web#id={kwargs.get('id')}&model=vehicle.repair"
        return request.redirect(url)

    @http.route("/vehicle_repair/top_repairs/view_card/web/<int:id>", website=True)
    def view_card_info_web(self, **kwargs):
        record = request.env["vehicle.repair"].browse(kwargs.get("id"))
        return request.render("vehicle_repair.card_info", {"record": record})

    @http.route("/contact/request", type="http", auth="user", website=True)
    def contact_request(self, **kwargs):
        return request.render("vehicle_repair.contact_request_page")

    @http.route("/contact/request/submit", type="http", auth="user", website=True)
    def contact_request_submit(self, **kwargs):
        request.env["res.partner"].sudo().create(
            {"name": kwargs.get("name"), "email": kwargs.get("email")}
        )
        return request.redirect("/contactus-thank-you")

    @http.route("/vehicle_repair/requests", website=True)
    def repair_requests(self, **kwargs):
        records = request.env['vehicle.repair'].search([])
        return request.render("vehicle_repair.repair_requests_page", {"records": records})

    def record_exists(self, vals):
        return request.env["vehicle.repair"].search(
            [
                ("name_id", "=", vals.get("customer_id")),
                ("vehicle_type_id", "=", vals.get("vehicle_type_id")),
                ("vehicle_model_id", "=", vals.get("vehicle_model_id")),
            ]
        )
