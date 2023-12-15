# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, time



class CourseCertificate(models.Model):
    _name = 'certificate.template'
    _description = 'Certificate Template'


    # @api.depends('student_id')
    # def _compute_student_code(self):
    #     for data in self:
    #         admission = self.env['op.admission'].search([('course_id','=',data.course_id.id),('student_id','=',data.student_id.id)],limit=1)
    #         data.student_code = admission.enrollment_number

    name = fields.Char(index=True, default_export_compatible=True)
    date = fields.Date('Date',default=date.today())
    certificate_type = fields.Selection([('main','Main Certificate'),('marksheet','Mark Sheet'),('consolidated','Consolidated Sheet')],'Certificate Type')
    course_id = fields.Many2one('op.course','Course')
    company_id = fields.Many2one('res.company', 'Company',default=lambda self: self.env.company)
    main_report_id = fields.Many2one('ir.actions.report', 'Main Report Template',
                                     domain="[('model', '=', 'course.certificate')]")
    mark_sheet_report_id = fields.Many2one('ir.actions.report', 'Mark Sheet Report Template',
                                           domain="[('model', '=', 'course.certificate')]")
    consolidate_report_id = fields.Many2one('ir.actions.report', 'Consolidate Report Template',
                                            domain="[('model', '=', 'course.certificate')]")
    main_certificate = fields.Boolean('Main Certificate')
    mark_sheet = fields.Boolean('Mark Sheet')
    consolidate_sheet = fields.Boolean('Consolidate Sheet')

