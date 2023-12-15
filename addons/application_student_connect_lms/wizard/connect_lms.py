# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class StudentConnectLMSWizard(models.TransientModel):
    _name = 'student.connect.lms.wizard'
    _description = 'Connect student to LMS Wizard'

    admission_id = fields.Many2one(comodel_name='op.admission', string="Associated Application", required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    connect_to_lms = fields.Boolean(string="Connect to LMS", default=True)
    slide_channel_id = fields.Many2one('slide.channel', string='LMS')

    @api.depends('course_id', 'course_id.course_frame_id')
    def compute_lms(self):
        if self.course_id.course_frame_id:
            lms = self.env['slide.channel'].search([('course_frame_id', '=', self.course_id.course_frame_id.id)],
                                                   limit=1)
            if lms:
                self.slide_channel_id = lms.id

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_lead_id
        to ease window action definitions, and be backward compatible. """
        result = super(StudentConnectLMSWizard, self).default_get(fields_vals)

        if not result.get('admission_id') and self.env.context.get('active_id'):
            result['admission_id'] = self.env.context.get('active_id')
        if result.get('admission_id'):
            admission = self.env['op.admission'].browse(result['admission_id'])
            result['course_id'] = admission.course_id.id
            result['slide_channel_id'] = self.env['slide.channel'].search([('course_frame_id', '=', admission.course_id.course_frame_id.id)], limit=1) if admission.course_id.course_frame_id else False
        return result

    def action_connect_to_lms(self):
        if self.connect_to_lms:
            if self.slide_channel_id:
                lms = self.slide_channel_id
            else:
                lms = self.env['slide.channel'].search([('course_frame_id', '=', self.course_id.course_frame_id.id)], limit=1) if self.course_id.course_frame_id else False
            if not lms:
                raise ValueError(_("Matching LMS not found"))
            template = self.env.ref('website_slides.mail_template_slide_channel_invite', raise_if_not_found=False)

            local_context = dict(
                self.env.context,
                default_channel_id=lms.id,
                default_partner_ids=[(4, self.admission_id.partner_id.id)],
                default_admission_id=self.admission_id.id,
                default_use_template=bool(template),
                default_template_id=template and template.id or False,
                default_email_layout_xmlid='website_slides.mail_notification_channel_invite',
            )
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'slide.channel.invite',
                'target': 'new',
                'context': local_context,
            }
