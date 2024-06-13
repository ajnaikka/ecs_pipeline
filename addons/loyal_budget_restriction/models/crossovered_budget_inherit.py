from odoo import models, fields, api, exceptions


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'



class CrossoveredBudgetLines(models.Model):
    _inherit = 'crossovered.budget.lines'

    budget = fields.Float('Budget')
    additional_budget = fields.Float('Additional Budget')
    planned_amount = fields.Monetary(
        'Planned Amount', required=True,
        help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.")


    @api.onchange('budget', 'additional_budget')
    def _onchange_planned_amount(self):
        for rec in self:
            rec.planned_amount = rec.budget + rec.additional_budget





class ExpenseInvoice(models.Model):
    _inherit = 'account.move'

    @api.constrains('amount_total')
    def _check_budget(self):
        for invoice in self:
            for inv in invoice.invoice_line_ids:
                acc = inv.account_id
                budgets = self.env['crossovered.budget.lines'].search([])
                for budget in budgets:
                    general = budget.general_budget_id.account_ids
                    for gen in general:
                        if gen.id == acc.id:
                            planned_amount = budget.planned_amount
                            if invoice.amount_total > planned_amount:
                                raise exceptions.ValidationError('Invoice amount exceeds the budgeted amount.')










