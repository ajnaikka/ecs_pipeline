# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_qualification = fields.Char(string='Last Qualification')


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    # def _send_invoice(self):
    #     super()._send_invoice()
    #     email_template = self.env.ref('asbm_website_course_sale.email_template_invoice_paid_account_manager')
    #     for record in self:
    #         for invoice in record.invoice_ids.with_user(SUPERUSER_ID):
    #             users = invoice.company_id.payment_notification_users
    #             emails = set(r.email for r in users if r.email)
    #             email_values = {
    #                 'email_to': ','.join(emails)
    #             }
    #             email_template.send_mail(invoice.id, force_send=True, email_values=email_values)

    def _invoice_sale_orders(self):
        super()._invoice_sale_orders()
        email_template = self.env.ref('asbm_website_course_sale.email_template_invoice_paid_account_manager')
        for record in self:
            for invoice in record.invoice_ids.with_user(SUPERUSER_ID):
                users = invoice.company_id.payment_notification_users
                emails = set(r.email for r in users if r.email)
                email_values = {
                    'email_to': ','.join(emails)
                }
                email_template.send_mail(invoice.id, force_send=True, email_values=email_values)
                # invoice.message_post_with_template(
                #     int(email_template.id),
                #     email_layout_xmlid='mail.mail_notification_layout_with_responsible_signature',
                # )
