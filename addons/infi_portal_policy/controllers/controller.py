# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, request, route, Controller
from odoo.addons.portal.controllers.portal import CustomerPortal
import base64
from datetime import datetime
from odoo import http, fields


class CustomerPortalInherited(CustomerPortal):

    @http.route('/my/policy', type='http', methods=["POST"], auth="user", website=True, csrf=False)
    def fetch_policy_agree_form(self, **post):
        user = request.env.user
        today = datetime.now()
        employee = request.env.user.employee_id
        if employee:
            dept = employee.department_id.name
            employment_no = employee.registration_number
            reporting_manager = employee.parent_id.name
            employee.have_agreed_policy = True
            request.env['employee.policy.history'].sudo().create({
                "date": today,
                "employee_id": employee.id,
                "status": "true",
                "department": dept,
                "employement_id": employment_no,
                "reporting_manager": reporting_manager
            })
            print("iiiiiiiiiiii",dept,employment_no,reporting_manager)
        return "True"

    def _prepare_portal_layout_values(self):
        """Values for /my/* templates rendering.

        Does not include the record counts.
        """
        # get customer sales rep
        sales_user_sudo = request.env['res.users']
        partner_sudo = request.env.user.partner_id
        employee_sudo = request.env.user.employee_id
        if partner_sudo.user_id and not partner_sudo.user_id._is_public():
            sales_user_sudo = partner_sudo.user_id
        else:
            fallback_sales_user = partner_sudo.commercial_partner_id.user_id
            if fallback_sales_user and not fallback_sales_user._is_public():
                sales_user_sudo = fallback_sales_user
        policies = request.env['employee.policy'].sudo().search([])
        policy_list = []
        if policies:
            for policy in policies:
                policy_data = {
                    "name": policy.name,
                    "description": policy.description
                }
                policy_list.append(policy_data)
        return {
            'sales_user': sales_user_sudo,
            'page_name': 'home',
            'policies': policy_list,
            'policy_state': employee_sudo.have_agreed_policy
        }


