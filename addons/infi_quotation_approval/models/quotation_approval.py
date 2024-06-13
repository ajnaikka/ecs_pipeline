from odoo import models, fields, api, _


class EmployeeRecruitement(models.Model):
    _inherit = ['hr.employee']

    def quotation_approval_wizard_action(self):
        print()


