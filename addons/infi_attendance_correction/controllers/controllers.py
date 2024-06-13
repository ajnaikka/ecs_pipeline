# -*- coding: utf-8 -*-
# from odoo import http


# class InfiAttendanceCorrection(http.Controller):
#     @http.route('/infi_attendance_correction/infi_attendance_correction', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/infi_attendance_correction/infi_attendance_correction/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('infi_attendance_correction.listing', {
#             'root': '/infi_attendance_correction/infi_attendance_correction',
#             'objects': http.request.env['infi_attendance_correction.infi_attendance_correction'].search([]),
#         })

#     @http.route('/infi_attendance_correction/infi_attendance_correction/objects/<model("infi_attendance_correction.infi_attendance_correction"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('infi_attendance_correction.object', {
#             'object': obj
#         })

