# -*- coding: utf-8 -*-
from venv import logger
from odoo import http,fields
from odoo.http import content_disposition, Controller, request, route
import datetime

class AttendancePortal(Controller):

    @http.route('/my/employee_list/shoot_request_menu', type='http', auth='user', website=True)
    def show_employee_list_shoot(self, **kw):
        employees = request.env['hr.employee'].sudo().search([('user_id', '=', http.request.env.user.id)])
        return request.render('infi_portal_shoot_request.employee_shoot_request_menu_template', {'employees': employees})
    
    # @http.route(['/my/employees/shoot'], type='http', auth='user', website=True)
    # def employee_shoot(self):
    #     employee = request.env['hr.employee']
    #     employees = employee.sudo().search([('user_id.groups_id', 'in', [request.env.ref('infinous_user_groups.assigment_hr').id])])
    #     user = http.request.env.user

    #     stage = http.request.env['shoot.request'].sudo().search([('user_id', '=', user.id)], limit=1).state
    #     return request.render('infi_portal_shoot_request.employee_shoot_request_form',{'employees': employees,'email':employees.work_email,'stage': stage,})
    
    @http.route(['/my/employees/shoot'], type='http', auth='user', website=True)
    def employee_shoot(self):
        employee = http.request.env['hr.employee']
        employees = employee.sudo().search([('user_id.groups_id', 'in', [http.request.env.ref('infinous_user_groups.assigment_hr').id])])
        
        user = http.request.env.user
        stage = http.request.env['shoot.request'].sudo().search([('user_id', '=', user.id)], limit=1).state
        
        # # Fetching email addresses of users belonging to the "Assignment Team"
        # assignment_team_group = http.request.env.ref('infinous_user_groups.assigment_team')
        # assignment_team_users = assignment_team_group.users.filtered(lambda user: user.email)  # Filter users with an email address
        
        # # Fetching the first email address from the assignment team users
        # assignment_team_email = assignment_team_users[0].email if assignment_team_users else None
        # Fetching email addresses of users belonging to the "Assignment Team"
        assignment_team_group = http.request.env.ref('infinous_user_groups.assigment_team')
        # Use sudo() to access records with elevated privileges
        assignment_team_users = assignment_team_group.sudo().users.filtered(lambda user: user.email)  # Filter users with an email address

        # Fetching the first email address from the assignment team users
        assignment_team_email = assignment_team_users[0].email if assignment_team_users else None
        assignment_team_users_name = assignment_team_group.sudo().users.filtered(lambda user: user.name)  # Filter users with an email address

        # Fetching the first email address from the assignment team users
        assignment_team_email_name = assignment_team_users_name[0].name if assignment_team_users_name else None


        return http.request.render('infi_portal_shoot_request.employee_shoot_request_form', {
            'employees': employees,
            'email': assignment_team_email,  # Pass the email address to the template
            'name' : assignment_team_email_name,
            'stage': stage,
        })


    @http.route(['/my/send_mail/shooting_request'], type='http', auth='user', website=True)
    def employee_shoot_submit(self, **kw):
        email_send = kw.get('email_send')
        email_from = kw.get('email_from')
        shoot_subject = kw.get('shoot_subject')
        shoot_description = kw.get('shoot_description')
        shoot_attachments = request.httprequest.files.getlist('shoot_attachments')
        employee_id = request.env.user.employee_id.id
        try:
            mail_values = {
                'author_id': request.env.user.partner_id.id,
                'email_from': email_from,
                'auto_delete': True,
                'email_to': email_send,
                'subject': shoot_subject,
                'body_html': shoot_description,
            }
            mail = request.env['mail.mail'].sudo().create(mail_values)

            if shoot_attachments:
                for attachment in shoot_attachments:
                    attachment_data = {
                        'name': attachment.filename,
                        'datas': attachment.read(),
                        'res_model': 'mail.message',
                        'res_id': mail.id,
                        'mimetype': attachment.content_type,
                    }
                    attachment = request.env['ir.attachment'].sudo().create(attachment_data)
                    mail.attachment_ids = [(4, attachment.id)]

            # Send the mail immediately after creation
            mail.send()

            request_date = fields.Date.today()

            shoot_request = request.env['shoot.request'].sudo().create({
                'employee_id': employee_id,
                'request_date': request_date,
            })

            shoot_request.state = 'shoot_req'

            return request.render('infi_portal_shoot_request.shootrequest_submited_view')


        except Exception as e:
            error_message = f"An error occurred while processing the form: {str(e)}"
            return error_message

    @http.route('/my/shootrequest/table', type='http', auth='user', website=True)
    def employee_shoot_table(self, **post):

        user = http.request.env.user
        stage = http.request.env['shoot.request'].sudo().search([('user_id', '=', user.id)], limit=1).state
        
        state_dict = {
            'draft': 'Draft',
            'shoot_req': 'Shoot Request',
            'to_storeperson': 'Request To store Person',
            'to_reporter': 'Assign To Reporter',
            'cancel': 'Canceled',
            'closed': 'Closed',
        }

        filters = []

        current_employee_id = request.env.user.employee_id.id
        filters.append(('employee_id','=',current_employee_id))

        records = request.env['shoot.request'].sudo().search(filters)
        print("rec", records)
        
        return http.request.render('infi_portal_shoot_request.shootrequest_table_view_template', {
            'records': records,
            'state_dict': state_dict,
            'stage': stage,
        })
