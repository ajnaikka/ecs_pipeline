from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    structure_type_id = fields.Many2one('hr.payroll.structure.type', "Salary Structure Type")
    contract_type_id = fields.Many2one('hr.contract.type', "Contract Type", )
    ise_invisible = fields.Boolean(string="Invisible")

    @api.onchange('structure_type_id')
    def _compute_contract_type_id(self):
        for record in self:
            record.contract_type_id = self.structure_type_id.contract_type_id
            if record.structure_type_id.contract_type:
                record.ise_invisible = True
            else:
                record.ise_invisible = False

    @api.onchange('contract_type_id')
    def permenant_choose_error(self):
        for record in self:
            if record.structure_type_id.contract_type and self.contract_type_id.permanent:
                raise ValidationError("The Worker Cannot Select Permanent Contract type.")
