# -*- coding: utf-8 -*-
# from odoo import http


# class CourseFrame(http.Controller):
#     @http.route('/course_frame/course_frame', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/course_frame/course_frame/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('course_frame.listing', {
#             'root': '/course_frame/course_frame',
#             'objects': http.request.env['course_frame.course_frame'].search([]),
#         })

#     @http.route('/course_frame/course_frame/objects/<model("course_frame.course_frame"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('course_frame.object', {
#             'object': obj
#         })
