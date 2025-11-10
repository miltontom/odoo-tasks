from odoo import http
from odoo.http import request
import base64


class Main(http.Controller):
    @http.route("/new_product", type="http", auth="user", website=True)
    def new_product(self, **kwargs):
        return request.render("website_product_form.new_product_page")

    @http.route("/create_product")
    def create_product(self, **kwargs):
        image = kwargs.get("file")

        product = request.env["product.template"].create(
            {
                "name": kwargs.get("name"),
                "list_price": kwargs.get("price"),
                "is_published": True,
                "image_1920": base64.b64encode(image.read()) if image else False,
            }
        )
        return request.redirect(f"/shop/{product.id}")
