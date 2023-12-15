# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime
import psycopg2


class OpAdmission(models.Model):
    _inherit = "op.admission"

    exam_ids = fields.One2many('op.exam', 'admission_id', 'Exam(s)')
    enrollment_number = fields.Char(string="Enrollment Number", copy=False, readonly=True,
                                    default=lambda self: _('New'))

    def enroll_student(self):
        for record in self:
            if record.lead_id.bdh_verified is False:
                raise ValidationError(_("BDH verification is not completed."))
            if not record.admission_date:
                raise UserError(_("Please provide admission date"))
            if not record.course_type:
                raise UserError(_("Please select course type"))
            if not record.phone or not record.mobile:
                raise UserError(
                    _('Please fill in the mobile number'))
            if record.register_id.max_count:
                total_admission = self.env['op.admission'].search_count(
                    [('register_id', '=', record.register_id.id),
                     ('state', '=', 'done')])
                if not total_admission < record.register_id.max_count:
                    msg = 'Max Admission In Admission Register :- (%s)' % (
                        record.register_id.max_count)
                    raise ValidationError(_(msg))
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
            min_time = datetime.datetime.min.time()
            max_time = datetime.time(23, 59, 59)
            for subject in record.course_id.subject_ids:
                exam = self.env['op.exam'].create({
                    'session_id': exam_session.id,
                    'subject_id': subject.id,
                    'name': record.course_id.name + " - " + subject.name,
                    'exam_code': record.application_number + " - " + record.course_id.code + " - " + subject.code,
                    'start_time': datetime.datetime.combine(exam_date, min_time),
                    'end_time': datetime.datetime.combine(exam_date, max_time),
                    'total_marks': int(subject.total_marks),
                    'min_marks': int(subject.passing_marks),
                    'admission_id': record.id,
                    'exam_date': exam_date,
                    'attendees_line': [(0, 0, {
                        'student_id': record.student_id.id,
                        'course_id': record.course_id.id,
                        'batch_id': record.batch_id.id,
                        'status': 'present',
                    })]
                })

            record.write({
                'nbr': 1,
                'state': 'done',
                'is_student': True,
                'enrollment_number': self.env['ir.sequence'].next_by_code('student.enrollment',
                                                                          sequence_date=record.admission_date),
            })
            student_course_details = self.env['op.student.course'].search([('op_admission_id', '=', record.id)])
            student_course_details.roll_number = record.enrollment_number
            reg_id = self.env['op.subject.registration'].create({
                'student_id': record.student_id.id,
                'batch_id': record.batch_id.id,
                'course_id': record.course_id.id,
                'min_unit_load': record.course_id.min_unit_load or 0.0,
                'max_unit_load': record.course_id.max_unit_load or 0.0,
                'state': 'draft',
            })
            reg_id.get_subjects()
            template = self.env.ref('admission_students_enrollment.student_enrollment_email_template', False)
            try:
                template.sudo().send_mail(res_id=record.id, force_send=True)
            except psycopg2.errors.SerializationFailure as e:
                # Handle the SerializationFailure exception here
                print(f"Caught a SerializationFailure: {e}")

# class MailTemplate(models.Model):
#     "Templates for sending email"
#     _inherit = "mail.template"
#
#     def send_mail(self, res_id, force_send=False, raise_exception=False, email_values=None,
#                   email_layout_xmlid=False):
#         try:
#             super(MailTemplate, self).send_mail()
#         except psycopg2.errors.SerializationFailure as e:
#             # Handle the SerializationFailure exception here
#             print(f"Caught a SerializationFailure: {e}")



class OpExam(models.Model):
    _inherit = "op.exam"

    admission_id = fields.Many2one('op.admission', 'Admission')
    exam_date = fields.Date(string='Exam Date')
