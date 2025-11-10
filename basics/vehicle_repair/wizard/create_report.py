import io
import json

import xlsxwriter

from odoo import fields, models
from odoo.exceptions import MissingError
from odoo.tools.json import json_default


class CreateReport(models.TransientModel):
    _name = "create.report.wizard"

    customer_ids = fields.Many2many("res.partner", string="Customer")
    service_advisor_ids = fields.Many2many("res.users", string="Service Advisor")
    start_date = fields.Date()
    end_date = fields.Date()

    def get_query(self):
        query = """
                SELECT
                    partner.name AS "customer",
                    model_categ.name AS "vehicle category",
                    model.name AS "vehicle model",
                    repair.vehicle_number AS "vehicle number",
                    advisor.name AS "service advisor",
                    repair.state AS "state",
                    repair.start_date AS "start date",
                    repair.delivery_date AS "delivery date",
                    repair.estimated_amount AS "estimated amount",
                    repair.service_type AS "service type",
                    (repair.total_labor_cost + repair.total_consumed_parts) AS "total amount"
                FROM
                    vehicle_repair AS repair
                    JOIN res_partner AS partner ON partner.id = repair.name_id
                    JOIN res_partner AS advisor ON advisor.user_id = repair.service_advisor_id
                    JOIN fleet_vehicle_model_category AS model_categ ON model_categ.id = repair.vehicle_type_id
                    JOIN fleet_vehicle_model AS model ON model.id = repair.vehicle_model_id
                """

        if any([self.customer_ids, self.service_advisor_ids, self.start_date]):
            domain = "WHERE "
            if self.customer_ids:
                ids = ",".join([str(id) for id in self.customer_ids.ids])
                domain += f"partner.id IN ({ids})\n"

            if self.service_advisor_ids:
                ids = ",".join([str(id) for id in self.service_advisor_ids.ids])
                domain += f"repair.service_advisor_id IN ({ids})\n"

            if self.start_date and self.end_date:
                domain += f"repair.start_date >= '{self.start_date}' AND repair.delivery_date <= '{self.end_date}'\n"
            elif self.start_date:
                domain += f"repair.start_date >= '{self.start_date}'\n"

            split = domain.split("\n")
            if "" in split:
                split.remove("")
            final_domain = " AND ".join(split)
            query += final_domain

        return query

    def action_create_report(self):
        self.env.cr.execute(self.get_query())
        records = self.env.cr.dictfetchall()  # list of dictionaries

        customer_len = len(self.customer_ids)
        service_adv_len = len(self.service_advisor_ids)

        customer = self.customer_ids if customer_len == 1 else None
        service_advisor = self.service_advisor_ids if service_adv_len == 1 else None

        data = {
            "records": records,
            "customer_len": customer_len,
            "service_adv_len": service_adv_len,
            "customer": customer.name if customer != None else "",
            "service_advisor": service_advisor.name if service_advisor != None else "",
        }

        return self.env.ref(
            "vehicle_repair.vehicle_repair_report_action"
        ).report_action(self, data=data)

    def action_create_report_xlsx(self):
        self.env.cr.execute(self.get_query())
        query_result = self.env.cr.dictfetchall()
        data = {
            "records": query_result,
            "customer_len": len(self.customer_ids),
            "service_adv_len": len(self.service_advisor_ids),
        }

        return {
            "type": "ir.actions.report",
            "data": {
                "model": "create.report.wizard",
                "options": json.dumps(data, default=json_default),
                "output_format": "xlsx",
                "report_name": "Excel Report",
            },
            "report_type": "xlsx",
        }

    def get_xlsx_report(self, data, response):
        # print(json.dumps(data, default=json_default, indent=2))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        sheet = workbook.add_worksheet()
        col_head = workbook.add_format(
            {"align": "center", "bold": True, "font_size": "11px", "border": 1}
        )
        sheet.set_column("B:N", 20)
        txt = workbook.add_format({"font_size": "10px", "align": "center", "border": 1})
        single = workbook.add_format({"bold": True})

        customer_len = data.get("customer_len", 0)
        service_adv_len = data.get("service_adv_len", 0)

        customers = [d.get("customer") for d in data["records"]]
        service_advisors = [d.get("service advisor") for d in data["records"]]
        model_categories = [d.get("vehicle category") for d in data["records"]]
        models = [d.get("vehicle model") for d in data["records"]]
        vehicle_numbers = [d.get("vehicle number") for d in data["records"]]
        states = [d.get("state").replace("_", " ").title() for d in data["records"]]
        start_dates = [d.get("start date") for d in data["records"]]
        end_dates = [d.get("delivery date") for d in data["records"]]
        estimated_amounts = [d.get("estimated amount") for d in data["records"]]
        service_types = [d.get("service type") for d in data["records"]]
        total_amounts = [d.get("total amount") for d in data["records"]]

        if data.get("customer_len", 0) == 1:
            sheet.write("D3", "Customer:", single)
            sheet.write("E3", data["records"][0].get("customer"))

        if data.get("service_adv_len", 0) == 1:
            sheet.write("D4", "Service Advisor:", single)
            sheet.write("E4", data["records"][0].get("service advisor"))

        col = 6
        if customer_len > 1 or customer_len == 0:
            sheet.write(f"B{col}", "Customer", col_head)
            sheet.write_column(f"B{(col := col + 1)}", customers, txt)
        col = 6
        if service_adv_len > 1 or service_adv_len == 0:
            sheet.write(f"C{col}", "Service Advisor", col_head)
            sheet.write_column(f"C{(col := col + 1)}", service_advisors, txt)
        col = 6
        sheet.write(f"D{col}", "Vehicle Category", col_head)
        sheet.write_column(f"D{(col := col + 1)}", model_categories, txt)
        col = 6
        sheet.write(f"E{col}", "Vehicle Model", col_head)
        sheet.write_column(f"E{(col := col + 1)}", models, txt)
        col = 6
        sheet.write(f"F{col}", "Vehicle Number", col_head)
        sheet.write_column(f"F{(col := col + 1)}", vehicle_numbers, txt)
        col = 6
        sheet.write(f"G{col}", "State", col_head)
        sheet.write_column(f"G{(col := col + 1)}", states, txt)
        col = 6
        sheet.write(f"H{col}", "Start Date", col_head)
        sheet.write_column(f"H{(col := col + 1)}", start_dates, txt)
        col = 6
        sheet.write(f"I{col}", "End Date", col_head)
        sheet.write_column(f"I{(col := col + 1)}", end_dates, txt)
        col = 6
        sheet.write(f"J{col}", "Service Type", col_head)
        sheet.write_column(f"J{(col := col + 1)}", service_types, txt)
        col = 6
        sheet.write(f"K{col}", "Estimated Amount", col_head)
        sheet.write_column(f"K{(col := col + 1)}", estimated_amounts, txt)
        col = 6
        sheet.write(f"L{col}", "Total Amount", col_head)
        sheet.write_column(f"L{(col := col + 1)}", total_amounts, txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
