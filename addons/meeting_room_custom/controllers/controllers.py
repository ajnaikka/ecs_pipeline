# -*- coding: utf-8 -*-
# from odoo import http


# class MeetingRoomCustom(http.Controller):
#     @http.route('/meeting_room_custom/meeting_room_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/meeting_room_custom/meeting_room_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('meeting_room_custom.listing', {
#             'root': '/meeting_room_custom/meeting_room_custom',
#             'objects': http.request.env['meeting_room_custom.meeting_room_custom'].search([]),
#         })

#     @http.route('/meeting_room_custom/meeting_room_custom/objects/<model("meeting_room_custom.meeting_room_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('meeting_room_custom.object', {
#             'object': obj
#         })

