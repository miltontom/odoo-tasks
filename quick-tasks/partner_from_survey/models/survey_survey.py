from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    contact_relation_id = fields.One2many("contact.relation", "survey_id")
