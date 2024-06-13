from odoo import models, fields, api, _

class HrContract(models.Model):
    _inherit = 'hr.contract'

    user_group_bool = fields.Boolean(
        string='User Group Boolean',
        compute='_compute_responsible_group_bool'
    )

    def _compute_responsible_group_bool(self):
        for record in self:
            # Check each group individually
            record.user_group_bool = any(
                self.env.user.has_group(group) for group in ['account.group_account_manager', 'account.group_account_user','account.group_account_invoice'])


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    date_difference = fields.Integer(string='Date Difference', compute='_compute_date_difference', store=True)

    def action_salary_slip(self):
        report = self.env.ref('infinous_user_groups.action_salary_slip_template')
        return report.report_action(self)

    @api.depends('date_from', 'date_to')
    def _compute_date_difference(self):
        for record in self:
            if record.date_from and record.date_to:
                delta = record.date_to - record.date_from
                record.date_difference = delta.days
            else:
                record.date_difference = 0





