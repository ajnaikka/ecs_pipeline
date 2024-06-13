from odoo import models, fields

class JoiningLetter(models.Model):
    _name = 'joining.letter'
    _description = 'Joining Letter'

    STATES = [
        ('draft', 'Draft'),
        ('letter_generated', 'Letter Generated'),
    ]

    state = fields.Selection(STATES, string='State', default='draft')


    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    joining_date = fields.Date(string='Joining Date', required=True)
    department = fields.Many2one('hr.department', string='Department', required=True)
    designation = fields.Many2one('hr.job', string='Designation', required=True)


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'


    def create_employee_from_applicant(self):
        employee_id = super(HrApplicant, self).create_employee_from_applicant()


        if employee_id:
            joining_letter_obj = self.env['joining.letter'].create({
                'employee_id': self.emp_id.id,
                'joining_date': fields.Date.today(),
                'department': self.department_id.id,
                'designation': self.job_id.id,
            })

        return employee_id

