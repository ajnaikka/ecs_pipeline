# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import datetime


class OpResultTemplate(models.Model):
    _inherit = "op.result.template"

    created_from_exam_id = fields.Many2one('op.exam', string="Created From", help="Result Template created from which exam record", copy=False)
    student_id = fields.Many2one('op.student', string="Student", required=True)

    @api.constrains('exam_session_id', 'student_id')
    def _check_exam_session(self):
        for record in self:
            for exam in record.exam_session_id.exam_ids.filtered(lambda l: record.student_id.id in l.attendees_line.student_id.ids and l.state not in ['result_updated', 'done', 'cancel']):
                if exam.state != 'held':
                    raise ValidationError(_('All subject exam of selected student should be in held state.'))

    def generate_result(self):
        for record in self:
            marksheet_reg_id = self.env['op.marksheet.register'].create({
                'name': 'Mark Sheet for %s - %s' % (record.exam_session_id.name, record.student_id.name),
                'exam_session_id': record.exam_session_id.id,
                'generated_date': self.result_date,
                'generated_by': self.env.uid,
                'state': 'draft',
                'result_template_id': record.id
            })
            student_dict = {}
            for exam in record.exam_session_id.exam_ids.filtered(lambda l: record.student_id.id in l.attendees_line.student_id.ids and l.op_result_template_id.id == record.id):
                for attendee in exam.attendees_line.filtered(lambda l: l.student_id.id == record.student_id.id):
                    result_line_id = self.env['op.result.line'].create({
                        'student_id': attendee.student_id.id,
                        'exam_id': exam.id,
                        'marks': str(attendee.marks and attendee.marks or 0),
                    })
                    if attendee.student_id.id not in student_dict:
                        student_dict[attendee.student_id.id] = []
                    student_dict[attendee.student_id.id].append(result_line_id)
            for student in student_dict:
                marksheet_line_id = self.env['op.marksheet.line'].create({
                    'student_id': student,
                    'marksheet_reg_id': marksheet_reg_id.id,
                })
                for result_line in student_dict[student]:
                    result_line.marksheet_line_id = marksheet_line_id
            record.state = 'result_generated'


class OpExam(models.Model):
    _inherit = "op.exam"

    evaluation_type = fields.Selection(
        related='session_id.evaluation_type', string="Evaluation Type",
        store=True, tracking=True)
    grade_ids = fields.Many2many(
        'op.grade.configuration', string='Grade Configuration')
    op_result_template_id = fields.Many2one('op.result.template', string="Result Template")

    def act_result_updated(self):
        if self.evaluation_type == 'grade' and not self.grade_ids:
            raise UserError(_("Please provide grades"))
        student_id = self.attendees_line.student_id.ids[0]
        student = self.env['op.student'].browse(student_id)
        grade_ids = [(4, grade.id) for grade in self.grade_ids]
        if self.session_id.course_type == 'normal':
            days = self.session_id.batch_id.result_duration
        elif self.session_id.course_type == 'emergency':
            days = self.session_id.batch_id.emergency_result_duration
        else:
            days = self.session_id.batch_id.super_result_duration
        result = self.env['op.result.template'].create({
            'exam_session_id': self.session_id.id,
            'result_date': self.end_time.date() + datetime.timedelta(days=days),
            'name': self.session_id.name + " - " + student.name,
            'grade_ids': grade_ids,
            'student_id': student_id,
            'created_from_exam_id': self.id,
        })
        self.write({
            'state': 'done',
            'op_result_template_id': result.id,
        })
        for exam in self.session_id.exam_ids.filtered(
                lambda l: student_id in l.attendees_line.student_id.ids and l.state not in ['result_updated', 'done', 'cancel']):
            exam.write({
                'state': 'done',
                'op_result_template_id': result.id,
            })


class OpMarksheetRegister(models.Model):
    _inherit = "op.marksheet.register"

    exam_result_status = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string='Exam Result',
                              compute='_compute_exam_result_status', store=True)

    @api.depends('total_failed', 'total_pass')
    def _compute_exam_result_status(self):
        for record in self:
            record.exam_result_status = 'pass'
            if record.total_failed > 0:
                record.exam_result_status = 'fail'