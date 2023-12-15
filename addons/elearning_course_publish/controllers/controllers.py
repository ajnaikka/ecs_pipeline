# -*- coding: utf-8 -*-
# from odoo import http


# class ElearningCoursePublish(http.Controller):
#     @http.route('/elearning_course_publish/elearning_course_publish', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/elearning_course_publish/elearning_course_publish/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('elearning_course_publish.listing', {
#             'root': '/elearning_course_publish/elearning_course_publish',
#             'objects': http.request.env['elearning_course_publish.elearning_course_publish'].search([]),
#         })

#     @http.route('/elearning_course_publish/elearning_course_publish/objects/<model("elearning_course_publish.elearning_course_publish"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('elearning_course_publish.object', {
#             'object': obj
#         })
