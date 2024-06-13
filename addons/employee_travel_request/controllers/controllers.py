# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeTravelRequest(http.Controller):
#     @http.route('/employee_travel_request/employee_travel_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_travel_request/employee_travel_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_travel_request.listing', {
#             'root': '/employee_travel_request/employee_travel_request',
#             'objects': http.request.env['employee_travel_request.employee_travel_request'].search([]),
#         })

#     @http.route('/employee_travel_request/employee_travel_request/objects/<model("employee_travel_request.employee_travel_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_travel_request.object', {
#             'object': obj
#         })

