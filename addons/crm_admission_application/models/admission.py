# -*- coding: utf-8 -*-


from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class OpAdmission(models.Model):
    _inherit = "op.admission"

    course_type = fields.Selection([('normal', 'Normal'), ('emergency', 'Emergency'), ('super', 'Super Emergency')],
                                   string="Course Type")
    lead_id = fields.Many2one('crm.lead', string="Lead/Opportunity")

    def view_student_fees_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fees Details',
            'view_mode': 'tree',
            'res_model': 'op.student.fees.details',
            'context': {'create': False},
            'domain': [('op_admission_id', '=', self.id)],
            'target': 'current',
        }


class OpStudentCourse(models.Model):
    _inherit = "op.student.course"

    op_admission_id = fields.Many2one('op.admission', string="Admission Ref")
