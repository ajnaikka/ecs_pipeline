# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, Controller, request, route

class CompensatoryPortal(Controller):
    @route(['/my/employees/compensatory'], type='http', auth='user', website=True)
    def employee(self):
        employee = request.env['hr.employee']
        return request.render('infi_portal_attendance_correction.employee_list_attendance_form',
                              {'employees': employee, 'email': employee.work_email})

    @http.route('/my/employee/compensatorys', type='http', auth='user', website=True)
    def comp_req(self, **kw):
        return request.render('infi_compensatory_request.employee_compensatory_email_form')

    @http.route('/my/employee/compensatorys', type='http', auth='user', website=True)
    def comp_req(self, **kw):
        return request.render('infi_compensatory_request.employee_compensatory_email_form')

    @http.route('/my/employee_comp', type='http', auth='user', website=True)
    def comp(self, **kw):
        return request.render('infi_compensatory_request.employee_list_template_compensatory')

    @http.route('/my/compensatory/tables', type='http', auth='user', website=True)
    def compensatory_table_view(self, **post):
        state_dict = {
            'draft': 'Draft',
            'to_reporter': 'Request To Reporting Manager',
            'to_hr': 'Request to hr',
            'approved': 'Approved',
            'cancel': 'Rejected',
        }

        filters = []

        current_employee_id = request.env.user.employee_id.id
        filters.append(('employee_id', '=', current_employee_id))

        records = request.env['compensatory.request'].sudo().search(filters)

        return http.request.render('infi_compensatory_request.compensatory_table_view_template', {
            'records': records,
            'state_dict': state_dict,
        })


    @http.route('/my/employee_compensatory_email', type='http', auth='user', website=True)
    def submit(self, **kw):
        employees =  request.env.user.employee_id# Example search condition
        print("employees",employees.name)

        for employee in employees:
            if employee:
                Attendance = request.env['hr.attendance']
                print(Attendance, 'attendance')
                count = Attendance.sudo().search_count(
                    [('employee_id', '=', employee.id), ('status', '=', 'approved')])
                print(count,'count')
                if count > 0:
                    email = kw.get('email')
                    subject = kw.get('subject')
                    description = kw.get('description')
                    attachments = request.httprequest.files.getlist('attachments')
                    send_to = kw.get('employee_list')
                    request_date = kw.get('date_from')
                    request_date_to = kw.get('date_to')
                    comp = {
                        'employee_id': request.env.user.employee_id.id,
                        'date_from': request_date,
                        'date_to':request_date_to,
                    }
                    compensatory = request.env['compensatory.request'].sudo().create(comp)

                    print(compensatory, 'compensatory')
                    compensatory.state = 'to_reporter'
                    try:
                        mail_values = {
                            'author_id': request.env.user.partner_id.id,
                            'email_from': request.env.user.email_formatted,
                            'auto_delete': True,
                            'email_to': email,
                            'subject': subject,
                            'body_html': description,
                        }
                        mail = request.env['mail.mail'].sudo().create(mail_values)

                        if attachments:
                            for attachment in attachments:
                                attachment_data = {
                                    'name': attachment.filename,
                                    'datas': attachment.read(),
                                    'res_model': 'mail.message',
                                    'res_id': mail.id,
                                    'mimetype': attachment.content_type,
                                }
                                attachment = request.env['ir.attachment'].sudo().create(attachment_data)
                                mail.attachment_ids = [(4, attachment.id)]

                        mail.send()

                        return request.render('infi_compensatory_request.compensatory_submitted_view')
                    except Exception as e:
                        error_message = f"An error occurred while sending the email: {str(e)}"
                        return error_message

                else:
                    print('okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                    return request.render('infi_compensatory_request.compensatory_cancel_submitted_view')







