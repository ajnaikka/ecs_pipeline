# -*- coding: utf-8 -*-
from venv import logger
from odoo import http, fields
from odoo.http import content_disposition, Controller, request, route
import datetime
from werkzeug.datastructures import ImmutableMultiDict



class travelRequest(Controller):

    @http.route('/my/employees/travel_request', type='http', auth='user', website=True)
    def show_employee_list(self, **kw):
        user = http.request.env.user
        stage = http.request.env['travel.request'].sudo().search([('user_id', '=', user.id)], limit=1).state

        return request.render('infi_portal_travle_request.travel_request_form', {
            'stage': stage,
        })

    @http.route('/my/employees/travel_request/home', type='http', auth='user', website=True)
    def show_employee_list_home(self, **kw):

        return request.render('infi_portal_travle_request.travel_request_portal_employee')
    @http.route(['/my/send_mail/travel_request'], type='http', auth='user', website=True)
    def employee_travel_submit(self, **kw):
        # Convert kw to ImmutableMultiDict to use getlist method
        kw = ImmutableMultiDict(kw)

        description = kw.get('description')
        travel_place = kw.getlist('travel_place[]')
        place_description = kw.getlist('place_description[]')
        request_date = kw.get('request_date')
        employee_id = request.env.user.employee_id.id
        reporting_manager = request.env.user.employee_id.parent_id.work_email
        email_from = kw.get('email_from')
        travel_start_date = kw.get('travel_start_date')
        travel_end_date = kw.get('travel_end_date')

        try:
            # Create and send email
            body_content = f'<p>{description}</p>'
            body_content += '<p><strong>Travel Details:</strong></p>'
            travel_placesss = []
            for i in range(len(request.httprequest.form.getlist('travel_place[]'))):
                place = request.httprequest.form.getlist('travel_place[]')[i]
                place_description = request.httprequest.form.getlist('place_description[]')[i]
                travel_placesss.append((0, 0, {
                    'name': place,
                    'place_name': place_description
                }))

                body_content += f'<p><strong>Place:</strong> {travel_placesss}</p>'


            print("Body Content:", body_content)  # Add this line for debugging

            travel_places = []
            for i in range(len(request.httprequest.form.getlist('travel_place[]'))):
                place = request.httprequest.form.getlist('travel_place[]')[i]
                place_description = request.httprequest.form.getlist('place_description[]')[i]
                travel_places.append((0, 0, {
                    'name': place,
                    'place_name': place_description
                }))

            print("Travel Places:", travel_places)  # Add this line for debugging

            mail_values = {
                'author_id': request.env.user.partner_id.id,
                'email_from': email_from,
                'auto_delete': True,
                'email_to': reporting_manager,
                'subject': 'Travel Request',
                'body_html': body_content,
            }
            mail = request.env['mail.mail'].sudo().create(mail_values)
            mail.send()

            # Create travel request record
            travel_request = request.env['travel.request'].sudo().create({
                'employee_id': employee_id,
                'description': description,
                'request_date': request_date,
                'start_date': travel_start_date,
                'end_date': travel_end_date,
                'travel_place_ids': travel_places,
            })
            travel_request.state = 'travel_req'

            print("Travel Request:", travel_request)  # Add this line for debugging

            return request.render('infi_portal_travle_request.travelrequest_submit_view')

        except Exception as e:
            error_message = f"An error occurred while processing the form: {str(e)}"
            print("Error:", error_message)  # Add this line for debugging
            return error_message

    @http.route('/my/employees/travel_request/status', type='http', auth='user', website=True)
    def show_employee_request(self, **kw):
        user = http.request.env.user
        stage = http.request.env['travel.request'].sudo().search([('user_id', '=', user.id)], limit=1).state

        state_dict = {
            'draft': 'Draft',
            'travel_req': 'Travel Approve Request to Manager',
            'approve_manager': 'Approved by Manager',
            'refuse_manager': 'Refused by Manager',

        }
        print("state_dict",state_dict)
        filters = []

        current_employee_id = request.env.user.employee_id.id
        filters.append(('employee_id', '=', current_employee_id))

        records = request.env['travel.request'].sudo().search(filters)
        print("rec", records)

        return http.request.render('infi_portal_travle_request.travelrequest_table_view_template', {
            'records': records,
            'state_dict': state_dict,
            'stage': stage,
        })


