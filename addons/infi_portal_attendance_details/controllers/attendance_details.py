# -*- coding: utf-8 -*-

from odoo.http import Controller, request, route
from odoo import fields
from odoo import http
import re
from datetime import datetime

from odoo.tools.safe_eval import json


class AttendanceDetailsPortal(Controller):
    
    @route(['/my/employees/attendance_details'], type='http', auth='user', website=True)
    def employee_attendance_details(self):
        employee = request.env.user.employee_id
        current_emp_attendance = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee.id)])
        return request.render('infi_portal_attendance_details.employee_attendance_tree_view',
                              {'employees': current_emp_attendance, 'employee': employee})

    @http.route('/create_attendance', type='http', auth="user", website=True)
    def create_attendance(self, action=None):
        employee_id = request.env.user.employee_id
        if employee_id:
            if action == 'checkin':
                attendance_vals = {
                    'employee_id': employee_id.id,
                    'check_in': fields.Datetime.now(),
                }
                request.env['hr.attendance'].sudo().create(attendance_vals)
            elif action == 'checkout':
                last_attendance = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id.id)],
                                                                             order='id desc', limit=1)
                if last_attendance:
                    last_attendance.sudo().write({'check_out': fields.Datetime.now()})
            return request.redirect('/my/employees/attendance_details')


    @http.route('/send_attendance_correction', type='http', auth="public", website=True)
    def send_attendance_correction(self, **post):
        subject = post.get('subject')
        subjects = post.get('subjects')
        checkin_date = post.get('checkin_date')
        checkin = post.get('checkin')
        employee_email = post.get('employee_email')


        hr_manager = request.env.user.employee_id.hr_manager_id
        
        current_employee = request.env.user.employee_id.name

        mail_user = hr_manager.user_id.id
        user_revoke = request.env['res.users'].sudo().browse(mail_user)

        formatted_checkin_date = datetime.strptime(checkin_date, '%m/%d/%Y').strftime('%d-%m-%Y') if checkin_date else None


        formatted_checkin_date_2 = datetime.strptime(checkin, '%Y-%m-%d').strftime('%d-%m-%Y') if checkin else None

        message_post = request.env.user.partner_id.message_post(
            body=subject if subject else subjects,
            subject=f'Attendance Correction Request From {current_employee} for {formatted_checkin_date}' if formatted_checkin_date else f'Attendance Correction Request From {current_employee} in  {formatted_checkin_date_2}',
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
            author_id=request.env.user.partner_id.id
        )

        if message_post:
            notification_values = [{
                'res_partner_id': user.partner_id.id,
                'mail_message_id': message_post.id
            } for user in user_revoke]

            message_post.sudo().notification_ids = [(0, 0, vals) for vals in notification_values]

        mail_values = {
            'body_html': subject if subject else subjects,
            'email_to': employee_email,
            'subject': f'Attendance Correction Request From {current_employee} for {formatted_checkin_date}' if formatted_checkin_date else f'Attendance Correction Request From {current_employee} in  {formatted_checkin_date_2}',
        }

        mail = request.env['mail.mail'].sudo().create(mail_values)
        mail.send()

        return request.render('infi_portal_attendance_details.attendance_correction_submited_view', {
            'subject': subject if subject else subjects
        })

    @http.route('/hr_attendance/upload_imaged', type='http', auth="public", website=True)
    def uploadingImg(self, **post):
        # Get the image data from the POST request
        image_data_checkin = post.get('image_data')
        # outformData = post.get('outimageData')
        user_name = request.env.user.name

        print("User:", user_name)
        image_data = image_data_checkin.split(",")[1]
        print("image_data", image_data)
        # print("outformData", outformData)

        # Search for an existing attendance record
        attendance_record = request.env['hr.attendance'].sudo().search([
            ('checked_in', '=', False),  # Check if checked_out field is not set
            ('employee_id', '=', request.env.user.employee_id.id)  # Add additional conditions if needed
        ], limit=1)

        if attendance_record:
            # Update existing record with the outformData
            attendance_record.write({'checked_in': image_data})

            # attendance_record.write({'checked_out': outformData})
            print("Updated existing attendance record:", attendance_record.id)
            return json.dumps({'success': True, 'attendance_record_id': attendance_record.id})
        else:
            # Create a new record
            attendance_record = request.env['hr.attendance'].sudo().create({
                'checked_in': image_data,

                # Add any other fields you need to set
            })
            print("Created new attendance record:", attendance_record.id)
            return json.dumps({'success': True, 'attendance_record_id': attendance_record.id})

    @http.route('/hr_attendance/upload_imaged_out', type='http', auth="public", website=True)
    def uploadingImgout(self, **post):
        # Get the image data from the POST request
        #     image_data = post.get('image_data')
            outformData_out = post.get('outimageData')
            user_name = request.env.user.name

            print("User:", user_name)
            outformData = outformData_out.split(",")[1]
            # print("image_data", image_data)
            print("outformData", outformData)

            # Search for an existing attendance record
            attendance_record = request.env['hr.attendance'].sudo().search([
                ('checked_out', '=', False),  # Check if checked_out field is not set
                ('employee_id', '=', request.env.user.employee_id.id)  # Add additional conditions if needed
            ], limit=1)

            if attendance_record:
                # Update existing record with the outformData
                # attendance_record.write({'checked_in': image_data})

                attendance_record.write({'checked_out': outformData})
                print("Updated existing attendance record:", attendance_record.id)
                return json.dumps({'success': True, 'attendance_record_id': attendance_record.id})
            else:
                # Create a new record
                attendance_record = request.env['hr.attendance'].sudo().create({
                    
                    'checked_out': outformData,
                    # Add any other fields you need to set
                })
                print("Created new attendance record:", attendance_record.id)
                return json.dumps({'success': True, 'attendance_record_id': attendance_record.id})