# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, time
import calendar


from odoo import models, fields, api


class OpBatch(models.Model):
    _inherit = 'op.batch'
    _description = 'Batch Customization'

    normal_batch_month_id = fields.Many2one('batch.exam.month','Exam Month(Normal)')
    emergency_batch_month_id = fields.Many2one('batch.exam.month','Exam Month(Emergency)')
    super_batch_month_id = fields.Many2one('batch.exam.month','Exam Month(Super Emergency)')

    course_duration = fields.Integer('Normal Course Duration(Days)',default=90)
    emergency_course_duration = fields.Integer('Emergency Course Duration(Days)',default=60)
    super_course_duration = fields.Integer('Super Emergency Course Duration(Days)',default=30)

    exam_duration = fields.Integer('Normal Exam Duration(Days)')
    emergency_exam_duration = fields.Integer('Emergency Exam Duration(Days)')
    super_exam_duration = fields.Integer('Super Exam Duration(Days)')

    result_duration = fields.Integer('Normal Result Duration(Days)')
    emergency_result_duration = fields.Integer('Emergency Result Duration(Days)')
    super_result_duration = fields.Integer('Super Result Duration(Days)')

    certificate_days = fields.Integer('Normal Certificate Duration(Days)')
    emergency_certificate_days = fields.Integer('Emergency Certificate Duration(Days)')
    super_certificate_days = fields.Integer('Super Certificate Duration(Days)')

    state = fields.Selection([('draft','Draft'),('confirm','Confirmed')],default='draft')

    exam_session_count = fields.Integer(compute='_get_session_count', string='Exam Session Count', copy=False, default=0)

    def _get_session_count(self):
        for rec in self:
            sessions = self.env['op.exam.session'].search([('batch_id','=',rec.id)])
            rec.exam_session_count = len(sessions)

    def action_view_sessions(self):
        return {
            'name': 'Exam Sessions',
            'domain': [('batch_id', 'in', [self.id])],
            'context': {'search_default_batch_id': self.id},
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'op.exam.session',
            'type': 'ir.actions.act_window',
        }

    def action_confirm(self):
        for data in self:

            normal_month = int(data.normal_batch_month_id.month)
            normal_year = int(data.normal_batch_month_id.year)
            normal_start_date =  datetime(normal_year, normal_month, 1)
            normal_res = calendar.monthrange(normal_start_date.year, normal_start_date.month)
            normal_day = normal_res[1]
            normal_end_date = normal_start_date + relativedelta(days=normal_day-1)

            emergency_month = int(data.emergency_batch_month_id.month)
            emergency_year = int(data.emergency_batch_month_id.year)
            emergency_start_date =  datetime(emergency_year, emergency_month, 1)
            emergency_res = calendar.monthrange(emergency_start_date.year, emergency_start_date.month)
            emergency_day = emergency_res[1]
            emergency_end_date = normal_start_date + relativedelta(days=emergency_day-1)

            super_month = int(data.super_batch_month_id.month)
            super_year = int(data.super_batch_month_id.year)
            super_start_date =  datetime(super_year, super_month, 1)
            super_res = calendar.monthrange(super_start_date.year, super_start_date.month)
            super_day = super_res[1]
            super_end_date = super_start_date + relativedelta(days=super_day-1)

            exam_type = self.env['op.exam.type'].search([('name','=','Online')],limit=1)
            normal_exam = {'name':data.course_id.name +'-'+data.name+'- (Normal)',
                           'exam_code':data.code+'-'+str(normal_year)+'-'+str(normal_month),
                           'start_date':normal_start_date,
                           'end_date':normal_end_date,
                           'course_id':data.course_id.id,
                           'batch_id':data.id,
                           'course_type':'normal',
                           'exam_type':exam_type.id,
                           'evaluation_type':'normal',
                           }
            emergency_exam = {'name':data.course_id.name +'-'+data.name+'- (Emergency)',
                           'exam_code':data.code+'-'+str(emergency_year)+'-'+str(emergency_month),
                           'start_date':emergency_start_date,
                           'end_date':emergency_end_date,
                           'course_id':data.course_id.id,
                           'batch_id':data.id,
                            'course_type': 'emergency',
                           'exam_type':exam_type.id,
                           'evaluation_type':'normal',
                           }
            super_exam = {'name':data.course_id.name +'-'+data.name+'- (Super Emergency)',
                           'exam_code':data.code+'-'+str(super_year)+'-'+str(super_month),
                           'start_date':super_start_date,
                           'end_date':super_end_date,
                           'course_id':data.course_id.id,
                           'batch_id':data.id,
                           'course_type': 'super',
                           'exam_type':exam_type.id,
                           'evaluation_type':'normal',
                           }
            normal_session = self.env['op.exam.session'].create(normal_exam)
            emergency_session = self.env['op.exam.session'].create(emergency_exam)
            super_session = self.env['op.exam.session'].create(super_exam)
            data.state = 'confirm'