# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError, RedirectWarning
import logging

_logger = logging.getLogger(__name__)




class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    # state = fields.Selection(selection_add=[('approved_manager', 'Approved By Manager')],string="Status",ondelete={'approved_manager': 'set default'} )
    state = fields.Selection(
        selection=[
            ('draft', 'To Submit'),
            ('submit', 'Submitted'),
            # ('approved_manager', 'Approved By Manager'),
            ('approve', 'Approved By Manager'),
            ('post', 'Posted'),
            ('done', 'Done'),
            ('cancel', 'Refused')
        ],
        string="Status",
        compute='_compute_state', store=True, readonly=True,
        index=True,
        required=True,
        default='draft',
        tracking=True,
        copy=False,
    )
    # def action_approve_by_manager(self, ctx=None):
    #     # Your logic to handle approval by manager
    #     template = self.env.ref('employee_expense_double_approval.manager_to_hr_email')
    #     compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
    #
    #     context = {
    #         'default_model': 'hr.expense.sheet',
    #         'default_res_ids': [self.id],
    #         # 'default_partner_ids': [self.email_to.id],
    #         'default_raise_req_id': self.id,
    #         'default_use_template': bool(template),
    #         'default_template_id': template.id,
    #         'default_composition_mode': 'comment',
    #         'default_attachment_ids': None,
    #         'force_email': True,
    #         'default_email_from': self.employee_id.parent_id.work_email,
    #         'default_partner_id': self.employee_id.parent_id.user_partner_id.id
    #     }
    #
    #     if ctx:
    #         context.update(ctx)
    #     print(context, 'context')
    #
    #     self.write({'state': 'approved_manager'})
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'mail.compose.message',
    #         'views': [(compose_form_id, 'form')],
    #         'views_id': compose_form_id,
    #         'target': 'new',
    #         'context': context,
    #     }

    def action_refuse_by_hr_manager(self):
        # Your logic to handle approval by manager
        # self.write({'state': 'cancel'})
        self._check_can_refuse()
        return self.env["ir.actions.act_window"]._for_xml_id('hr_expense.hr_expense_refuse_wizard_action')
    # def action_approve_by_manager(self):
    #     # Your logic to handle approval by manager
    #     self.write({'state': 'approved_manager'})
    #
    #     # Find HR manager email and name
    #     hr_manager = self.employee_id.hr_manager_id
    #     if hr_manager and hr_manager.work_email:
    #         # Compose the message
    #         subject = _("Expense report approval needed")
    #         body = _("Dear HR,<br/><br/>"
    #
    #                  "Please review and approve the expense report of the employee %s") % (self.employee_id.name)
    #
    #         # Send message to HR manager
    #         self.env['mail.mail'].create({
    #             'subject': subject,
    #             'body_html': body,
    #             'email_to': hr_manager.work_email,
    #         }).send()
    #
    #     return True
    def action_reset_approval_expense_sheets(self):
        self._check_can_reset_approval()
        self._do_reset_approval()

    def action_refuse_expense_sheets(self):
        self._check_can_refuse()
        return self.env["ir.actions.act_window"]._for_xml_id('hr_expense.hr_expense_refuse_wizard_action')


    def action_approve_expense_sheets(self):
        self._check_can_approve()
        self._validate_analytic_distribution()
        duplicates = self.expense_line_ids.duplicate_expense_ids.filtered(lambda exp: exp.state in {'approved', 'done'})
        if duplicates:
            action = self.env["ir.actions.act_window"]._for_xml_id('hr_expense.hr_expense_approve_duplicate_action')
            action['context'] = {'default_sheet_ids': self.ids, 'default_expense_ids': duplicates.ids}
            return action
        self._do_approve()
        return self.write({'state': 'approve'})
    def _do_approve(self):
        for sheet in self.filtered(lambda s: s.state in {'submit', 'draft'}):
            sheet.write({
                'approval_state': 'approve',
                'user_id': sheet.user_id.id or self.env.user.id,
                'approval_date': fields.Date.context_today(sheet),
            })
        self.activity_update()
    def _check_can_approve(self):
        if not all(self.mapped('can_approve')):
            reasons = _("You cannot approve:\n %s", "\n".join(self.mapped('cannot_approve_reason')))
            raise UserError(reasons)


class HrExpense(models.Model):
    _inherit = "hr.expense"
    # state = fields.Selection(selection_add=[('approved_manager', 'Approved By Manager')],string="Status",ondelete={'approved_manager': 'set default'} ,
    #
    #     compute='_compute_state', store=True, readonly=True,
    #     index=True,
    #     copy=False,
    #     default='draft',
    # )
    state = fields.Selection(
        selection=[
            ('draft', 'To Report'),
            ('reported', 'To Submit'),
            ('submitted', 'Submitted'),
            # ('approved_manager', 'Approved By Manager'),
            ('approved', 'Approved By Manager'),
            ('done', 'Done'),
            ('refused', 'Refused')
        ],
        string="Status",
        compute='_compute_state', store=True, readonly=True,
        index=True,
        copy=False,
        default='draft',
    )

    @api.depends('sheet_id', 'sheet_id.account_move_ids', 'sheet_id.state')
    def _compute_state(self):
        for expense in self:
            if not expense.sheet_id:
                expense.state = 'draft'
            elif expense.sheet_id.state == 'draft':
                expense.state = 'reported'
            elif expense.sheet_id.state == 'cancel':
                expense.state = 'refused'
            # elif expense.sheet_id.state == 'approved_manager':
            #     expense.state = 'approved_manager'
            elif expense.sheet_id.state in {'approve', 'post'}:
                expense.state = 'approved'
            elif not expense.sheet_id.account_move_ids:
                expense.state = 'submitted'
            else:
                expense.state = 'done'

