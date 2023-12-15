# -*- coding: utf-8 -*-
# from odoo import http


# class ApplicationStudentConnectLms(http.Controller):
#     @http.route('/application_student_connect_lms/application_student_connect_lms', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/application_student_connect_lms/application_student_connect_lms/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('application_student_connect_lms.listing', {
#             'root': '/application_student_connect_lms/application_student_connect_lms',
#             'objects': http.request.env['application_student_connect_lms.application_student_connect_lms'].search([]),
#         })

#     @http.route('/application_student_connect_lms/application_student_connect_lms/objects/<model("application_student_connect_lms.application_student_connect_lms"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('application_student_connect_lms.object', {
#             'object': obj
#         })
