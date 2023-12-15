# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError


class SlideChannelInvite(models.TransientModel):
    _inherit = 'slide.channel.invite'

    def action_invite(self):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed """
        self.ensure_one()

        if not self.env.user.email:
            raise UserError(_("Unable to post message, please configure the sender's email address."))
        if not self.partner_ids:
            raise UserError(_("Please select at least one recipient."))

        try:
            self.channel_id.check_access_rights('write')
            self.channel_id.check_access_rule('write')
        except AccessError:
            raise AccessError(
                _('You are not allowed to add members to this course. Please contact the course responsible or an administrator.'))

        mail_values = []
        for partner_id in self.partner_ids:
            slide_channel_partner = self.channel_id._action_add_members(partner_id)
            if slide_channel_partner:
                mail_values.append(self._prepare_mail_values(slide_channel_partner))

        created_mail = self.env['mail.mail'].sudo().create(mail_values)
        created_mail.send()

        return {'type': 'ir.actions.act_window_close'}
