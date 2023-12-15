# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ContentDevelopment(models.Model):
    _name = 'content.development'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Content Development'

    def _check_user1_has(self):
        for data in self:
            if data.employee_1_id.user_id.id == self.env.user.id:
                data.is_assigned_emp_1 = True
            else:
                data.is_assigned_emp_1 = False

    def _check_user2_has(self):
        for data in self:
            if data.employee_2_id.user_id.id == self.env.user.id:
                data.is_assigned_emp_2 = True
            else:
                data.is_assigned_emp_2 = False

    def _check_userhas(self):
        for data in self:
            if data.department_head_id.user_id.id == self.env.user.id:
                data.is_dh = True
            else:
                data.is_dh = False

    name = fields.Char(string="Name", required=True, copy=False, readonly=True, index='trigram',
                       default=lambda self: _('New'))

    state = fields.Selection([('content_book_format', 'Content Book Format'),
                              ('alignment_dtp_work', 'Alignment DTP work '),
                              ('vetting_external', 'Book Content Vetting External'),
                              ('book_verification', 'Book Content Verification'),
                              ], copy=False, tracking=True,
                             default='content_book_format', string='Status')

    stage_1 = fields.Selection([('draft', 'Draft'), ('assigned', 'Assigned'), ('submitted_to_tl', 'Submitted To Tl'),
                                ('tl_approved', 'Submitted to AH'), ('rejected_by_tl', 'TL Rejected'),
                                ('reject', 'AH Rejected'), ('approved', 'AH Approved')], default='draft', copy=False,
                               tracking=True, string="State1")
    stage_2 = fields.Selection([('draft', 'Draft'), ('assigned', 'Assigned DH'), ('assigned_emp', 'Assigned EMP'),('submitted_to_dh', 'Submitted To DH'),
                                ('dh_approved', 'Submitted To TL'),
                                ('rejected_by_dh', 'DH Rejected'), ('ah_approved', 'TL Approved'),
                                ('ah_rejected', 'TL Rejected')], default='draft', copy=False, tracking=True)
    stage_3 = fields.Selection([('draft', 'Draft'), ('send', 'Sended'), ('submitted', 'Submitted'),
                                ('reject', 'Rejected'), ('approved', 'Approved')], default='draft', copy=False,
                               tracking=True, string="State2")
    stage_4 = fields.Selection([('send', 'Send To MD'), ('approve', 'Approved'), ('reject', 'Rejected')],
                               default='send', copy=False,
                               tracking=True, string="State2")

    course_frame_id = fields.Many2one('course.frame', 'Course Frame')

    date = fields.Date('Request Date', default=fields.Date.context_today)
    employee_1_id = fields.Many2one('hr.employee', 'Assigned To', )
    employee_2_id = fields.Many2one('hr.employee', 'Assigned To')
    department_id = fields.Many2one('hr.department', 'Department')
    department_head_id = fields.Many2one('hr.employee', related='department_id.manager_id', string='Department Head')
    request_type_id = fields.Many2one('request.type', 'Type Of Request')
    due_date = fields.Date('Due Date')
    expected_date = fields.Date('Expected Date')
    dead_date = fields.Date('Dead Date')
    subject_id = fields.Many2one('op.subject', required=True)
    unit_id = fields.Many2one('subject.unit', required=True)
    topic_id = fields.Many2one('subject.topic', required=True)
    book_format_content = fields.Binary('Book Format Doc')
    dtp_content = fields.Binary('DTP Alignment Doc')
    vetting_content = fields.Binary('Vetting Doc')
    vetting_content_checked = fields.Binary('Approved Vetting Doc')
    remarks = fields.Char('Remarks')
    color = fields.Integer('Colour')

    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    receive_user_id = fields.Many2one('res.users', 'Receive User')

    is_assigned_emp_1 = fields.Boolean('Is Assigned Emp1', compute='_check_user1_has', default=False)
    is_assigned_emp_2 = fields.Boolean('Is Assigned Emp2', compute='_check_user2_has', default=False)
    is_dh = fields.Boolean('Is Dep Head', compute='_check_userhas', default=False)
    is_content_writer = fields.Boolean('Is Content Writer', related='course_frame_id.is_content_writer')
    is_team_lead = fields.Boolean('Is TL',related='course_frame_id.is_team_lead')
    is_academic_head = fields.Boolean('Is AH', related='course_frame_id.is_academic_head')
    is_ass_dean = fields.Boolean('Is AD', related='course_frame_id.is_ass_dean')
    is_managing_dir = fields.Boolean('Is MD', related='course_frame_id.is_managing_dir')

    def action_open_content_development_form(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('course_frame.content_development_action_window')
        action.update({
            'view_mode': 'form',
            'view_id': self.env.ref('course_frame.view_content_development_form').id,
            'views': [(self.env.ref('course_frame.view_content_development_form').id, 'form')],
            'res_id': self.id,
        })
        return action

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('content.development') or _('New')
        request = super(ContentDevelopment, self).create(vals)
        return request

    def content_action_assign(self):
        for data in self:
            if not data.employee_1_id:
                raise UserError(_("Please select the employee."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.employee_1_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.employee_1_id.user_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' assigns the content development for book format ' + data.name + '. And assigned it to you Please do the needful.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_1': 'assigned'})

    def action_content_submitted_to_tl(self):
        for data in self:
            if not data.book_format_content:
                raise UserError(_("Please upload the Content."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.course_frame_id.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.course_frame_id.team_lead_id.name + ', ' + data.employee_1_id.user_id.name + ' uploads the content against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_1': 'submitted_to_tl'})

    def content_action_tl_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.course_frame_id.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            print(data.course_frame_id.team_lead_id.name, data.employee_1_id.user_id.name)
            body = _(
                u'Hello ' + data.course_frame_id.academic_head_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' Approves the content request against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_1': 'tl_approved',
                               'remarks': False})

    def content_action_tl_reject(self):
        for data in self:
            if not data.remarks:
                raise UserError(_("Please enter the reject reason in remarks."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.course_frame_id.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            print(data.course_frame_id.team_lead_id.name, data.employee_1_id.user_id.name)
            body = _(
                u'Hello ' + data.employee_1_id.user_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' rejects the content request ' + data.name + ' due to ' + data.remarks + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_1': 'rejected_by_tl'})

    def content_action_ah_approve(self):
        for data in self:
            return data.write({'stage_1': 'approved',
                               'state': 'alignment_dtp_work',
                               'remarks': False})

    def content_action_ah_reject(self):
        for data in self:
            if not data.remarks:
                raise UserError(_("Please enter the reject reason in remarks."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'media.reques')]).ids
            for user in data.course_frame_id.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.course_frame_id.team_lead_id.name + ', ' + data.course_frame_id.academic_head_id.name + ' rejects the content request ' + data.name + ' due to ' + data.remarks + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_1': 'reject'})

    def alignment_action_assign(self):
        for data in self:
            # if not data.employee_2_id:
            #     raise UserError(_("Please select the employee."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.department_head_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.department_head_id.user_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' assigns the "Book Content allignment DTP work" ' + data.name + '. And assigned it to you Please do the needful.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_2': 'assigned'})

    def alignment_action_assign_emp(self):
        for data in self:
            if not data.employee_2_id:
                raise UserError(_("Please select the employee."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.employee_2_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.employee_2_id.user_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' assigns the "Book Content allignment DTP work" ' + data.name + '. And assigned it to you Please do the needful.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_2': 'assigned_emp'})

    def alignment_content_submitted_to_dh(self):
        for data in self:
            if not data.dtp_content:
                raise UserError(_("Please upload the Aligned Document."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.department_head_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.department_head_id.user_id.name + ', ' + data.employee_2_id.user_id.name + ' uploads the aligned document against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_2': 'submitted_to_dh',
                               'remarks': False})

    def alignment_action_dh_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.course_frame_id.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            print(data.course_frame_id.team_lead_id.name, data.employee_1_id.user_id.name)
            body = _(
                u'Hello ' + data.course_frame_id.academic_head_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' Approves the content request against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_2': 'dh_approved',
                               'remarks': False})

    def content_action_dh_reject(self):
        for data in self:
            if not data.remarks:
                raise UserError(_("Please enter the reject reason in remarks."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.employee_1_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            print(data.course_frame_id.team_lead_id.name, data.employee_1_id.user_id.name)
            body = _(
                u'Hello ' + data.employee_1_id.user_id.name + ', ' + data.department_head_id.user_id.name + ' rejects the aligned document request ' + data.name + ' due to ' + data.remarks + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_2': 'rejected_by_dh'})

    def alignment_action_ah_approve(self):
        for data in self:
            return data.write({'stage_2': 'ah_approved',
                               'state': 'vetting_external',
                               'remarks': False})

    def alignment_action_ah_reject(self):
        for data in self:
            if not data.remarks:
                raise UserError(_("Please enter the reject reason in remarks."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.department_head_id.user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.department_head_id.user_id.name + ', ' + data.course_frame_id.academic_head_id.name + ' rejects the aligned document request ' + data.name + ' due to ' + data.remarks + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_2': 'ah_rejected'})

    def vetting_content_send_to_receiver(self):
        for data in self:
            if not data.vetting_content:
                raise UserError(_("Please upload the vetting document."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.receive_user_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.receive_user_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' Send the "Book Content allignment DTP work" ' + data.name + '. Please Check and Resend.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_3': 'send'})

    def vetting_content_send_to_ah(self):
        for data in self:
            if not data.receive_user_id:
                raise UserError(_("Please select the receiver."))
            if not data.vetting_content_checked:
                raise UserError(_("Please upload the checked vetting document."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.course_frame_id.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.course_frame_id.academic_head_id.name + ', ' + data.course_frame_id.team_lead_id.name + ' Send the "Book Content allignment DTP work" ' + data.name + '. Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_3': 'submitted',
                               'remarks': False})

    def vetting_content_approved_by_ah(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.course_frame_id.managing_director_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.course_frame_id.managing_director_id.name + ', ' + data.course_frame_id.academic_head_id.name + ' Approves the "Book Content Verification" " ' + data.name + ' and submitted to you. Please Check and approve')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_3': 'approved',
                               'state': 'book_verification',
                               'remarks': False})

    def vetting_content_rejected_by_ah(self):
        for data in self:
            if not data.remarks:
                raise UserError(_("Please enter the reject reason in remarks."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.course_frame_id.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.course_frame_id.team_lead_id.name + ', ' + data.course_frame_id.academic_head_id.name + ' Rejects the "Book Content allignment DTP work" ' + data.name + ' Due to ' + data.remarks + ' .')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_3': 'reject'})

    def vetting_content_approved_by_md(self):
        for data in self:
            for data in self:
                return data.write({'stage_4': 'approve',
                                   'remarks': False})

    def vetting_content_rejected_by_md(self):
        for data in self:
            if not data.remarks:
                raise UserError(_("Please enter the reject reason in remarks."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'content.development')]).ids
            for user in data.course_frame_id.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.course_frame_id.team_lead_id.name + ', ' + data.course_frame_id.managing_director_id.name + ' Rejects the "Book Content Verification" ' + data.name + ' Due to ' + data.remarks + ' .')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'stage_3': 'reject'})
