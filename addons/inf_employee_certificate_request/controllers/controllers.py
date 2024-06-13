from odoo import http
from odoo.http import request

class EmployeeController(http.Controller):

    @http.route('/confirm_action/<int:employee_id>', type='http', auth="public", website=True)
    def confirm_action(self, employee_id, **kw):
        employee = request.env['hr.employee'].browse(employee_id)
        if employee:
            action = request.env.ref('inf_employee_certificate_request.action_confirmation_description_form')
            action['context'] = {'default_employee_id': employee.id,'default_status_bool': True}
            action_url = '/web#action=%s' % action.id
            return request.redirect(action_url)

    @http.route('/terminate_action/<int:employee_id>', type='http', auth="public", website=True)
    def terminate_action(self, employee_id, **kw):
        employee = request.env['hr.employee'].browse(employee_id)
        if employee:
            action = request.env.ref('inf_employee_certificate_request.action_confirmation_description_form')
            action['context'] = {'default_employee_id': employee.id,'default_status_bool': False}
            action_url = '/web#action=%s' % action.id
            return request.redirect(action_url)
