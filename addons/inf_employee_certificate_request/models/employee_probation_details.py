from odoo import models, fields,api,_


class EmployeeProbationDetails(models.Model):
    _name = 'employee.probation.details'
    _description = 'Employee Probation Details'

    employee_id = fields.Many2one('hr.employee', string="Concerned Employee", required=True)
    date = fields.Date(string='Date')
    user_ids = fields.Many2many('res.users', string='Users')
    company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.company)

    attachment_ids = fields.Many2many('ir.attachment')


class EmployeeCertificate(models.Model):
    _name = 'employee.certificate.details'
    _description = 'Employee Certificate Details'


    send_to = fields.Many2one('hr.employee', string="Send To")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    mail_displayed = fields.Char(compute='_compute_mail_displayed',store=True,string="Email")
    attachment_ids = fields.Many2many('ir.attachment')
    user_id = fields.Many2one('res.users', string='Users')
    date = fields.Date(string="Date")


    @api.depends('send_to')
    def _compute_mail_displayed(self):
        for wizard in self:
            if wizard.send_to:
                wizard.mail_displayed = wizard.send_to.private_email or wizard.send_to.work_email
            else:
                wizard.mail_displayed = False

    def action_generate_certificate(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Certificate Generations',
            'res_model': 'certificate.generations',
            'view_mode': 'form',
            'target': 'current',
            'context':{
                'default_employee_id':self.user_id.employee_id.id,
                'date':self.date,
            }
        }




class CertificateGeneration(models.Model):
    _name = 'certificate.generations'
    _description = "Certificate Generation"
    _rec_name = "employee_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string="Employee")
    date = fields.Date(string="Date")
    purpos = fields.Char(string="Purpose")

    hr_manager_id = fields.Many2one('hr.employee', string="HR Manager", related='employee_id.hr_manager_id', store=True)
    hr_manager_signature = fields.Binary(string="HR Manager Signature", compute='_compute_hr_manager_signature')

    @api.depends('employee_id')
    def _compute_hr_manager_signature(self):
        for record in self:
            if record.employee_id:
                hr_manager_user = record.employee_id.hr_manager_id.user_id
                print("HR Manager User:", hr_manager_user)
                if hr_manager_user:
                    print("HR Manager Signature:", hr_manager_user.sign_signature)
                    record.hr_manager_signature = hr_manager_user.sign_signature
                else:
                    record.hr_manager_signature = False
            else:
                record.hr_manager_signature = False
                
    def action_send_mail(self):
        template = self.env.ref('inf_employee_certificate_request.employee_certificate_template')
        compose_ctx = dict(
            default_partner_ids=[self.employee_id.user_partner_id.id],
            default_model='certificate.generations',
            default_res_ids=self.ids,
            default_template_id=template.id,
            default_composition_mode='comment'
        )

        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificate Generation Mail'),
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': compose_ctx,
        }

