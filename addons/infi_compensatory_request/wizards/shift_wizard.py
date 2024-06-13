from odoo import models, fields, api, exceptions, _


class ShiftRequestEmployeeWizard(models.TransientModel):
    _name = 'shift.request.employee.wizard'
    _description = 'Shift Request Employee Wizard'

    employee_ids = fields.Many2many('hr.employee', string='Employees')
    shift_day_start = fields.Date(string='Start Date')
    shift_day_end = fields.Date(string='End Date')
    shift_id = fields.Many2one('shift.master', string='Shift')

    def confirm(self):
        shift_request_vals_list = []
        for employee in self.employee_ids:
            vals = {
                'employee_id': employee.id,
                'shift_id': self.shift_id.id,
                'shift_from': self.shift_day_start,
                'shift_to': self.shift_day_end,
            }
            shift_request_vals_list.append(vals)

        self.env['shift.request'].create(shift_request_vals_list)
