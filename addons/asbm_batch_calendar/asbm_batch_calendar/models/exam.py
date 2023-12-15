# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, time


from odoo import models, fields, api


class ExamSession(models.Model):
    _inherit = 'op.exam.session'
    _description = 'Exam Session'

    course_type = fields.Selection([('normal','Normal'),('emergency','Emergency'),('super','Super Emergency')])




