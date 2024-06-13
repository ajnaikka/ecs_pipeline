from odoo import http
import base64

from odoo.http import request
from odoo.tools.safe_eval import json


class myAttendance(http.Controller):

    @http.route('/hr_attendance/upload_imageds', type='http', auth="public", website=True)
    def uploadingImgs(self, **post):
        # Get the image data from the POST request
        image_data_in = post.get('image_data')
        outformData = post.get('outimageData')
        image_data = image_data_in.split(",")[1]
        user_name = request.env.user.name

        print("User:", user_name)

        print("checkin", image_data)
        print("outformData", outformData)

        # Search for an existing attendance record
        attendance_record = request.env['hr.attendance'].sudo().search([
            ('checked_out', '=', False),  # Check if checked_out field is not set
            ('employee_id', '=', request.env.user.employee_id.id)  # Add additional conditions if needed
        ], limit=1)

        if attendance_record:
            # Update existing record with the outformData
            attendance_record.write({'checked_in': image_data})

            attendance_record.write({'checked_out': outformData})
            print("Updated existing attendance record:", attendance_record.id)
            return json.dumps({'success': True, 'attendance_record_id': attendance_record.id})
        else:
            # Create a new record
            attendance_record = request.env['hr.attendance'].sudo().create({
                'checked_in': image_data,
                'checked_out': outformData,
                # Add any other fields you need to set
            })
            print("Created new attendance record:", attendance_record.id)
            return json.dumps({'success': True, 'attendance_record_id': attendance_record.id})
    @http.route('/hr_attendance/upload_image', type='http', auth='user')
    def upload_image(self, **post):
        image_data = post.get('image_data')
        test = post.get('image_out')
        outformData = test.split(",")[1]
        user_name = request.env.user.name

        print("User:", test)

        print("checkout", image_data)
        print("outformData", outformData)

        # Search for an existing attendance record
        attendance_record = request.env['hr.attendance'].sudo().search([
            ('checked_out', '=', False),  # Check if checked_out field is not set
            ('employee_id', '=', request.env.user.employee_id.id)  # Add additional conditions if needed
        ], limit=1)

        if attendance_record:
            # Update existing record with the outformData
            attendance_record.write({'checked_out': outformData})
            print("Updated existing attendance record:", attendance_record.id)
            return json.dumps({'success': True, 'attendance_record_id': attendance_record.id})
        else:
            # Create a new record
            attendance_record = request.env['hr.attendance'].sudo().create({
                'checked_in': image_data,
                'checked_out': outformData,
                # Add any other fields you need to set
            })
            print("Created new attendance record:", attendance_record.id)
            return json.dumps({'success': True, 'attendance_record_id': attendance_record.id})