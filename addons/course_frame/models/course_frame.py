# -*- coding: utf-8 -*-
from datetime import date, datetime, time

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError


class CourseFrame(models.Model):
    _name = 'course.frame'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Course Frame'

    name = fields.Char('Course Name', copy=False, tracking=True, required=True)
    course_code = fields.Char('Course Code', copy=False, tracking=True)
    stages = fields.Selection([('course_subject_selection', 'Course and Subject Suggestion'),
                               ('freasing_stage', 'Freezing Stage'), ('toc_syllabas', 'TOC & Syllabus Development'),
                               ('course_development', 'Cours Re Development'),
                               ('study_material', 'Study materials into Software')], copy=False, tracking=True,
                              default='course_subject_selection', group_expand='_expand_states')
    state = fields.Selection(
        [('draft', 'Draft'), ('assigned_cw', 'Assigned to CW'), ('submitted_tl', 'Submitted To TL'),
         ('submitted_to_ah', 'TL Approved'), ('submitted_dean', 'AH Approved'),
         ('submitted_director', 'AD Approved'), ('approved', 'Director Approved'), ('reject_by_tl', 'TL Rejected'),
         ('reject_by_ah', 'AH Rejected'),
         ('rejected_by_dean', 'AD Rejected'), ('rejected_by_director', 'Director Rejected')], copy=False, tracking=True,
        default='draft')
    freezing_state = fields.Selection(
        [('draft', 'Draft'), ('submitted_to_ah', 'Submitted To AH'), ('submitted_to_account', 'Submitted To Accounts'),
         ('submitted_to_director', 'Submitted To Director'), ('approved', 'Director Approved'),
         ('reject_by_ah', 'AH Rejected'), ('reject_by_accounts', 'Accounts Rejected'),
         ('rejected_by_director', 'Director Rejected')], copy=False, tracking=True, default='draft')
    freezing_states = fields.Selection([('freez', 'Freez'), ('unfreez', 'Unfreezed')], string='Stages', copy=False,
                                       default='unfreez')

    toc_stage = fields.Selection([('draft', 'Draft'), ('submitted_tl', 'Submitted To TL'),
                                  ('submitted_to_ah', 'TL Approved'), ('submitted_dean', 'AH Approved'),
                                  ('submitted_director', 'AD Approved'), ('approved', 'Director Approved'),
                                  ('reject_by_tl', 'TL Rejected'),
                                  ('reject_by_ah', 'AH Rejected'),
                                  ('rejected_by_dean', 'AD Rejected'), ('rejected_by_director', 'Director Rejected')],
                                 string='Stages', copy=False,
                                 default='draft')

    syllabus_stage = fields.Selection([('draft', 'Draft'), ('submitted_tl', 'Submitted To TL'),
                                       ('submitted_to_ah', 'TL Approved'), ('submitted_dean', 'AH Approved'),
                                       ('submitted_director', 'AD Approved'), ('approved', 'Director Approved'),
                                       ('reject_by_tl', 'TL Rejected'),
                                       ('reject_by_ah', 'AH Rejected'),
                                       ('rejected_by_dean', 'AD Rejected'),
                                       ('rejected_by_director', 'Director Rejected')], string='Stages', copy=False,
                                      default='draft')

    subject_id = fields.Many2one('op.subject', 'Subject', copy=True, tracking=True, )
    grade_id = fields.Many2one('subject.grade', 'Grade', copy=True, tracking=True, )
    specialisation_id = fields.Many2one('op.specialization', 'Specialisation', copy=True, tracking=True, )
    learning_platform_id = fields.Many2one('learning.platform', 'Course Learning Platform', copy=True, tracking=True, )
    # course_tag_ids = fields.Many2many('course.tag','course_tag_id', 'Course Categories',)
    course_tags_ids = fields.Many2many('course.tag', 'course_tag_rel', 'tag_id', 'course_id',
                                       'Course Categories')
    job_tags_ids = fields.Many2many('course.tag', 'job_tag_rel', 'tag_id', 'job_id', 'Job Categories', )
    course_overview = fields.Text('Course Overview', copy=True, tracking=True, )
    course_overview_video = fields.Char('Course Overview Video Link')
    course_type_id = fields.Many2one('op.course.type', 'Certificate Type', copy=True, tracking=True, )
    certificate_version = fields.Date('Certificate Version', copy=True, tracking=True, )
    # course_fee_id = fields.Many2one('course.fee', 'Course Fee Structure', copy=True, tracking=True, )
    course_fee_id = fields.Many2one('op.fees.terms', 'Fees Term', copy=True, tracking=True,required=True )
    course_fee = fields.Float('Course Fee', copy=True, tracking=True, )
    course_learning_hours = fields.Float('Total Course Learning Hrs', copy=True, tracking=True, )
    # course_mode_id = fields.Many2one('course.mode', 'Course Mode', copy=True, tracking=True, )
    eligibility = fields.Char('Eligibility', copy=True, tracking=True, )
    qualification = fields.Char('Qualification', copy=True, tracking=True, )
    additional_skills = fields.Text('Additional Skills', copy=True, tracking=True, )
    experience_required = fields.Text('Experience Required', copy=True, tracking=True, )
    minimum_years = fields.Integer('Minimum Year', copy=True, tracking=True, )
    maximum_years = fields.Integer('Maximum Year', copy=True, tracking=True, )
    course_mode_type = fields.Many2one('course.mode.type', 'Course Mode', copy=True, tracking=True, )
    course_duration = fields.Integer('Course Duration', copy=True, tracking=True, )
    duration_type = fields.Selection([('month', 'Month'), ('year', 'Year')],
                                     string='Month/Year')
    total_score = fields.Float('Total Score', copy=True, tracking=True, )
    preferred_region = fields.Char('Preferred Region', copy=True, tracking=True, )
    preferred_branch = fields.Selection([('management', 'Management'), ('technical', 'Technical')],
                                        string='Preferred Branch', )
    grading_version = fields.Date('Grading Version')
    version_from = fields.Date('Version From')
    version_to = fields.Date('Version To')
    is_main_project = fields.Boolean('Main Project')
    project_name_main = fields.Char('Project')
    project_score_main = fields.Float('Total Marks Preferred')
    is_mini_project = fields.Boolean('Mini Project')
    project_name_mini = fields.Char('Project')
    project_score_mini = fields.Float('Total Marks Preferred')
    is_case_study = fields.Boolean('Case Study')
    is_course_created = fields.Boolean('Course Created', default=False)
    is_lms_created = fields.Boolean('LMS Created', default=False)
    case_study = fields.Char('Case Name')
    case_study_score = fields.Float('Total Marks Preferred')
    subject_count = fields.Float('Total No of Sub')
    category = fields.Char('Course tag/Category')
    study_material_type_id = fields.Many2one('study.material.type', 'Study material type')
    team_lead_id = fields.Many2one('res.users', 'Team Lead', copy=True, tracking=True,
                                   default=lambda self: self.env.user,
                                   domain=lambda self: [
                                       ("groups_id", "=", self.env.ref("course_frame.group_academy_team_lead").id)])
    content_writer_id = fields.Many2one('res.users', 'Content Writer', copy=True, tracking=True, required=True,
                                        domain=lambda self: [("groups_id", "=", self.env.ref(
                                            "course_frame.group_academy_content_writer").id)])
    academic_head_id = fields.Many2one('res.users', 'Academic Head', copy=True, tracking=True, required=True,
                                       domain=lambda self: [("groups_id", "=", self.env.ref(
                                           "course_frame.group_academy_academy_head").id)])
    asso_dean_id = fields.Many2one('res.users', 'Associate Dean', copy=True, tracking=True, required=True,
                                   domain=lambda self: [("groups_id", "=", self.env.ref(
                                       "course_frame.group_academy_associate_dean").id)])
    managing_director_id = fields.Many2one('res.users', 'Managing Director', copy=True, tracking=True, required=True,
                                           domain=lambda self: [("groups_id", "=", self.env.ref(
                                               "course_frame.group_academy_director").id)])
    accountant_id = fields.Many2one('res.users', 'Accounts Head', copy=True, tracking=True, required=True,
                                    domain=lambda self: [("groups_id", "=", self.env.ref(
                                        "account.group_account_manager").id)])
    grading_line = fields.One2many('grading.system.line', 'course_id', string='Grading System')
    subject_line = fields.One2many('course.subject.line', 'course_id', string='Subjects')
    course_fee_line = fields.One2many('course.fee.structure', 'course_id', string='Course Fee')
    reason = fields.Text('Reason', copy=True, tracking=True)
    color = fields.Integer('Colour Index')

    # budget
    total_man_days = fields.Integer('Total Man Days Required')
    budget_line = fields.One2many('course.budget.line', 'course_id', string='Budgeting')
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)
    amount_total = fields.Monetary('Total Amount', store=True, compute='_compute_amounts', tracking=4)

    # TOC & Syllabas Development

    toc_lines = fields.One2many('course.toc.line', 'course_id', string='TOC Uploading')
    syllabus_lines = fields.One2many('course.syllabus.line', 'course_id', string='Syllabus Development')

    # Course Re-Development
    request_count = fields.Integer(compute='compute_media_request_count')
    media_request_lines = fields.One2many('media.request','course_frame_id')
    content_development_lines = fields.One2many('content.development','course_frame_id')

    is_content_writer = fields.Boolean('Is Content Writer', compute='_check_content_writer', default=False)
    is_team_lead = fields.Boolean('Is TL', compute='_check_team_lead', default=False)
    is_academic_head = fields.Boolean('Is AH', compute='_check_academic_head', default=False)
    is_ass_dean = fields.Boolean('Is AD', compute='_check_asso_dean', default=False)
    is_managing_dir = fields.Boolean('Is MD', compute='_check_managing_director', default=False)
    is_accounts_head = fields.Boolean('Is Acc Head', compute='_check_accounts_head', default=False)


    @api.onchange('grade_id')
    def onchange_grade_id(self):
        for data in self:
            if data.grade_id:
                data.grading_line = False
                lines = []
                for rec in data.grade_id.grade_lines:
                    vals = {
                        'name': rec.name,
                        'grade': rec.grade,
                        'performance':rec.performance,
                        'grade_point':rec.grade_point,
                    }
                    lines.append((0,0,vals))
                data.grading_line = lines
            else:
                data.grading_line = False


    def _check_content_writer(self):
        for data in self:
            if data.content_writer_id.id == self.env.user.id:
                data.is_content_writer = True
            else:
                data.is_content_writer = False

    def _check_team_lead(self):
        for data in self:
            if data.team_lead_id.id == self.env.user.id:
                data.is_team_lead = True
            else:
                data.is_team_lead = False

    def _check_academic_head(self):
        for data in self:
            if data.academic_head_id.id == self.env.user.id:
                data.is_academic_head = True
            else:
                data.is_academic_head = False

    def _check_asso_dean(self):
        for data in self:
            if data.asso_dean_id.id == self.env.user.id:
                data.is_ass_dean = True
            else:
                data.is_ass_dean = False

    def _check_managing_director(self):
        for data in self:
            if data.managing_director_id.id == self.env.user.id:
                data.is_managing_dir = True
            else:
                data.is_managing_dir = False

    def _check_accounts_head(self):
        for data in self:
            if data.accountant_id.id == self.env.user.id:
                data.is_accounts_head = True
            else:
                data.is_accounts_head  = False






    def compute_media_request_count(self):
        for data in self:
            query = self.env['media.request'].search([('course_frame_id','=',data.id)])
            data.request_count = len(query)




    def action_create_media_request(self):
        request = self.env['media.request'].create({
            'course_frame_id': self.id,
            'date': date.today(),})
        return {
            'name': 'Media Request',
            'domain': [('course_frame_id', 'in', [self.id])],
            'context': {'search_default_course_frame_id': self.id},
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'media.request',
            'type': 'ir.actions.act_window',
        }

    def action_open_course_frame_wizard(self):
        if self.freezing_states == 'freez':
            raise AccessError(_("Unfreeze course frame before creating course"))
        if not self.media_request_lines or not self.content_development_lines:
            raise ValidationError(_("Please add media request and book content"))
        if self.media_request_lines and any(self.media_request_lines.filtered(lambda l: l.state != 'approved')):
            raise ValidationError(_("Please approve all media request before creating course"))
        if self.content_development_lines and any(self.content_development_lines.filtered(lambda l: l.state != 'book_verification' or l.stage_4 != 'approve')):
            raise ValidationError(_("Please approve all book content before creating course"))
        return {
            'name': _('Course Frame Wizard'),
            'type': 'ir.actions.act_window',
            'context': {'default_course_frame_id': self.id, 'default_user_id': self.env.user.id},
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'course.frame.wizard',
            'target': 'new',
        }

    def action_move_to_study_material(self):
        for data in self:
            data.stages = 'study_material'
            data.freezing_states = 'freez'

    def action_reject_back_study_material_to_development(self):
        for data in self:
            data.stages = 'course_development'

    def change_location(self):
        view = self.env.ref('fair_construction.view_change_dest_location')
        wiz = self.env['change.dest.location'].create({'location_dest_id': self.location_dest_id.id,
                                                       'picking_id': self.id})
        # TDE FIXME: a return in a loop, what a good idea. Really.
        return {
            'name': _('Change Destination Location'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'change.dest.location',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }



    def action_view_media_request(self):
        '''media request button clicking action'''

        return {
            'name': 'Media Request',
            'domain': [('course_frame_id', 'in', [self.id])],
            'context': {'search_default_course_frame_id': self.id},
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'media.request',
            'type': 'ir.actions.act_window',
        }

    def _expand_states(self, stages, domain, order):
        return [key for key, val in type(self).stages.selection]

    @api.depends('budget_line.cost')
    def _compute_amounts(self):
        for data in self:
            amount_total = 0
            for line in data.budget_line:
                amount_total += line.cost
            data.amount_total = amount_total

    def action_freez(self):
        for data in self:
            data.freezing_states = 'freez'

    def action_unfreez(self):
        for data in self:
            data.freezing_states = 'unfreez'

    # -------------------------------------------------------------------------------------------------------------------------------------------------
    #     Course and Subject Suggestion
    # -------------------------------------------------------------------------------------------------------------------------------------------------
    def action_assign(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.content_writer_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.content_writer_id.name + ', ' + data.team_lead_id.name + ' creates the course frame ' + data.name + '. And assigned it to you Please Fill and Send Back.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'assigned_cw'})

    def action_submitted(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.team_lead_id.name + ', ' + data.content_writer_id.name + ' fills the details of the course frame ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'submitted_tl',
                               'reason': False})

    def action_tl_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.academic_head_id.name + ', ' + data.team_lead_id.name + ' approves the course frame ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'submitted_to_ah',
                               'reason': False})

    def action_tl_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.content_writer_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.content_writer_id.name + ', ' + data.team_lead_id.name + ' Rejected the course frame ' + data.name + 'due to , ' + data.reason + ' . Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'reject_by_tl', })

    def action_ah_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.asso_dean_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.asso_dean_id.name + ', ' + data.academic_head_id.name + ' Approves the course frame ' + data.name + '. Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'submitted_dean',
                               'reason': False})

    def action_ah_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.team_lead_id.name + ', ' + data.academic_head_id.name + ' Rejected the course frame ' + data.name + 'due to , ' + data.reason + ' . Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'reject_by_ah'})

    def action_asso_dean_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.managing_director_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.managing_director_id.name + ', ' + data.asso_dean_id.name + ' Approves the course frame ' + data.name + '. Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'submitted_director',
                               'reason': False})

    def action_asso_dean_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.academic_head_id.name + ', ' + data.asso_dean_id.name + ' Rejected the course frame ' + data.name + 'due to , ' + data.reason + ' . Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'rejected_by_dean'})

    def action_director_approve(self):
        for data in self:
            # partners = []
            # subtype_ids = self.env['mail.message.subtype'].search(
            #     [('res_model', '=', 'course.frame')]).ids
            # for user in data.managing_director_id:
            #     self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
            #     partners.append(user.partner_id.id)
            # body = _(
            #     u'Hello ' + data.managing_director_id.name + ', ' + data.academic_head_id.name + ' Rejected the course frame ' + data.name + 'due to , ' + data.reason + ' . Please Check and Resubmit.')
            # data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'approved',
                               'stages': 'freasing_stage',
                               })

    def action_reject_back_freezing_to_course_subject(self):
        for data in self:
            return data.write({'state': 'submitted_director',
                               'stages': 'course_subject_selection',
                               })

    def action_director_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.asso_dean_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.asso_dean_id.name + ', ' + data.managing_director_id.name + ' Rejected the course frame ' + data.name + 'due to , ' + data.reason + ' . Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'rejected_by_director'})

    # --------------------------------------------------------------------------------------------------------------------------------
    # Freezing Stages
    # --------------------------------------------------------------------------------------------------------------------------------


    def action_submitted_to_ah(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.academic_head_id.name + ', ' + data.team_lead_id.name + ' fill the budget ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'freezing_state': 'submitted_to_ah',
                               'reason': False})

    def action_submitted_to_account(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.accountant_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.accountant_id.name + ', ' + data.academic_head_id.name + ' approves the budget ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'freezing_state': 'submitted_to_account',
                               'reason': False})

    def action_budget_rejected_by_ah(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.team_lead_id.name + ', ' + data.academic_head_id.name + ' rejects the budget ' + data.name + '. Due to ' + data.reason + ' Please Check and Re-approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'freezing_state': 'reject_by_ah'})

    def action_submitted_to_director(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.managing_director_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.managing_director_id.name + ', ' + data.accountant_id.name + ' approves the budget ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'freezing_state': 'submitted_to_director',
                               'reason': False})

    def action_budget_rejected_by_accountant(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.academic_head_id.name + ', ' + data.accountant_id.name + ' rejects the budget ' + data.name + '. Due to ' + data.reason + ' Please Check and Re-approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'freezing_state': 'reject_by_accounts'})


    # test button to go anywhere
    def action_to_freeze(self):
        for data in self:
            data.stages='freasing_stage'
            data.freezing_state='submitted_to_director'

    def action_budget_director_approve(self):
        for data in self:
            return data.write({'freezing_state': 'approved',
                               'stages': 'toc_syllabas',
                               'freezing_states': 'freez',
                               })

    def action_budget_rejected_by_director(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.accountant_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.accountant_id.name + ', ' + data.managing_director_id.name + ' rejects the budget ' + data.name + '. Due to ' + data.reason + ' Please Check and Re-approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'freezing_state': 'rejected_by_director'})

    def action_reject_back_toc_syllabas_to_freazing_stage(self):
        for data in self:
            return data.write({'freezing_state': 'submitted_to_director',
                               'stages': 'freasing_stage',
                               'freezing_states': 'unfreez',
                               })

    # ____________________________________________________________________
    # TOC Uploading
    # ____________________________________________________________________

    def action_reject_toc_to_freeze(self):
        for data in self:
            if data.stages == 'toc_syllabas':
                if not data.reason:
                    raise UserError(_("Please Fill the reject Reason."))
                partners = []
                subtype_ids = self.env['mail.message.subtype'].search(
                    [('res_model', '=', 'course.frame')]).ids
                for user in data.asso_dean_id:
                    self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                    partners.append(user.partner_id.id)
                body = _(
                    u'Hello ' + data.asso_dean_id.name + ', ' + data.managing_director_id.name + ' Rejected the course frame ' + data.name + 'due to , ' + data.reason + ' . Please Check and Resubmit.')
                data.message_post(body=body, partner_ids=partners)
                return data.write({'freezing_state': 'submitted_to_director',
                                   'freezing_states': 'unfreez',
                                   'stages': 'freasing_stage'})


    def action_toc_submitted(self):
        for data in self:
            if data.freezing_states == 'freez':
                raise AccessError(_("Unfreeze course frame before submitting TOC"))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.team_lead_id.name + ', ' + data.content_writer_id.name + ' uploads the toc document against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'toc_stage': 'submitted_tl',
                               'reason': False})

    def action_tl_toc_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.academic_head_id.name + ', ' + data.team_lead_id.name + ' approves the TOC documents against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'toc_stage': 'submitted_to_ah',
                               'reason': False})

    def action_tl_toc_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.content_writer_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.content_writer_id.name + ', ' + data.team_lead_id.name + ' Rejected the TOC documents against ' + data.name + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'toc_stage': 'reject_by_tl', })

    def action_ah_toc_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.asso_dean_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.asso_dean_id.name + ', ' + data.academic_head_id.name + ' Approves the TOC documents against ' + data.name + '. Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'toc_stage': 'submitted_dean',
                               'reason': False})

    def action_ah_toc_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.team_lead_id.name + ', ' + data.academic_head_id.name + ' Rejected the TOC documents against ' + data.name + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'toc_stage': 'reject_by_ah'})

    def action_asso_dean_toc_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.managing_director_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.managing_director_id.name + ', ' + data.asso_dean_id.name + ' Approves the TOC documents against ' + data.name + '. Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'toc_stage': 'submitted_director',
                               'reason': False})

    def action_asso_dean_toc_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.academic_head_id.name + ', ' + data.asso_dean_id.name + ' Rejected theTOC documents against ' + data.name + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'toc_stage': 'rejected_by_dean'})

    def action_director_toc_approve(self):
        for data in self:
            if data.syllabus_stage == 'approved':
                return data.write({'toc_stage': 'approved',
                                   'stages': 'course_development',
                                   'freezing_states': 'freez',
                                   })
            else:
                return data.write({'toc_stage': 'approved',
                                   })

    def action_director_toc_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.asso_dean_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.asso_dean_id.name + ', ' + data.managing_director_id.name + ' Rejected the TOC documents against ' + data.name + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'toc_stage': 'rejected_by_director'})

    # ____________________________________________________________________
    # Syllabus Development
    # ____________________________________________________________________

    def action_reject_redevelopment_to_toc(self):
        for data in self:
            if data.stages == 'course_development':
                if not data.reason:
                    raise UserError(_("Please Fill the reject Reason."))
                partners = []
                subtype_ids = self.env['mail.message.subtype'].search(
                    [('res_model', '=', 'course.frame')]).ids
                for user in data.asso_dean_id:
                    self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                    partners.append(user.partner_id.id)
                body = _(
                    u'Hello ' + data.asso_dean_id.name + ', ' + data.managing_director_id.name + ' Rejected the course frame ' + data.name + 'due to , ' + data.reason + ' . Please Check and Resubmit.')
                data.message_post(body=body, partner_ids=partners)
                return data.write({'toc_stage': 'submitted_director',
                                   'syllabus_stage': 'submitted_director',
                                   'freezing_states': 'unfreez',
                                   'stages': 'toc_syllabas'})

    def action_syllabus_submitted(self):
        for data in self:
            if data.freezing_states == 'freez':
                raise AccessError(_("Unfreeze course frame before submitting syllabus"))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.team_lead_id.name + ', ' + data.content_writer_id.name + ' fills the syllabus documents against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'syllabus_stage': 'submitted_tl',
                               'reason': False})

    def action_tl_syllabus_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.academic_head_id.name + ', ' + data.team_lead_id.name + ' approves the syllabus documents against ' + data.name + '. And submitted to you Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'syllabus_stage': 'submitted_to_ah',
                               'reason': False})

    def action_tl_syllabus_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.content_writer_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.content_writer_id.name + ', ' + data.team_lead_id.name + ' Rejected the syllabus documents against ' + data.name + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'syllabus_stage': 'reject_by_tl', })

    def action_ah_syllabus_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.asso_dean_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.asso_dean_id.name + ', ' + data.academic_head_id.name + ' Approves the syllabus documents against ' + data.name + '. Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'syllabus_stage': 'submitted_dean',
                               'reason': False})

    def action_ah_syllabus_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.team_lead_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.team_lead_id.name + ', ' + data.academic_head_id.name + ' Rejected the syllabus documents against ' + data.name + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'syllabus_stage': 'reject_by_ah'})

    def action_asso_dean_syllabus_approve(self):
        for data in self:
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.managing_director_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.managing_director_id.name + ', ' + data.asso_dean_id.name + ' Approves the syllabus documents against ' + data.name + '. Please Check and Approve.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'syllabus_stage': 'submitted_director',
                               'reason': False})

    def action_asso_dean_syllabus_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.academic_head_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.academic_head_id.name + ', ' + data.asso_dean_id.name + ' Rejected the syllabus documents against ' + data.name + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'syllabus_stage': 'rejected_by_dean'})

    def action_director_syllabus_approve(self):
        for data in self:
            if data.toc_stage == 'approved':
                return data.write({'syllabus_stage': 'approved',
                                   'stages': 'course_development',
                                   'freezing_states': 'freez',
                                   })
            else:
                return data.write({'syllabus_stage': 'approved', })

    def action_director_syllabus_reject(self):
        for data in self:
            if not data.reason:
                raise UserError(_("Please Fill the reject Reason."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'course.frame')]).ids
            for user in data.asso_dean_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.asso_dean_id.name + ', ' + data.managing_director_id.name + ' Rejected the syllabus documents against ' + data.name + '. Please Check and Resubmit.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'syllabus_stage': 'rejected_by_director'})

class GradingSystemLines(models.Model):
    _name = 'grading.system.line'

    course_id = fields.Many2one('course.frame')
    name = fields.Char('Percentage of Marks', required=True)
    grade = fields.Selection(
        [('s', 'S'), ('a+', 'A+'), ('a', 'A'), ('b+', 'B+'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('f', 'F')],
        string='Grade', required=True)
    performance = fields.Char('Performance', required=True)
    grade_point = fields.Integer('Grade Point', required=True)


class CourseSubjectLines(models.Model):
    _name = 'course.subject.line'

    course_id = fields.Many2one('course.frame')
    name = fields.Char('Tittle Name')
    type = fields.Selection([('subject', 'Subject'), ('specialisation', 'Specialisation')], 'Tittle Type',
                            default='subject')
    display_type_id = fields.Many2one('subject.display.details')
    subject_id = fields.Many2one('op.subject')
    specialisation_id = fields.Many2one('op.specialization', 'Specialisation', )
    code = fields.Char('Tittle Code')
    learning_hour = fields.Float('Learning Hr')
    total_marks = fields.Float('Total Marks')
    passing_marks = fields.Float('Passing Marks')
    showing_as_id = fields.Many2one('showing.as', 'Showing As')
    showing_in = fields.Many2one('showing.in', 'Showing In')
    position_is = fields.Many2one('subject.positions', string="Position")

    @api.onchange('type', 'display_type_id', 'subject_id', 'specialisation_id')
    def _onchange_type(self):
        for data in self:
            if data.type == 'subject' and data.subject_id:
                data.code = data.subject_id.code
                data.name = data.subject_id.name
            if data.type == 'specialisation' and data.specialisation_id:
                data.code = data.specialisation_id.code
                data.name = data.specialisation_id.name

class BudgetLines(models.Model):
    _name = 'course.budget.line'

    course_id = fields.Many2one('course.frame')
    budget_id = fields.Many2one('budget.budget', 'Budget Items', required=True)
    cost = fields.Float('Amount', required=True)

class CourseFeeStructure(models.Model):
    _name = 'course.fee.structure'

    course_id = fields.Many2one('course.frame')
    course_fee_id = fields.Many2one('course.fee', 'Course Fee Structure', copy=True, tracking=True, )
    course_fee = fields.Float('Course Fee', copy=True, tracking=True, )

class CourseTocLines(models.Model):
    _name = 'course.toc.line'

    course_id = fields.Many2one('course.frame')
    name = fields.Char('Name')
    subject_id = fields.Many2one('op.subject', required=True)
    remarks = fields.Char('Remarks')
    toc_doc = fields.Binary('TOC Doc',required=True)
    toc_stage = fields.Selection(related='course_id.toc_stage')

class CourseSyllabusLines(models.Model):
    _name = 'course.syllabus.line'

    course_id = fields.Many2one('course.frame')
    name = fields.Char('Name')
    subject_id = fields.Many2one('op.subject', required=True)
    remarks = fields.Char('Remarks')
    syllabus_doc = fields.Binary('Syllabus Doc',required=True)
    syllabus_stage = fields.Selection(related='course_id.syllabus_stage')


class CourseContentLines(models.Model):
    _name = 'course.content.line'

    course_id = fields.Many2one('course.frame')
    name = fields.Char('Name')
    subject_id = fields.Many2one('op.subject', required=True)
    unit_id = fields.Many2one('subject.unit', required=True)
    topic_id = fields.Many2one('subject.topic', required=True)
    remarks = fields.Char('Remarks')
    content = fields.Binary('Syllabus Doc')


class CourseContentAlignmentLines(models.Model):
    _name = 'content.alignment.line'

    course_id = fields.Many2one('course.frame')
    name = fields.Char('Name')
    subject_id = fields.Many2one('op.subject', required=True)
    unit_id = fields.Many2one('subject.unit', required=True)
    topic_id = fields.Many2one('subject.topic', required=True)
    remarks = fields.Char('Remarks')
    content = fields.Binary('Syllabus Doc')
