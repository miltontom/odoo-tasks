from odoo import api, fields, models
from pprint import pprint


class ContactRelation(models.Model):
    _name = "contact.relation"

    partner_id = fields.Many2one("res.partner")
    survey_id = fields.Many2one("survey.survey")
    question_id = fields.Many2one(
        "survey.question", domain="[('survey_id', '=', survey_id)]", ondelete="cascade"
    )

    partner_field = fields.Selection(
        [("name", "Name"), ("email", "Email"), ("mobile", "Mobile")], required=True
    )
