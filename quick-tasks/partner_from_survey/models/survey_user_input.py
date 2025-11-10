from odoo import api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)

        contact_relation = self.env["contact.relation"].search(
            [("survey_id", "=", res.survey_id.id)]
        )

        contact_relation_line = contact_relation.filtered(
            lambda s: s.question_id == res.question_id
        )
        corresponding_partner_field = contact_relation_line.partner_field

        if not contact_relation.partner_id and corresponding_partner_field == "name":
            partner = self.env["res.partner"].create(
                {corresponding_partner_field: res.value_char_box}
            )
            contact_relation.partner_id = partner.id
        else:
            contact_relation.partner_id.write(
                {corresponding_partner_field: res.value_char_box}
            )
        return res
