from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    _sql_constraints = [
        (
            "check_question_time_limit_seconds",
            "CHECK(question_time_limit_seconds != 0",
            "Seconds cannot be zero!",
        )
    ]

    per_question_time_limit = fields.Boolean()
    question_time_limit_seconds = fields.Integer(
        string="Question Time Limit", help="Per question time limit"
    )
