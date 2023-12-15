# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request
import werkzeug.utils
from odoo.addons.portal.controllers.web import Home as home


class StudentLogin(home):

    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        response = super(StudentLogin, self).web_login(
            redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            login_user = request.env['res.users'].browse(request.uid)
            if not login_user.has_group('base.group_user') and login_user.partner_id.is_student:
                redirect = '/slides'
                return werkzeug.utils.redirect(redirect)
        return response

    def _login_redirect(self, uid, redirect=None):
        res = super(StudentLogin, self)._login_redirect(uid, redirect)
        if request.env.user.partner_id.is_student:
            return '/slides'
        return res
