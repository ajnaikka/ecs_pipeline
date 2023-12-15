# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lead_status = fields.Char(string="Lead Status")

    def check_lead_duplication(self):
        _lead_all_with_dup = self.env['crm.lead'].search([('type', '=', 'lead')], order='id asc')
        duplicated_opportunity = []
        duplicate_leads = []
        duplicated_opportunity_list = []
        if _lead_all_with_dup:
            for _lead_rec in _lead_all_with_dup:
                email_from = _lead_rec.email_from
                if email_from:
                    check_stage_ids = self.env['crm.lead'].search(
                        [('stage_id.avoid_duplicate_check', '!=', True), ('type', '=', 'opportunity'),
                         ('email_from', '=', email_from)])
                    if check_stage_ids:
                        _lead_rec.write({
                            'lead_status': 'Duplication',
                        })
                        duplicate_leads.append((4, _lead_rec.id))
                        for i in check_stage_ids:
                            if i.id not in duplicated_opportunity_list:
                                duplicated_opportunity_list.append(i.id)
                        for _check_stage_ids_rec in check_stage_ids:
                            if _check_stage_ids_rec.user_id:
                                # Send Notification
                                notification_ids = []
                                notification_ids.append((0, 0, {
                                    'res_partner_id': _check_stage_ids_rec.user_id.partner_id.id,
                                    'notification_status': 'exception'}))

                                _check_stage_ids_rec.message_post(
                                    body="You received duplicate lead notification",
                                    subject=_('Duplicate Lead'),
                                    message_type='comment',
                                    author_id=_check_stage_ids_rec.user_id.partner_id.id,
                                    partner_ids=_check_stage_ids_rec.user_id.partner_id.ids,
                                    subtype_id=self.env.ref('mail.mt_comment').id,
                                    notification_ids=notification_ids,
                                )
        all_leads_without_dupe = self.env['crm.lead'].search([('type', '=', 'lead'), ('lead_status', '!=', 'Duplication')], order='id asc')
        if all_leads_without_dupe:
            for lead_rec in all_leads_without_dupe:
                email_from = lead_rec.email_from
                if email_from and lead_rec.lead_status != 'Duplication':
                    lead_rec.lead_status = 'Fresh'
                    check_lead_ids = self.env['crm.lead'].search([
                        ('stage_id.avoid_duplicate_check', '!=', True), ('type', '=', 'lead'),
                        ('email_from', '=', email_from), ('id', '!=', lead_rec.id)])
                    if check_lead_ids:
                        if lead_rec.user_id:
                            # Send Notification
                            notification_ids = []
                            notification_ids.append((0, 0, {
                                'res_partner_id': lead_rec.user_id.partner_id.id,
                                'notification_status': 'exception'}))

                            lead_rec.message_post(
                                body="You received duplicate lead notification",
                                subject=_('Duplicate Lead'),
                                message_type='comment',
                                author_id=lead_rec.user_id.partner_id.id,
                                partner_ids=lead_rec.user_id.partner_id.ids,
                                subtype_id=self.env.ref('mail.mt_comment').id,
                                notification_ids=notification_ids,
                            )
                        for lead in check_lead_ids:
                            duplicate_leads.append((4, lead.id))
                            lead.write({
                                'lead_status': 'Duplication',
                            })
        fresh_leads = self.env['crm.lead'].search([('type', '=', 'lead'), ('lead_status', '=', 'Fresh')],
                                                  order='id asc')
        for lead in fresh_leads:
            lead2opportunity = self.env['crm.lead2opportunity.partner'].with_context({'active_id': lead.id, 'active_ids': [lead.id], 'active_model': 'crm.lead'}).create({
                'name': 'convert',
                'lead_id': lead.id,
            })
            res = lead2opportunity.action_apply()
        if duplicated_opportunity_list:
            for record in duplicated_opportunity_list:
                duplicated_opportunity.append((4, record))
        if duplicated_opportunity or duplicate_leads:
            vals = {
                'duplicated_opportunity_ids': duplicated_opportunity if duplicated_opportunity else False,
                'duplicate_lead_ids': duplicate_leads if duplicate_leads else False,
                'duplication': True,
                'message': "All leads are converted to opportunity"
            }
            crm_check = self.env['crm.duplicate.check'].create(vals)
            return {
                'name': _('CRM Duplication'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'views': [[False, "form"]],
                'res_model': 'crm.duplicate.check',
                'target': 'new',
                'res_id': crm_check.id,
                'context': self.env.context,
            }
        else:
            vals = {
                'duplication': False,
                'message': "All leads are converted to opportunity"
            }
            crm_check = self.env['crm.duplicate.check'].create(vals)
            return {
                'name': _('CRM Duplication'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'views': [[False, "form"]],
                'res_model': 'crm.duplicate.check',
                'target': 'new',
                'res_id': crm_check.id,
                'context': self.env.context,
            }
