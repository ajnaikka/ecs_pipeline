from _weakref import ref

from odoo import models, fields, api, tools


class QuotationApprovalWizard(models.TransientModel):
    _name = 'quotation.approval'
    _inherit = ['mail.thread']
    _rec_name = 'user_id'

    # send_to = fields.Many2many('res.users', string="Send To")
    send_to = fields.Many2many('res.users', string="Send To", domain="[('groups_id', 'in', group_purchase_director)]")

    group_purchase_director = fields.Many2one('res.groups', default=lambda self: self.env.ref('purchase_order_approval.group_purchase_director', raise_if_not_found=False))

    user_id = fields.Many2one('res.users', 'Users', default=lambda self: self.env.user)
    mail_to = fields.Selection([
        ('work', 'Work'),
    ], string='Email', help="""Email used to send the Quotation Approval.
                        - Work takes the email defined in "work email"
                        - Private takes the email defined in Private Information
                        - If the selected email is not defined, the available one will be used.""", default='work')

    subject = fields.Char(string="Subject", required=True, default='Quotation Approval')
    message = fields.Html("Message")
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments 1")
    attachment_sec_ids = fields.Many2many('ir.attachment', 'quotation_approval_attachment_rel_2', 'wizard_id', 'attachment_id', string="Attachments 2")
    email = fields.Char(string='Recipient Email')


    def to_cc(self):
        for wizard in self:
            attachment_ids = [attachment.id for attachment in wizard.attachment_ids]
            attachment_sec_ids = [attachment.id for attachment in wizard.attachment_sec_ids]

            att = wizard.env['ir.attachment'].browse(attachment_ids)
            att.write({'public': True})

            att_2 = wizard.env['ir.attachment'].browse(attachment_sec_ids)
            att_2.write({'public': True})

            email_to_list = [employee.work_email for employee in wizard.send_to]

            mail_values = {
                'author_id': wizard.env.user.partner_id.id,
                'auto_delete': True,
                'body_html': wizard.message,
                'email_from': wizard.env.user.email_formatted,
                'email_to': ', '.join(email_to_list),
                'subject': wizard.subject,
                'attachment_ids': [(6, 0, attachment_ids)],
                'attachment_sec_ids': [(6, 0, attachment_sec_ids)],
            }

            mail = wizard.env['mail.mail'].sudo().create(mail_values)
            mail.send()

    def button_send_quotation_approval(self):
        for wizard in self:
            attachment_ids = [attachment.id for attachment in wizard.attachment_ids]
            attachment_sec_ids = [attachment.id for attachment in wizard.attachment_sec_ids]

            att = wizard.env['ir.attachment'].browse(attachment_ids + attachment_sec_ids)
            att.write({'public': True})

            email_address = wizard.email

            # Combine both sets of attachments into a single list
            all_attachment_ids = attachment_ids + attachment_sec_ids

            # Email with both primary and secondary attachments
            mail_values = {
                'author_id': wizard.env.user.partner_id.id,
                'auto_delete': True,
                'body_html': wizard.message,
                'email_from': wizard.env.user.email_formatted,
                'email_to': email_address,
                'subject': wizard.subject,
                'attachment_ids': [(6, 0, all_attachment_ids)],
            }

            mail = wizard.env['mail.mail'].sudo().create(mail_values)
            mail.send()

    # @api.depends('send_to', 'mail_to')
    # def _compute_mail_displayed(self):
    #     for wizard in self:
    #         if wizard.send_to:
    #             wizard.mail_displayed = wizard.send_to[0].private_email if wizard.mail_to == 'private' else \
    #                 wizard.send_to[0].work_email
    #         else:
    #             wizard.mail_displayed = False