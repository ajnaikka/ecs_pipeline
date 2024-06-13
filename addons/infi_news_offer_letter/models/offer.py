from odoo import models, fields, api, exceptions, _
import base64
import pdfkit


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'
    is_amend = fields.Boolean(string='Is amend')

    def action_offer_letter(self):
        recuritment = self.env['offer.letter'].create({
            'recruitment_id': self.id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offer Letter',
            'view_mode': 'form',
            'res_model': 'offer.letter',  # Corrected model name
            'target': 'current',
            'res_id': recuritment.id,
        }

    def smart_offer_letter(self):
        self.ensure_one()
        # Find all records related to the current record's employee(s) where is_holiday is True
        all_child = self.env['offer.letter'].with_context(active_test=False).search([
            ('recruitment_id', '=', self.id)
        ])

        # Prepare the action for displaying the HR attendances
        action = self.env["ir.actions.act_window"]._for_xml_id("infi_news_offer_letter.offer_letter_form_action")
        action['domain'] = [('id', 'in', all_child.ids)]
        action['context'] = {'search_default_recruitment_id': self.id}

        return action

    def send_amend(self):
        self.is_amend = True
        for record in self:
            # Create email template
            template_values = {
                'name': 'Offer letter',
                'subject': 'Offer letter',
                'body_html': """
                        <div class="page">
                            <div class="oe_structure"/>
                                <div style="text-align: center;color:blue;">
                                    <h1 style="text-decoration: underline;">Offer Letter</h1>
                                </div>
                                <br/>
                                <br/>
                                <br/>
                                <p>Dear %s,</p>
                                <br/>
                                <br/>
                                <br/>
        
                                <p>We are pleased to offer you the position of %s at our company with a CTC of %s .We look forward to your valuable contributions to our team. Please sign below to accept this offer.</p>
                                <br/>
                                <br/>
                                <br/>
                                <p>___________________________</p>
                                <p>Signature</p>
                        </div>
                    """% (
                self.partner_name,self.name,self.salary_proposed),
                'model_id': self.env.ref('hr_recruitment.model_hr_applicant').id,  # Update with actual model reference
            }
            email_template = self.env['mail.template'].create(template_values)
            mail_template = self.env['mail.template'].browse(email_template.id)

            # Render the email content
            rendered_message = mail_template.body_html

            # Create and send the email with attachment
            pdf_data = pdfkit.from_string(rendered_message, False)

            # Encode the PDF data
            pdf_data_base64 = base64.b64encode(pdf_data)

            # Create attachment data for the PDF
            attachment_data = {
                'name': 'Release_checklist.pdf',
                'datas': pdf_data_base64,
                'res_model': 'mail.mail',
                'res_id': 0,
            }
            email_address = self.email_cc

            # Create and send the email with attachment
            mail = self.env['mail.mail'].create({
                'subject': mail_template.subject,
                'body_html': rendered_message,
                'email_from': self.env.user.email,
                'email_to': email_address,
                'attachment_ids': [(0, 0, attachment_data)],
            })
            mail.send()


    def resend_amend(self):
        for record in self:
            # Create email template
            template_values = {
                'name': 'Offer letter',
                'subject': 'Offer letter',
                'body_html': """
                        <div class="page">
                            <div class="oe_structure"/>
                                <div style="text-align: center;color:blue;">
                                    <h1 style="text-decoration: underline;">Offer Letter</h1>
                                </div>
                                <br/>
                                <br/>
                                <br/>
                                <p>Dear %s,</p>
                                <br/>
                                <br/>
                                <br/>
                                <p>We are pleased to offer you the position of %s at our company with a CTC of %s .We look forward to your valuable contributions to our team. Please sign below to accept this offer.</p>
                                <br/>
                                <br/>
                                <br/>
                                <p>___________________________</p>
                                <p>Signature</p>
                                <p>Date</p>
                        </div>
                    """ % (
                    self.partner_name, self.name, self.salary_proposed),
                'model_id': self.env.ref('hr_recruitment.model_hr_applicant').id,  # Update with actual model reference
            }
            email_template = self.env['mail.template'].create(template_values)
            mail_template = self.env['mail.template'].browse(email_template.id)

            # Render the email content
            rendered_message = mail_template.body_html

            # Create and send the email with attachment
            pdf_data = pdfkit.from_string(rendered_message, False)

            # Encode the PDF data
            pdf_data_base64 = base64.b64encode(pdf_data)

            # Create attachment data for the PDF
            attachment_data = {
                'name': 'Release_checklist.pdf',
                'datas': pdf_data_base64,
                'res_model': 'mail.mail',
                'res_id': 0,
            }
            email_address = self.email_cc
            # Create and send the email with attachment
            mail = self.env['mail.mail'].create({
                'subject': mail_template.subject,
                'body_html': rendered_message,
                'email_from': self.env.user.email,
                'email_to': email_address,
                'attachment_ids': [(0, 0, attachment_data)],
            })
            mail.send()

class OfferLetterForm(models.Model):
    _name = 'offer.letter'
    _description = 'Exit Form'
    _order = 'id desc'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name= fields.Char(string='Name')
    email = fields.Char(string='Email')
    position = fields.Char(string='Position')
    date_joining = fields.Date(string='Joining Date')
    department = fields.Char(string='Department')
    location = fields.Char(string='Current Location')
    basic = fields.Float(string="Basic")
    dra = fields.Float(string="DRA")
    hra = fields.Float(string="HRA")
    conveyance = fields.Float(string="Conveyance")
    other_allownance = fields.Float(string="Other Allowance")
    lpf = fields.Float(string="EPF")
    lwf = fields.Float(string="LWF")
    esi = fields.Float(string="ESI")
    company_id = fields.Many2one('res.company', string='Company',
                                  readonly=True,
                                 default=lambda self: self.env.company)
    recruitment_id = fields.Many2one('hr.applicant', string='Recruitment')
    date = fields.Date(
        string='Create Date',
        default=lambda self: fields.Date.today()
    )

    def send_offer(self):
        template = self.env.ref('infi_news_offer_letter.candidate_offer_letter_template')
        email_addresses = [record.email for record in self if record.email]

        compose_ctx = {
            'default_model': 'certificate.generations',
            'default_res_ids': self.ids,
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_use_template': bool(template.id),
            'default_email_from': self.env.user.email,  # Assuming the sender's email is the current user's email
            'default_email_to': ','.join(email_addresses)
        }

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









