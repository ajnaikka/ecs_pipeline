# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    po_approval = fields.Boolean(default=False, string='PO Approval')
    lower_amount = fields.Monetary(string="Lower Amount", readonly=False, )
    higher_amount = fields.Monetary(string="Higher Amount", readonly=False, )



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lower_amount = fields.Monetary(string="Lower Amount", currency_field='company_currency_id',related='company_id.lower_amount', readonly=False)
    higher_amount = fields.Monetary(string="Higher Amount", currency_field='company_currency_id',related='company_id.higher_amount', readonly=False)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('waiting_for_manager_approval', 'Lower Authority Approved'),
                                            ('waiting_for_medium_level_approval', 'Medium Authority Approved'),
                                            ('waiting_for_higher_manager_approval', 'Higher Authority Approved'),
                                            ('waiting_for_financial_approval', 'Finance Approved'),
                                            ('refused', 'Refused')])

    partner_ids = fields.Many2many('res.partner', string='Vendors')

    @api.model_create_multi
    def create(self, vals_list):
        orders = super(PurchaseOrder, self).create(vals_list)


        for order in orders:
            if order.partner_ids:
                if self.env.context.get('send_rfq', False):
                    mail_template = self.env.ref('purchase.email_template_edi_purchase', raise_if_not_found=False)
                else:
                    mail_template = self.env.ref('purchase.email_template_edi_purchase_done', raise_if_not_found=False)

                for partner in order.partner_ids:
                    new_order = order.copy(default={'partner_id': partner.id, 'partner_ids': False})
                    if new_order != order:
                        if mail_template:
                            mail_template.send_mail(new_order.id, force_send=True)
                            new_order.message_post(
                                body="Email sent to vendor {} using template {}".format(partner.name,
                                                                                        mail_template.name))

                if mail_template:
                    mail_template.send_mail(order.id, force_send=True)
                    order.message_post(body="Email sent to vendors using template {}".format(mail_template.name))

        return orders


    # def button_confirm(self):
    #     for order in self:
    #         if not order.company_id.po_approval:
    #             res = super(PurchaseOrder, self).button_confirm()
    #         else:
    #             if order.state in ['waiting_for_financial_approval']:
    #                 if order.env.user.user_has_groups('purchase_order_approval.group_finance_manager'):
    #                     order._add_supplier_to_product()
    #                     # Deal with double validation process
    #                     if order.company_id.po_double_validation == 'one_step' \
    #                         or (order.company_id.po_double_validation == 'two_step' \
    #                             and order.amount_total < self.env.company.currency_id._convert(
    #                             order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
    #                             order.date_order or fields.Date.today())) \
    #                             or order.user_has_groups('purchase.group_purchase_manager'):
    #                         order.button_approve()
    #                     else:
    #                         order.write({'state': 'to approve'})
    #                     res = True
    #                 else:
    #                     raise UserError(_(
    #                         "Your are not allowed to confirm the purchase order."))
    #             else:
    #                 res = True
    #                 if order.env.user.user_has_groups('purchase_order_approval.group_operation_manager'):
    #                     order.write({'state': 'waiting_for_director_approval'})
    #                     continue
    #                 else:
    #                     order.write({'state': 'waiting_for_manager_approval'})
    #                     continue
    #         return res
    def button_confirm(self):
        for order in self:
            order.write({'state': 'purchase'})
    # def button_approve(self, force=False):
    #     self = self.filtered(lambda order: order._approval_allowed())
    #     self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
    #     self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
    #     return {}
    @api.depends('amount_total', 'company_id.lower_amount')
    def _compute_can_manager_approval(self):
        for order in self:
            order.can_manager_approval = order.amount_total <= order.company_id.lower_amount


    can_manager_approval = fields.Boolean(compute='_compute_can_manager_approval', store=True)

    finance_manager_emails = fields.Many2many(
        'res.users', string='Finance Managers', compute='_compute_finance_manager_emails', store=True
    )

    @api.depends('company_id', 'company_id.lower_amount')
    def _compute_finance_manager_emails(self):
        finance_manager_group = self.env.ref('purchase_order_approval.group_finance_manager')
        self.finance_manager_emails = finance_manager_group.users


    def button_manager_approval(self):
        for order in self:
            if order.can_manager_approval:
                # order.write({'state': 'waiting_for_manager_approval'})
                # purchase_lower_authority_group = self.env.ref('purchase_order_approval.group_lower_purchase_director')
                # finance_manager_group = self.env.ref('purchase_order_approval.group_finance_manager')
                #
                # # Notify purchase director group
                # partners = purchase_lower_authority_group.users.mapped('partner_id')
                # message = f"RFQ  {order.name} approved by  purchase lower authority group. Please Verify and Confirm by Finance Manager."
                # order.message_post(body=message, partner_ids=partners.ids)
                #
                # # Notify finance manager group via Discuss
                # finance_managers = finance_manager_group.users
                # for finance_manager in finance_managers:
                #     finance_manager.partner_id.message_post(
                #         body=message,
                #     )
                template = self.env.ref('purchase_order_approval.lower_authority_approval_email')
                compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

                context = {
                    'default_model': 'purchase.order',
                    'default_res_ids': [self.id],
                    # 'default_partner_ids': [self.email_to.id],
                    'default_raise_req_id': self.id,
                    'default_use_template': bool(template),
                    'default_template_id': template.id,
                    'default_composition_mode': 'comment',
                    'default_attachment_ids': None,
                    'force_email': True,
                    'default_email_from': self.env.user.partner_id.email,
                    'default_partner_id': self.user_id.employee_id.id
                }



                self.write({'state': 'waiting_for_manager_approval'})

                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'mail.compose.message',
                    'views': [(compose_form_id, 'form')],
                    'views_id': compose_form_id,
                    'target': 'new',
                    'context': context,
                }


            else:
                raise UserError(_("You are not allowed to approve. Amount exceeds the configured limit."))

    def button_senior_manager_approval(self):
        for order in self:
            order.write({'state': 'waiting_for_higher_manager_approval'})
            template = self.env.ref('purchase_order_approval.higher_authority_approval_email')
            compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

            context = {
                'default_model': 'purchase.order',
                'default_res_ids': [self.id],
                # 'default_partner_ids': [self.email_to.id],
                'default_raise_req_id': self.id,
                'default_use_template': bool(template),
                'default_template_id': template.id,
                'default_composition_mode': 'comment',
                'default_attachment_ids': None,
                'force_email': True,
                'default_email_from': self.env.user.partner_id.email,
                'default_partner_id': self.user_id.employee_id.id
            }


            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form_id, 'form')],
                'views_id': compose_form_id,
                'target': 'new',
                'context': context,
            }


    @api.depends('amount_total', 'company_id.lower_amount', 'company_id.higher_amount')
    def _compute_can_medium_approval(self):
        for order in self:
            order.can_medium_approval = order.company_id.lower_amount <= order.amount_total <= order.company_id.higher_amount

    can_medium_approval = fields.Boolean(compute='_compute_can_medium_approval', store=True)

    def button_medium_authority_approval(self):
        for order in self:
            if order.can_medium_approval:
                # order.write({'state': 'waiting_for_medium_level_approval'})
                # purchase_medium_authority_group = self.env.ref('purchase_order_approval.group_medium_level_authority')
                # finance_manager_group = self.env.ref('purchase_order_approval.group_finance_manager')

                # Notify purchase director group
                # partners = purchase_medium_authority_group.users.mapped('partner_id')
                # message = f"RFQ  {order.name} approved by  purchase medium authority group. Please Verify and Confirm by Finance Manager."
                # order.message_post(body=message, partner_ids=partners.ids)

                # Notify finance manager group via Discuss
                # finance_managers = finance_manager_group.users
                # for finance_manager in finance_managers:
                #     finance_manager.partner_id.message_post(
                #         body=message,
                #     )

                template = self.env.ref('purchase_order_approval.medium_authority_approval_email')
                compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

                context = {
                    'default_model': 'purchase.order',
                    'default_res_ids': [self.id],
                    # 'default_partner_ids': [self.email_to.id],
                    'default_raise_req_id': self.id,
                    'default_use_template': bool(template),
                    'default_template_id': template.id,
                    'default_composition_mode': 'comment',
                    'default_attachment_ids': None,
                    'force_email': True,
                    'default_email_from': self.env.user.partner_id.email,
                    'default_partner_id': self.user_id.employee_id.id
                }

                self.write({'state': 'waiting_for_medium_level_approval'})

                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'mail.compose.message',
                    'views': [(compose_form_id, 'form')],
                    'views_id': compose_form_id,
                    'target': 'new',
                    'context': context,
                }
            else:
                raise UserError(
                    _("You are not allowed to approve. Amount should be between Lower Amount and Higher Amount."))


    def button_finance_manager_approval(self):
        for order in self:
            order.write({'state': 'waiting_for_financial_approval'})

    def button_refuse(self):
        for order in self:
            order.write({'state': 'refused'})



