# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, Controller, request, route

from odoo.addons.portal.controllers.mail import PortalChatter


class CustomPortalChatter(PortalChatter):

    @http.route('/mail/chatter_init', type='json', auth='public', website=True)
    def portal_chatter_init(self, res_model, res_id, domain=False, limit=False, **kwargs):
        is_user_public = http.request.env.user.has_group('base.group_public') or http.request.env.user.has_group(
            'base.group_portal')
        message_data = self.portal_message_fetch(res_model, res_id, domain=domain, limit=limit, **kwargs)
        display_composer = False
        if kwargs.get('allow_composer'):
            display_composer = kwargs.get('token') or not is_user_public
        return {
            'messages': message_data['messages'],
            'options': {
                'message_count': message_data['message_count'],
                'is_user_public': is_user_public,
                'is_user_employee': request.env.user._is_internal(),
                'is_user_publisher': request.env.user.has_group('website.group_website_restricted_editor'),
                'display_composer': display_composer,
                'partner_id': request.env.user.partner_id.id
            }
        }






