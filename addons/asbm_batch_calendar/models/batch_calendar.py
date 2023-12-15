# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, time


class Batchcalendar(models.Model):
    _name = 'batch.calendar'
    _inherit = "mail.thread"
    _description = 'Batch calendar'

    @api.depends('course_category_id')
    def _set_name(self):
        for rec in self:
            if rec.course_category_id:
                rec.name = rec.course_category_id.name
            else:
                rec.name = False

    @api.depends('course_category_id')
    def onchange_course_category_id(self):
        for rec in self:
            rec.calendar_lines = False
            for data in rec.course_ids:
                batches = self.env['op.batch'].search([('course_id', '=', data.id)])
                data = []
                for batch in batches:
                    vals = {'calendar_id': rec.id,
                            'batch_id': batch.id,
                            'batch_exam_month': batch.normal_batch_month_id.id,
                            'emergency_exam_month': batch.emergency_batch_month_id.id,
                            'super_emergency_exam_month': batch.super_batch_month_id.id,
                            }
                    data.append((0, 0, vals))
                rec.calendar_lines = data
            rec.is_compute = True


    @api.onchange('course_category_id')
    def onchane_course_category_id(self):
        for data in self:
            data.course_ids = data.course_category_id.course_ids

    name = fields.Char('Name',compute=_set_name)
    course_category_id = fields.Many2one('course.category','Course Calender')
    course_ids = fields.Many2many('op.course','batch_calender_id')
    user_id = fields.Many2one('res.users','User',default=lambda self: self.env.user)
    date = fields.Date('Date',default=date.today())
    company_id = fields.Many2one('res.company', 'Company',default=lambda self: self.env.company)
    is_compute = fields.Boolean(compute='onchange_course_category_id')
    calendar_lines = fields.One2many('batch.calendar.lines','calendar_id')






class BatchcalendarLines(models.Model):
    _name = 'batch.calendar.lines'
    _description = 'Batch calendar Lines'


    def action_open_batch_form(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('openeducat_core.act_open_op_batch_view')
        action.update({
            'view_mode': 'form',
            'view_id': self.env.ref('openeducat_core.view_op_batch_form').id,
            'views': [(self.env.ref('openeducat_core.view_op_batch_form').id, 'form')],
            'res_id': self.batch_id.id,
        })
        return action

    calendar_id = fields.Many2one('batch.calendar')
    batch_id = fields.Many2one('op.batch','Batch')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    pdc_date = fields.Date('PDC Dead Date')
    bach_type = fields.Selection([('normal','Normal'),('emergency','Emergency'),('super_emergency','Super Emergency')],string="Batch Type",default='normal')
    batch_exam_month = fields.Many2one('batch.exam.month','Batch Exam Month',related='batch_id.normal_batch_month_id')
    emergency_exam_month = fields.Many2one('batch.exam.month','Emergency Batch Exam Month',related='batch_id.emergency_batch_month_id')
    super_emergency_exam_month = fields.Many2one('batch.exam.month','Super Emergency Batch Exam Month',related='batch_id.super_batch_month_id')
    state = fields.Selection(related='batch_id.state')





