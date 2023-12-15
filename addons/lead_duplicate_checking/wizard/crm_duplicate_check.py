# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class CrmDuplicateCheck(models.TransientModel):
    _name = 'crm.duplicate.check'
    _description = 'CRM Duplicate Check Wizard'

    duplicated_opportunity_ids = fields.Many2many('crm.lead', 'duplicate_opportunity_rel',
          'duplicate_check_id', 'opportunity_id', string="Duplicated Opportunities", domain="[('type', '=', 'opportunity')]")
    duplicate_lead_ids = fields.Many2many('crm.lead', 'duplicate_lead_rel',
          'duplicate_check_id', 'lead_id', string="Duplicate Leads", domain="[('type', '=', 'lead')]")
    message = fields.Text(string="Message")
    duplication = fields.Boolean(default=False, required=True, string="Is duplicate entry?")

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_lead_id
        to ease window action definitions, and be backward compatible. """
        result = super(CrmDuplicateCheck, self).default_get(fields_vals)

        # if not result.get('lead_id') and self.env.context.get('active_id'):
        #     result['lead_id'] = self.env.context.get('active_id')
        # if result.get('lead_id'):
        #     lead = self.env['crm.lead'].browse(result['lead_id'])
        #     result['course_id'] = lead.admission_register.course_id.id
        #     result['register_id'] = lead.admission_register.id
        #     result['student_id'] = lead.student_id.id
        #     result['fees_term_id'] = lead.admission_register.course_id.fees_term_id.id
        #     result['discount'] = lead.admission_register.course_id.fees_term_id.discount or 0
        #     result['fees'] = lead.admission_register.product_id.lst_price
        return result

    def action_delete_leads(self):
        for record in self.duplicate_lead_ids:
            record.unlink()

    def action_convert_to_opportunity(self):
        duplicate_stage = self.env['crm.stage'].search([('duplicate_stage', '=', True)], limit=1)
        for lead in self.duplicate_lead_ids:
            lead2opportunity = self.env['crm.lead2opportunity.partner'].with_context({'active_id': lead.id, 'active_ids': [lead.id], 'active_model': 'crm.lead'}).create({
                'name': 'convert',
                'lead_id': lead.id,
            })
            lead2opportunity.action_apply()
            lead.stage_id = duplicate_stage.id
