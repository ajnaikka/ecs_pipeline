# # -*- coding: utf-8 -*-
from odoo.http import content_disposition, Controller, request, route
from odoo import http, fields

class CustomerPortal(Controller):

    @http.route('/send_shift_request', type='http', auth="user", website=True)
    def send_shift_request(self, **post):
        parent_work_email = request.env.user.employee_id.parent_id.work_email
        emp = request.env.user.employee_id.name

        subject = post.get('subjects')
        shift_id = post.get('shift_id')


        shift_requests = request.env['shift.request'].sudo().search([('id', '=', shift_id)])
        shift_requests.sudo().write({'state': 'request'})

        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        form_view_url = f'{base_url}/web#id={shift_id}&view_type=form&model=shift.request'

        mail_values = {
            'subject': f'Shift Correction Request of {emp}',
            'body_html': f'{subject}<br><br><a class="btn btn-primary" href="{form_view_url}" target="_blank">View Shift Details</a>',
            'email_to': parent_work_email,
        }
        mail = request.env['mail.mail'].sudo().create(mail_values)
        mail.send()

        return request.render('infi_employee_shift.shift_application_submited_views',
                              {'subject': subject})

    @http.route('/employee/shift', type='http', auth='user', website=True)
    def employee_shift(self, **post):
        employee = request.env.user.employee_id.id
        employee_manager = request.env.user.employee_id.parent_id
        shift = request.env['shift.request'].sudo().search([('employee_id','=',employee)])
        return request.render('infi_employee_shift.shift_tree_view',
                              {'shift_list': shift,'employee_manager':employee_manager})

