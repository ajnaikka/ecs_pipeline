# -*- coding: utf-8 -*-
# from odoo import http


# class ExamRegister(http.Controller):
#     @http.route('/exam_register/exam_register', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exam_register/exam_register/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exam_register.listing', {
#             'root': '/exam_register/exam_register',
#             'objects': http.request.env['exam_register.exam_register'].search([]),
#         })

#     @http.route('/exam_register/exam_register/objects/<model("exam_register.exam_register"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exam_register.object', {
#             'object': obj
#         })
