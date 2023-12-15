# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import email_normalize
from odoo.exceptions import UserError, ValidationError


class Lead(models.Model):
    _inherit = "crm.lead"

    partner_portal_user = fields.Many2one('res.users', string="Customer User")
    partner_portal_user_state = fields.Selection(related='partner_portal_user.state', string='Student Log in Status')
    portal_email_state = fields.Selection([
        ('ok', 'Valid'),
        ('not_ok', 'Invalid'),
        ('exist', 'Already Registered')],
        string='Status', compute='_compute_portal_email_state', store=True)
    application_status = fields.Selection([
        ('sent', 'Sent'),
        ('not_send', 'Not Send'),
        ('submitted', 'Submitted')],
        string='Application Status', default='not_send', store=True)

    def _find_matching_partner(self, email_only=False):
        """ Try to find a matching partner with available information on the
        lead, using notably customer's name, email, ...

        :param email_only: Only find a matching based on the email. To use
            for automatic process where ilike based on name can be too dangerous
        :return: partner browse record
        """
        self.ensure_one()
        partner = self.partner_id

        if not partner and self.email_from:
            partner = self.env['res.partner'].search([('email', '=', self.email_from), ('is_student', '=', True)], limit=1)

        if not partner and not email_only:
            # search through the existing partners based on the lead's partner or contact name
            # to be aligned with _create_customer, search on lead's name as last possibility
            for customer_potential_name in [self[field_name] for field_name in ['partner_name', 'contact_name', 'name']
                                            if self[field_name]]:
                partner = self.env['res.partner'].search([('name', 'ilike', '%' + customer_potential_name + '%'), ('is_student', '=', True)],
                                                         limit=1)
                if partner:
                    break

        return partner

    @api.depends('email_from')
    def _compute_portal_email_state(self):
        for lead in self:
            portal_email_state = False
            if lead.email_from:
                portal_users_with_email = lead.filtered(lambda user: email_normalize(user.email_from))
                (lead - portal_users_with_email).portal_email_state = 'not_ok'

                normalized_emails = [email_normalize(portal_user.email_from) for portal_user in portal_users_with_email]
                existing_users = self.env['res.users'].with_context(active_test=False).sudo().search_read(
                    [('login', 'in', normalized_emails)], ['id', 'login'])

                for portal_user in portal_users_with_email:
                    # if next((user for user in existing_users if
                    #          user['login'] == email_normalize(portal_user.email_from) and user[
                    #              'id'] != portal_user.user_id.id),
                    #         None):
                    if next((user for user in existing_users if
                             user['login'] == email_normalize(portal_user.email_from)),
                            None):
                        portal_user.portal_email_state = 'exist'
                    else:
                        portal_user.portal_email_state = 'ok'

    def _handle_partner_portal_user_assignment(self):
        """ Update customer - portal user of leads. Purpose is to set portal user
        on most leads; either through a newly created user either
        through existing portal user in partner.
        """
        for lead in self:
            user_obj = self.env['res.users']
            group_portal = self.env.ref('base.group_portal')
            group_public = self.env.ref('base.group_public')
            if lead.partner_id:
                lead.partner_id.is_student = True
                user = user_obj.search([('partner_id', '=', lead.partner_id.id)])
                lead.partner_portal_user = user.id
                if user and user.state == 'new':
                    lead.with_context(active_test=True)._send_portal_user_invite_email()
                if not user:
                    user = user_obj.with_context(no_reset_password=True)._create_user_from_template({
                        'email': email_normalize(lead.email_from),
                        'login': email_normalize(lead.email_from),
                        'partner_id': lead.partner_id.id,
                        'company_id': self.env.company.id,
                        'company_ids': [(6, 0, self.env.company.ids)],
                    })
                    user.write({'active': True, 'groups_id': [(4, group_portal.id), (3, group_public.id)],
                                'is_student': True})
                    # prepare for the signup process
                    user.partner_id.signup_prepare()
                    lead.partner_portal_user = user.id
                    lead.with_context(active_test=True)._send_portal_user_invite_email()

    def _send_portal_user_invite_email(self):
        """ send notification email to a new portal user """
        self.ensure_one()

        # determine subject and body in the portal user's language
        template = self.env.ref('lead_opportunity_custom.mail_template_data_student_welcome')
        if not template:
            raise UserError(_('The template "Opportunity: Student Invite" not found for sending email to the portal user.'))

        lang = self.partner_portal_user.sudo().lang
        partner = self.partner_portal_user.sudo().partner_id

        portal_url = partner.with_context(signup_force_type_in_url='', lang=lang)._get_signup_url_for_action()[partner.id]
        partner.signup_prepare()

        template.with_context(dbname=self._cr.dbname, portal_url=portal_url, lang=lang).send_mail(self.id, force_send=True)

        return True

    def action_send_mail(self):
        if self.partner_portal_user_state != 'active':
            raise ValidationError(_("The student has never logged in. Please wait for the student to log in."))
        res = super().action_send_mail()
        if res and 'context' in res:
            res['context']['mark_application_as_sent'] = True
        return res

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_application_as_sent'):
            self.filtered(lambda o: o.application_status == 'not_send').with_context(tracking_disable=True).write({'application_status': 'sent'})
        return super(Lead, self.with_context(
            mail_post_autofollow=self.env.context.get('mail_post_autofollow', True))).message_post(**kwargs)
