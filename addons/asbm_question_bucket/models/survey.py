# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'
    _description = 'Course Customization'

    course_id = fields.Many2one('op.course', 'Course')
    subject_id = fields.Many2one('op.subject', string='Subject', domain="[('course_id', '=', course_id)]")
    question_level = fields.Selection([('hard', 'Hard'), ('moderate', 'Moderate'), ('easy', 'Easy')], string="Question Type", default='hard')
