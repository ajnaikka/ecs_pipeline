from odoo import models, fields, api, _


class HrPayrollStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'

    contract_type_id = fields.Many2one('hr.contract.type', "Contract Type")
    contract_type = fields.Boolean('Is Worker')
