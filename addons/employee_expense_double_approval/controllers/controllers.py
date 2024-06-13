# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeExpenseDoubleApproval(http.Controller):
#     @http.route('/employee_expense_double_approval/employee_expense_double_approval', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_expense_double_approval/employee_expense_double_approval/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_expense_double_approval.listing', {
#             'root': '/employee_expense_double_approval/employee_expense_double_approval',
#             'objects': http.request.env['employee_expense_double_approval.employee_expense_double_approval'].search([]),
#         })

#     @http.route('/employee_expense_double_approval/employee_expense_double_approval/objects/<model("employee_expense_double_approval.employee_expense_double_approval"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_expense_double_approval.object', {
#             'object': obj
#         })

