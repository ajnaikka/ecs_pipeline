# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeHiringStatusView(http.Controller):
#     @http.route('/employee_hiring_status_view/employee_hiring_status_view', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_hiring_status_view/employee_hiring_status_view/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_hiring_status_view.listing', {
#             'root': '/employee_hiring_status_view/employee_hiring_status_view',
#             'objects': http.request.env['employee_hiring_status_view.employee_hiring_status_view'].search([]),
#         })

#     @http.route('/employee_hiring_status_view/employee_hiring_status_view/objects/<model("employee_hiring_status_view.employee_hiring_status_view"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_hiring_status_view.object', {
#             'object': obj
#         })

