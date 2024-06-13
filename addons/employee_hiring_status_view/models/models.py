# -*- coding: utf-8 -*-
from odoo import fields, models,api

class ResUsers(models.Model):
    _inherit = 'res.users'

    department_id = fields.Many2one('hr.department', string='Department')

class HrJob(models.Model):
    _inherit = 'hr.job'

    @api.model
    def _get_domain_for_own_department(self):
        # Retrieve the current user's department
        user_department_id = self.env.user.department_id.id
        # Define the domain to filter jobs based on the user's department
        domain = [('department_id', '=', user_department_id)]
        return domain

    # Create a record rule to apply the domain when reading hr.job records
    @api.model
    def create_record_rule_for_own_department(self):
        domain = self._get_domain_for_own_department()
        rule = self.env['ir.rule'].create({
            'name': 'View Own Department Jobs',
            'model_id': self.env.ref('hr.model_hr_job').id,
            'domain_force': domain,
            'perm_read': True,
            'perm_write': False,
            'perm_create': False,
            'perm_unlink': False,
        })
        return rule
class HrApplicant(models.Model):
    _inherit = 'hr.applicant'