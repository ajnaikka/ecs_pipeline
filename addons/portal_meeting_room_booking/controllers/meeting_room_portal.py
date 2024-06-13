# -*- coding: utf-8 -*-
from odoo import http,fields
from odoo.http import content_disposition, Controller, request, route
from datetime import datetime
import pytz
from datetime import timedelta


class MeetingRoomPortal(Controller):

    @route(['/meeting/room/booking'], type='http', auth='user', website=True)
    def meeting_room(self):
        room_booked_list = http.request.env['room.booking'].sudo().search([])

        formatted_room_booked_list = []

        user_tz = http.request.env.user.tz or 'UTC'

        for room_booking in room_booked_list:
            start_datetime = room_booking.start_datetime.astimezone(pytz.timezone(user_tz)).strftime(
                '%d-%m-%Y %H:%M')
            stop_datetime = room_booking.stop_datetime.astimezone(pytz.timezone(user_tz)).strftime('%d-%m-%Y %H:%M')

            formatted_room_booking = {
                'start_datetime': start_datetime,
                'stop_datetime': stop_datetime,
                'name': room_booking.name,
                'room_name': room_booking.room_id.name,
                'organizer_name': room_booking.organizer_id.name,
                'room_id': room_booking.id
            }

            formatted_room_booked_list.append(formatted_room_booking)


        print('formatted_room_booked_list',formatted_room_booked_list)

        return request.render('portal_meeting_room_booking.meeting_room_table_view_template',
                              {'room_booked_list': formatted_room_booked_list})

    @http.route('/meeting/room/booking/form', type='http', auth='user', website=True)
    def show_employee_list(self, room_id=None, **kw):
        room_booking = request.env['room.booking'].sudo().browse(int(room_id)) if room_id else False
        organizer = request.env['res.users'].sudo().search([])
        room = request.env['room.room'].sudo().search([])
        user_tz = pytz.timezone(request.env.user.tz or 'UTC')
        current_time = datetime.now(pytz.utc).astimezone(user_tz)
        user_tz = http.request.env.user.tz or 'UTC'

        start_time = ''
        stop_time = ''

        if room_booking:
            start_time = room_booking.start_datetime.astimezone(pytz.timezone(user_tz))
            stop_time = room_booking.stop_datetime.astimezone(pytz.timezone(user_tz))

        return request.render('portal_meeting_room_booking.meeting_room_booking_form',
                              {'room_booking': room_booking, 'start_datetime': start_time,
                               'stop_datetime': stop_time,
                               'organizer': organizer, 'rooms': room, 'current_time': current_time})

    @http.route('/room_booking/submit/from', type='http', auth='user', website=True)
    def submit_room(self, **kw):
        meeting_name = kw.get('meeting_name')
        room_id = int(kw.get('room_id'))
        start_datetime_str = kw.get('start_datetime')
        stop_datetime_str = kw.get('stop_datetime')
        organizer_id = int(kw.get('organizer'))
        
        start_datetime = pytz.utc.localize(datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M'))
        stop_datetime = pytz.utc.localize(datetime.strptime(stop_datetime_str, '%Y-%m-%dT%H:%M'))

        start_datetime_local = start_datetime
        stop_datetime_local = stop_datetime

        start_datetime_local -= timedelta(hours=5, minutes=30)
        stop_datetime_local -= timedelta(hours=5, minutes=30)

        room = request.env['room.room'].sudo().browse(room_id)
        organizer = request.env['res.users'].sudo().browse(organizer_id)

        room_booking_id = kw.get('room_booking')
        room_booking_data = {
            'name': meeting_name,
            'room_id': room.id,
            'start_datetime': start_datetime_local.strftime('%Y-%m-%d %H:%M'),
            'stop_datetime': stop_datetime_local.strftime('%Y-%m-%d %H:%M'),
            'organizer_id': organizer.id
        }

        if room_booking_id and room_booking_id.isdigit():
            room_booking = request.env['room.booking'].sudo().browse(int(room_booking_id))
            room_booking.sudo().write(room_booking_data)
        else:
            request.env['room.booking'].sudo().create(room_booking_data)

        return request.render('portal_meeting_room_booking.application_submited_view')






