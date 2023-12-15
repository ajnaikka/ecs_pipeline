# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ExamAddSurvey(models.TransientModel):
    _name = 'exam.add.survey'
    _description = 'Add Question to exam'

    exam_id = fields.Many2one('op.exam', string="Exam", required=True)
    subject_id = fields.Many2one('op.subject', 'Subject', related="exam_id.subject_id")
    question_level = fields.Selection([('hard', 'Hard'), ('moderate', 'Moderate'), ('easy', 'Easy')], string="Question Type", default='hard', required=True)
    survey_id = fields.Many2one('survey.survey', string="survey", required=True, domain="[('question_level', '=', question_level), ('subject_id', '=', subject_id), ('active', '=', True)]")
    exam_attempt = fields.Selection([('1', 'First'), ('2', 'Second'), ('3', 'Third')], string="No of Exam Attempt", required=True)

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_exam_id
        to ease window action definitions, and be backward compatible. """
        result = super(ExamAddSurvey, self).default_get(fields_vals)

        if not result.get('exam_id') and self.env.context.get('active_id'):
            result['exam_id'] = self.env.context.get('active_id')
            exam = self.env['op.exam'].browse(result['exam_id'])
            if exam.survey_id_2:
                exam_try = '3'
            elif exam.survey_id:
                exam_try = '2'
            else:
                exam_try = '1'
            result['exam_attempt'] = exam_try
        return result

    def add_question(self):
        if self.exam_attempt == '1':
            self.exam_id.write({
                'survey_id': self.survey_id.id,
                'session_code': self.survey_id.session_code,
                'session_link': self.survey_id.session_link,
            })
        elif self.exam_attempt == '2':
            self.exam_id.write({
                'survey_id_2': self.survey_id.id,
                'session_code_2': self.survey_id.session_code,
                'session_link_2': self.survey_id.session_link,
            })
        else:
            self.exam_id.write({
                'survey_id_3': self.survey_id.id,
                'session_code_3': self.survey_id.session_code,
                'session_link_3': self.survey_id.session_link,
            })
