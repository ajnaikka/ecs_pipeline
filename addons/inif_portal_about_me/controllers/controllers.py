# -*- coding: utf-8 -*-
from odoo import http
from odoo import http,fields
from odoo.http import content_disposition, Controller, request, route
import datetime

class AboutMePortal(Controller):

    @route(['/my/employees/about_me'], type='http', auth='user', website=True)
    def employee(self):
        employee = request.env['hr.employee']
        employees = employee.sudo().search([('user_id.groups_id', 'in', [request.env.ref('infinous_user_groups.assigment_hr').id])])
        user = http.request.env.user

        stage = http.request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1).state
        employee = request.env.user.employee_id
        if not employee.have_agreed_policy:
            return request.redirect('/my')
        else:
            return request.render('hr.view_employee_form', {'employees': employees,'email':employees.work_email,})
