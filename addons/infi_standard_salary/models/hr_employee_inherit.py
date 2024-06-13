from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    basic_salary = fields.Float('Basic salary')
    house_rent_allowance = fields.Float('House Rent Allowance')
    conveyance_allowance = fields.Float('Conveyance Allowance')
    other_allowance = fields.Float('Other Allowance')
    special_allowance = fields.Float('Special Allowance')
    pancard_no = fields.Char('Pan No')
    insurance_number = fields.Char('Insurance No')
    pf_number = fields.Char('PF No')