# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, time



class MarkSheetRegister(models.Model):
    _inherit = 'op.marksheet.register'
    _description = 'Mark Sheet Register'

    def action_validate(self):
        for data in self:
            certificate = self.env['course.certificate']
            lines = []
            result_tmpl = data.result_template_id.exam_session_id
            student_id = data.result_template_id.student_id
            student_code = data.result_template_id.student_id.gr_no
            course = data.result_template_id.exam_session_id.course_id
            name = str(student_code) if student_code else 'Certificate'
            name += '-'+str(student_id.name)
            batch = data.result_template_id.exam_session_id.batch_id
            course_type = data.result_template_id.exam_session_id.course_type
            percentage = data.marksheet_line[0].percentage if data.marksheet_line else 0
            month_year = False
            if course_type == 'normal':
                month_year = batch.normal_batch_month_id.id
            if course_type == 'emergency':
                month_year = batch.emergency_batch_month_id.id
            if course_type == 'super':
                month_year = batch.super_batch_month_id.id
            for rec in data.result_template_id.exam_session_id.exam_ids:
                vals = {'subject_id': rec.subject_id.id,
                        'subject_code': rec.subject_id.code,
                        'max_awarded':rec.attendees_line[0].marks,
                        'max_marks':rec.subject_id.total_marks,
                        'month_year':month_year,
                        }
                lines.append((0,0,vals))
            vals = {'name':name,
                    'date': date.today(),
                    'student_code': student_code,
                    'student_id': student_id.id,
                    'course_id': course.id,
                    'certificate_type': 'main',
                    'month_year': month_year,
                    'percentage': percentage,
                    'company_id': self.env.company.id,
                    'line_ids': lines,
                    }
            certificate.create(vals)
            data.state = 'validated'

