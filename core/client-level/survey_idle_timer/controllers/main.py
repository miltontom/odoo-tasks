from odoo import fields
from odoo.addons.survey.controllers.main import Survey


class SurveyInherit(Survey):

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        data = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)
        per_question_time_limit = survey_sudo.per_question_time_limit
        question_time_limit_seconds = survey_sudo.question_time_limit_seconds

        if (
            per_question_time_limit
            and question_time_limit_seconds
            and answer_sudo.start_datetime
        ):
            data.update(
                {
                    "question_time_limit_seconds": question_time_limit_seconds,
                    "server_time": fields.Datetime.now(),
                    "timer_start": answer_sudo.start_datetime.isoformat(),
                    "per_question_time_limit": per_question_time_limit,
                }
            )

        return data
