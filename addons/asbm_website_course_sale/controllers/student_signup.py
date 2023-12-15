# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request
import werkzeug.utils
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class StudentSignup(AuthSignupHome):

    @http.route()
    def web_auth_signup(self, *args, **kw):
        response = super(StudentSignup, self).web_auth_signup(*args, **kw)
        qcontext = self.get_auth_signup_qcontext()
        User = request.env['res.users']
        user_sudo = User.sudo().search(
            User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
        )
        template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
        if user_sudo and template:
            template.sudo().send_mail(user_sudo.id, force_send=True)
        return response

