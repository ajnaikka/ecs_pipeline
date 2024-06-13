from odoo import models, fields, api, _


class HrContractTypeInherit(models.Model):
    _inherit = 'hr.contract.type'

    permanent = fields.Boolean('Permanent')
