# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, time


from odoo import models, fields, api


class ExamSession(models.Model):
    _inherit = 'op.course'
    _description = 'Course Enhancement'

    course_category_id = fields.Many2one('course.category','Course Category')
    batch_calender_id = fields.Many2one('batch.calendar','Batch Calender')
    batch_id = fields.Many2one('op.batch','Batch')



