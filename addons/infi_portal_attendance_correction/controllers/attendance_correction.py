# -*- coding: utf-8 -*-
from venv import logger
from odoo import http,fields
from odoo.http import content_disposition, Controller, request, route
import datetime

class AttendancePortal(Controller):

    @route(['/my/employees/attendance'], type='http', auth='user', website=True)
    def employee(self):
        employee = request.env['hr.employee']
        employees = employee.sudo().search([('user_id.groups_id', 'in', [request.env.ref('infinous_user_groups.assigment_hr').id])],limit=1)
        user = http.request.env.user

        stage = http.request.env['attendance.correction'].sudo().search([('user_id', '=', user.id)], limit=1).state

        return request.render('infi_portal_attendance_correction.employee_list_attendance_form', {'employees': employees,'email':employees.work_email,'stage': stage,})

    @http.route('/my/employee_list/attendance_correction', type='http', auth='user', website=True)
    def show_employee_list(self, **kw):
        employees = request.env['hr.employee'].sudo().search([('user_id', '=', http.request.env.user.id)])
        return request.render('infi_portal_attendance_correction.employee_list_template_attendance', {'employees': employees})
    

    @http.route('/my/send_mail/attendance', type='http', auth='user', website=True)
    def submit(self, **kw):
        email_attendance = kw.get('email_attendance')
        subject_attendance = kw.get('subject_attendance')
        description_attendance = kw.get('description_attendance')
        attachments_attendance = request.httprequest.files.getlist('attachments_attendance')
        employee_id = request.env.user.employee_id.id  

        try:
            mail_values = {
                'author_id': request.env.user.partner_id.id,
                'email_from': request.env.user.email_formatted,
                'auto_delete': True,
                'email_to': email_attendance,
                'subject': subject_attendance,
                'body_html': description_attendance,
            }
            mail = request.env['mail.mail'].sudo().create(mail_values)

            if attachments_attendance:
                for attachment in attachments_attendance:
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

            request_date = fields.Date.today()
            attendance_correction = request.env['attendance.correction'].sudo().create({
                'employee_id': employee_id,
                'request_date': request_date,
            })

            attendance_correction.state = 'raise_correction_req'

            return request.render('infi_portal_attendance_correction.application_submited_view')

        except Exception as e:
            error_message = f"An error occurred while processing the form: {str(e)}"
            return error_message


        
    @http.route('/my/attendance/table', type='http', auth='user', website=True)
    def attendance_table_view(self, **post):
        state_dict = {
            'draft': 'Draft',
            'raise_correction_req': 'Attendance Correction Request to Manager',
            'issue_address': 'Issue Addressed',
            'corrected': 'Accepted & Corrected',
            'cancel': 'Rejected',
            'closed': 'Closed',
        }

        filters = []

        current_employee_id = request.env.user.employee_id.id
        filters.append(('employee_id', '=', current_employee_id))

        records = request.env['attendance.correction'].sudo().search(filters)

        return http.request.render('infi_portal_attendance_correction.attendance_table_view_template', {
            'records': records,
            'state_dict': state_dict,
        })
