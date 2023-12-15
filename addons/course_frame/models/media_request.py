# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MediaRequest(models.Model):
    _name = 'media.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Media Request'

    def _check_user_has(self):
        for data in self:
            if data.department_head_id.user_id.id == self.env.user.id:
                data.is_dep_head = True
            else:
                data.is_dep_head = False
            if data.employee_id.user_id.id == self.env.user.id:
                data.is_assigned_emp = True
            else:
                data.is_assigned_emp = False


    name = fields.Char(string="Name",required=True, copy=False, readonly=True,index='trigram',default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'), ('assigned', 'Assigned DH'),('assigned_emp', 'Assigned EMP'),('submitted', 'Submitted'),
                              ('reject', 'Rejected'), ('approved', 'Approved')], copy=False, tracking=True,
                             default='draft')
    department_id = fields.Many2one('hr.department', 'Department')
    date = fields.Date('Request Date',default=fields.Date.context_today)
    request_type_id = fields.Many2one('request.type', 'Type Of Request')
    course_frame_id = fields.Many2one('course.frame', 'Course Frame')
    expected_date = fields.Date('Expected Date')
    dead_date = fields.Date('Dead Date')
    department_head_id = fields.Many2one('hr.employee', related='department_id.manager_id', string='Department Head')
    employee_id = fields.Many2one('hr.employee', 'Assigned To', )
    create_uid = fields.Many2one('res.users', index=True,string="Created by")

    attachment_id = fields.Binary('Media')
    remark = fields.Text('Remarks')
    color = fields.Integer('Colour')
    is_assigned_emp = fields.Boolean('Is Assigned Emp',compute='_check_user_has',default=False)
    is_dep_head = fields.Boolean('Is Department Head',compute='_check_user_has',default=False)
    is_content_writer = fields.Boolean('Is Content Writer', related='course_frame_id.is_content_writer')
    is_team_lead = fields.Boolean('Is TL', related='course_frame_id.is_team_lead')
    is_academic_head = fields.Boolean('Is AH', related='course_frame_id.is_academic_head')
    is_ass_dean = fields.Boolean('Is AD', related='course_frame_id.is_ass_dean')
    is_managing_dir = fields.Boolean('Is MD', related='course_frame_id.is_managing_dir')

    def action_open_media_request_form(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('course_frame.media_request_action_window')
        action.update({
            'view_mode': 'form',
            'view_id': self.env.ref('course_frame.view_media_request_form').id,
            'views': [(self.env.ref('course_frame.view_media_request_form').id, 'form')],
            'res_id': self.id,
        })
        return action



    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('media.request') or _('New')
        request = super(MediaRequest, self).create(vals)
        return request

    def action_assigned(self):
        for data in self:
            if not data.department_id:
                raise UserError(_("Please select the department."))
            # if not data.employee_id:
            #     raise UserError(_("Please select the employee."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'media.request')]).ids
            for user in data.department_head_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.department_head_id.user_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' assigns the media request ' + data.name + '. And assigned it to you Please do the needful.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'assigned'})

    def action_assign_to_emp(self):
        for data in self:
            if not data.department_id:
                raise UserError(_("Please select the department."))
            if not data.employee_id:
                raise UserError(_("Please select the employee."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'media.request')]).ids
            for user in data.employee_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.employee_id.user_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' assigns the media request ' + data.name + '. And assigned it to you Please do the needful.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'assigned_emp'})

    def action_submitted_to_department_head(self):
        for data in self:
            if not data.attachment_id:
                raise UserError(_("Please upload the media."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'media.request')]).ids
            for user in data.department_head_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.department_head_id.user_id.name + ', ' + data.employee_id.user_id.name  + ' uploads the media against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'submitted'})

    def action_department_head_approve(self):
        for data in self:
            return data.write({'state': 'approved',
                               'remark': False})

    def action_department_head_reject(self):
        for data in self:
            if not data.remark:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'media.reques')]).ids
            for user in data.employee_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.employee_id.user_id.name + ', ' + data.department_head_id.user_id.name + ' Rejected the media request ' + data.name + 'due to , ' + data.remark + ' . Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'reject'})

    def action_reject_to_back_submitted(self):
        for data in self:
            return data.write({'state': 'submitted'})