# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class LeadAdmissionApplication(models.TransientModel):
    _name = 'crm.lead.admission.application'
    _description = 'Generate Application From opportunity'

    lead_id = fields.Many2one('crm.lead', string="Associated Lead", required=True)
    register_id = fields.Many2one('op.admission.register', 'Admission Register', required=True,
                                  domain="[('state', 'in', ['application','admission'])]")
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    application_date = fields.Datetime('Application Date', required=True, default=lambda self: fields.Datetime.now())
    student_id = fields.Many2one('op.student', 'Student')
    birth_date = fields.Date('Birth Date', required=True, related='student_id.birth_date', readonly=False)
    fees_term_id = fields.Many2one('op.fees.terms', 'Fees Term', required=True)
    fees_start_date = fields.Date('Fees Start Date', required=True)
    fees = fields.Float('Fees', required=True)
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)
    course_type = fields.Selection([('normal', 'Normal'), ('emergency', 'Emergency'), ('super', 'Super Emergency')],
                                   string="Batch Type", required=True)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))
            elif record:
                today_date = fields.Date.today()
                day = (today_date - record.birth_date).days
                years = day // 365
                if years < self.register_id.minimum_age_criteria:
                    raise ValidationError(_(
                        "Not Eligible for Admission minimum required age is : %s " % self.register_id.minimum_age_criteria))

    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        for rec in self:
            start_date = fields.Date.from_string(rec.register_id.start_date)
            end_date = fields.Date.from_string(rec.register_id.end_date)
            application_date = fields.Date.from_string(rec.application_date)
            if application_date < start_date or application_date > end_date:
                raise ValidationError(_(
                    "Application Date should be between Start Date & End Date of Admission Register."))

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_lead_id
        to ease window action definitions, and be backward compatible. """
        result = super(LeadAdmissionApplication, self).default_get(fields_vals)

        if not result.get('lead_id') and self.env.context.get('active_id'):
            result['lead_id'] = self.env.context.get('active_id')
        if result.get('lead_id'):
            lead = self.env['crm.lead'].browse(result['lead_id'])
            result['course_id'] = lead.admission_register.course_id.id
            result['register_id'] = lead.admission_register.id
            result['student_id'] = lead.student_id.id
            result['batch_id'] = lead.batch_id.id
            result['course_type'] = lead.batch_type
            result['fees_term_id'] = lead.admission_register.course_id.fees_term_id.id
            result['discount'] = lead.admission_register.course_id.fees_term_id.discount or 0
            result['fees'] = lead.total_course_fee
        return result

    def action_generate_application(self):
        sd = self.lead_id.student_id
        name = str(sd.first_name) + " " + str(sd.last_name) \
            if not sd.middle_name else str(sd.first_name) + " " + str(sd.middle_name) + " " + str(sd.last_name)
        admission_data = {
            'is_student': True,
            'student_id': sd.id,
            'title': sd.title and sd.title.id or False,
            'first_name': sd.first_name,
            'middle_name': sd.middle_name,
            'last_name': sd.last_name,
            'birth_date': sd.birth_date,
            'gender': sd.gender,
            'image': sd.image_1920 or False,
            'street': sd.street or False,
            'street2': sd.street2 or False,
            'phone': sd.phone or False,
            'mobile': sd.mobile or False,
            'email': sd.email or False,
            'zip': sd.zip or False,
            'city': sd.city or False,
            'country_id': sd.country_id and sd.country_id.id or False,
            'state_id': sd.state_id and sd.state_id.id or False,
            'partner_id': sd.partner_id and sd.partner_id.id or False,
            'name': name,
            'register_id': self.register_id.id,
            'course_id': self.course_id.id,
            'fees': self.fees,
            'discount': self.discount,
            'company_id': self.lead_id.company_id.id,
            'fees_term_id': self.fees_term_id.id,
            'batch_id': self.batch_id.id,
            'application_date': self.application_date,
            'fees_start_date': self.fees_start_date,
            'course_type': self.course_type,
            'lead_id': self.lead_id.id,
        }
        admission = self.env['op.admission'].create(admission_data)
        sd.write({
            'course_detail_ids': [[0, False, {
                'course_id':
                    self.course_id and self.course_id.id or False,
                'batch_id':
                    self.batch_id and self.batch_id.id or False,
                'fees_term_id': self.fees_term_id.id,
                'fees_start_date': self.fees_start_date,
                'op_admission_id': admission.id,
                'subject_ids': [(4, i) for i in self.course_id.subject_ids.ids],
            }]],
        })
        if self.fees_term_id.fees_terms in ['fixed_days', 'fixed_date']:
            val = []
            product_id = self.register_id.product_id.id
            for line in self.fees_term_id.line_ids:
                no_days = line.due_days
                per_amount = line.value
                amount = (per_amount * self.fees) / 100
                dict_val = {
                    'fees_line_id': line.id,
                    'amount': amount,
                    'fees_factor': per_amount,
                    'product_id': product_id,
                    'discount': self.discount,
                    'state': 'draft',
                    'course_id': self.course_id and self.course_id.id or False,
                    'batch_id': self.batch_id and self.batch_id.id or False,
                    'op_admission_id': admission.id,
                    'lead_id': self.lead_id.id,
                }
                if line.due_date:
                    date = line.due_date
                    dict_val.update({
                        'date': date
                    })
                elif self.fees_start_date:
                    date = self.fees_start_date + relativedelta(
                        days=no_days)
                    dict_val.update({
                        'date': date,
                    })
                else:
                    date_now = (datetime.today() + relativedelta(
                        days=no_days)).date()
                    dict_val.update({
                        'date': date_now,
                    })
                val.append([0, False, dict_val])
            sd.write({
                'fees_detail_ids': val
            })
        self.lead_id.op_admission_id = admission.id
