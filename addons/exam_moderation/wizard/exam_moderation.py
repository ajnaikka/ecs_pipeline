# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ExamModerationWizard(models.TransientModel):
    _name = 'exam.moderation.wizard'
    _description = 'Exam Moderation Wizard'

    exam_id = fields.Many2one(comodel_name='op.exam', string="Exam", required=True)
    marks = fields.Integer(string="Marks", required=True)
    passing_marks = fields.Integer(string="Passing Marks", required=True)
    total_marks = fields.Integer(string="Total Marks", required=True)

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_exam_id
        to ease window action definitions, and be backward compatible. """
        result = super(ExamModerationWizard, self).default_get(fields_vals)

        if not result.get('exam_id') and self.env.context.get('active_id'):
            result['exam_id'] = self.env.context.get('active_id')
            exam = self.env['op.exam'].browse(result['exam_id'])
            result['passing_marks'] = exam.min_marks
            result['total_marks'] = exam.total_marks
        return result

    @api.constrains('passing_marks', 'total_marks', 'marks')
    def check_marks_given(self):
        for record in self:
            if record.marks < record.passing_marks:
                raise UserError(_("Marks should be greater than passing marks"))
            if record.marks > record.total_marks:
                raise UserError(_("Marks should be less than total marks."))

    def action_moderate_exam(self):
        if not self.env.user.has_group('exam_moderation.group_exam_moderation_ah_approval'):
            raise ValidationError(_("You are not permitted to moderate the exam"))
        for line in self.exam_id.attendees_line:
            line.marks = self.marks
        self.exam_id.state = 'held'
        self.exam_id.moderation_exam_status = 'pass' if self.marks >= self.exam_id.min_marks else 'fail'
