# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime
from odoo.exceptions import ValidationError, UserError


class ExamRegister(models.Model):
    _name = 'exam.register'
    _inherit = "mail.thread"
    _description = 'Exam Register'

    session_id = fields.Many2one(comodel_name='op.exam.session', string='Exam Session', required=True)
    name = fields.Char(string='Exam Register Reference', copy=False, readonly=True, required=True, default=lambda self: _('New'))
    course_id = fields.Many2one(comodel_name='op.course', related='session_id.course_id', store=True, readonly=True)
    admission_id = fields.Many2one(comodel_name='op.admission', string='Admission', required=True)
    student_id = fields.Many2one(comodel_name='op.student', string='Student', required=True)
    exam_ids = fields.One2many(comodel_name='op.exam', inverse_name='exam_register_id', string='Exams')
    exam_date = fields.Date(string='Exam Date')
    state = fields.Selection(
        [('draft', 'Draft'), ('schedule', 'Scheduled'), ('question_added', 'Question Added')], string='State',
        readonly=True, default='draft', tracking=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    exam_status = fields.Selection([
        ('not_done', 'Not Done'),
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ], string='Status', compute='_compute_exam_status', store=True)

    @api.depends('exam_ids.exam_status')
    def _compute_exam_status(self):
        for record in self:
            record.exam_status = 'not_done'
            if any(record.exam_ids.filtered(lambda l: l.exam_status == 'fail')):
                record.exam_status = 'fail'
            if all(exam.exam_status == 'pass' for exam in record.exam_ids):
                record.exam_status = 'pass'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'exam.register') or _("New")

        return super().create(vals_list)

    def action_schedule_exam(self):
        for record in self:
            fee_details = self.env['op.student.fees.details'].search(
                [('op_admission_id', '=', record.admission_id.id)])
            if not fee_details:
                raise ValidationError(_("Please create fee details against admission"))
            if any(fee_details.filtered(lambda l: not l.invoice_id)):
                raise ValidationError(_("Please create invoice against all fee details"))
            if any(fee_details.filtered(lambda l: l.invoice_id.payment_state not in ['in_payment', 'paid'])):
                raise ValidationError(_("Make sure all exam fees has been fully paid"))
            record.state = 'schedule'
            for exam in record.exam_ids.filtered(lambda l: l.state == 'draft'):
                exam.state = 'schedule'

    def action_exam_add_survey(self):
        for exam in self.exam_ids.filtered(lambda l: l.state == 'schedule' and not l.survey_id):
            survey_id = self.env['survey.survey'].search([('question_level', '=', 'hard'), ('active', '=', True), ('subject_id', '=', exam.subject_id.id)], limit=1)
            if not survey_id:
                raise UserError(_("Please create survey"))
            exam.write({
                'survey_id': survey_id.id,
                'session_code': survey_id.session_code,
                'session_link': survey_id.session_link,
            })
        self.state = 'question_added'


class OpExam(models.Model):
    _inherit = "op.exam"

    exam_register_id = fields.Many2one(comodel_name='exam.register', string='Exam Register', ondelete="cascade")
    exam_status = fields.Selection([
        ('not_done', 'Not Done'),
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ], string='Status', compute='_compute_exam_status', store=True)

    @api.depends('moderation_exam_status', 'first_exam_status', 'second_exam_status', 'third_exam_status')
    def _compute_exam_status(self):
        for record in self:
            record.exam_status = 'not_done'
            if record.moderation_exam_status == 'pass' or record.first_exam_status == 'pass' or record.second_exam_status == 'pass' or record.third_exam_status == 'pass':
                record.exam_status = 'pass'
            if record.moderation_exam_status == 'fail' and record.first_exam_status == 'fail' and record.second_exam_status == 'fail' and record.third_exam_status == 'fail':
                record.exam_status = 'fail'

    def action_share_first_survey_id(self):
        if not self.survey_id.question_ids:
            raise UserError(_('You cannot send an invitation for an exam that has no questions.'))

        # Ensure that this survey has at least one section with question(s), if question layout is 'One page per section'.
        if self.survey_id.questions_layout == 'page_per_section':
            if not self.survey_id.page_ids:
                raise UserError(
                    _('You cannot send an invitation for a "One page per section" survey if the survey has no sections.'))
            if not self.survey_id.page_ids.mapped('question_ids'):
                raise UserError(
                    _('You cannot send an invitation for a "One page per section" survey if the survey only contains empty sections.'))

        if not self.survey_id.active:
            raise exceptions.UserError(_("You cannot send invitations for closed surveys."))

        template = self.env.ref('exam_scheduling.mail_template_student_input_invite', raise_if_not_found=False)
        exam_invite_obj = self.env['student.exam.invite'].create({
            'partner_ids': [(4, self.admission_id.partner_id.id)],
            'survey_id': self.survey_id.id,
            'exam_id': self.id,
            'exam_invite_attempt': '1',
            'template_id': template and template.id or False,
        })
        exam_invite_obj.action_invite()


class OpStudentCourse(models.Model):
    _inherit = "op.student.course"

    exam_register_id = fields.Many2one('exam.register', string="Exam register Ref")
    course_status = fields.Selection([
        ('not_done', 'Not Done'),
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ], string='Course Status', related='exam_register_id.exam_status', store=True)


class OpAdmission(models.Model):
    _inherit = "op.admission"

    def enroll_student(self):
        super().enroll_student()
        for record in self:
            exam_session = self.env['op.exam.session'].search([
                ('batch_id', '=', record.batch_id.id), ('course_type', '=', record.course_type),
                ('course_id', '=', record.course_id.id)])
            if record.course_type == 'normal':
                days = record.batch_id.course_duration + record.batch_id.exam_duration
            elif record.course_type == 'emergency':
                days = record.batch_id.emergency_course_duration + record.batch_id.emergency_exam_duration
            else:
                days = record.batch_id.super_course_duration + record.batch_id.super_exam_duration
            exam_date = record.admission_date + datetime.timedelta(days=days)
            if exam_date > exam_session.end_date:
                exam_date = exam_session.end_date
            exam_register = self.env['exam.register'].create({
                'session_id': exam_session.id,
                'course_id': exam_session.course_id.id,
                'admission_id': record.id,
                'student_id': record.student_id.id,
                'exam_ids': [(4, exam) for exam in record.exam_ids.ids],
                'exam_date': exam_date,
            })
            student_course_details = self.env['op.student.course'].search([('op_admission_id', '=', record.id)])
            student_course_details.exam_register_id = exam_register.id
