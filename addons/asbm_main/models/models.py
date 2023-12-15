# -*- coding: utf-8 -*-

from odoo import models, fields, api


class courseFrame(models.Model):
    _name = 'course.frame'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = 'Subject Frame'

    def _get_group_users(self):
        users = []
        users += self.env.ref('asbm_main.group_asbm_it').users.partner_id.ids + self.env.ref('asbm_main.group_asbm_admission').users.partner_id.ids + self.env.ref('account.group_account_invoice').users.partner_id.ids
        return list(set(users))
    def action_draft(self):
        self.state = 'draft'
        self.it_verified = False
        self.account_verified = False
        self.admission_verified = False
    def action_submit(self):
        self.state = 'in_verification'
        users = self._get_group_users()
        self.message_post_with_view('asbm_main.mail_notification_template_for_verification',
        values={'courseFrameName':self.name},
        partner_ids = [(4, p) for p in users],

        )

    def action_it_verification(self):
        self.it_verified = True
        self.get_verification_status()

    def action_account_verification(self):
        self.account_verified = True
        self.get_verification_status()

    def action_admission_verification(self):
        self.admission_verified = True
        self.get_verification_status()

    def action_md_verification(self):
        self.state = 'verified'
        project_id = self.env['project.project'].create({
        'name':self.name,
        'course_frame_id':self.id
        })
        users = self._get_group_users()
        self.message_post_with_view('asbm_main.mail_template_md_approval',
            values={'userName':self.user_id.name,'courseFrameName':self.name},
            partner_ids = [(4, p) for p in users]
            )
        self.project_id = project_id.id

    # @api.depends('it_verified','account_verified','admission_verified')
    def get_verification_status(self):
        if self.it_verified and self.account_verified and self.admission_verified:
            self.state = 'md_verification'




    name = fields.Char(string="Preferable Course Name", required=True)
    # suitable_for = fields.Char(string="Course is suitable for (Over view)")
    # type = fields.Selection([('subject','Subject'),
    #     ('specialization','Specialization')],string="Type")
    age_categories_if_any = fields.Char(string="Age categories if any")
    experience_required = fields.Char(string="Experience Required")
    documents_preferred_for_admission = fields.Char(string="Documents preferred for admission")
    regular = fields.Char(string="Regular")
    fast_track = fields.Char(string="Fast Track")
    emergency = fields.Char(string="Emergency")
    super_emergency = fields.Char(string="Super Emergency")
    preferred_regions = fields.Char(string="Preferred Regions")

    preferred_branch = fields.Char(string = "Preferred Branch")
    version = fields.Char(string = "Version")
    course_fees = fields.Char(string = "Course Fees")
    tax_percentage_details_can_be_added = fields.Char(string = "Tax Percentage (Details can be added)")
    course_materials_types = fields.Char(string = "Course Materials types")
    available_exam_modes = fields.Char(string = "Available Exam Modes")
    total_subjects_and_marks_preferred = fields.Char(string = "Total Subjects and marks preferred")
    total_specializations_and_marks_preferred = fields.Char(string = "Total Specializations and marks preferred")
    total_case_studies_and_marks_preferred = fields.Char(string = "Total Case studies and marks preferred")
    total_projects_and_marks_preferred = fields.Char(string = "Total Projects and marks Preferred")
    total_assignments_and_marks_preferred = fields.Char(string = "Total Assignments and marks preferred")
    total_gd_and_marks_preferred = fields.Char(string = "Total GD and marks preferred")
    total_points_to_be_calculated_for_awards = fields.Char(string = "Total Points to be calculated for awards")
    total_internal_marks_can_be_given = fields.Char(string = "Total internal marks can be given")
    define_grade_system_short_note = fields.Char(string = "Define Grade system (Short note)")
    add_an_existing_grading_system = fields.Boolean(string="Add an existing Grading System")
    cost_estimation = fields.Char(string="Cost Estimation")
    title_content_preparation_external = fields.Char(string="Title content Preparation (External)")
    title_quiz_assignments_and_answers = fields.Char(string="Title Quiz, Assignments and answers")
    vetting = fields.Char(string="Vetting")
    alignment = fields.Char(string="Alignment")
    design_works = fields.Char(string="Design Works")
    printing_cost = fields.Char(string="Printing Cost")
    technical_cost = fields.Char(string="Technical Cost")
    internal_manpower_cost = fields.Char(string="Internal Manpower cost")
    total_man_days_required = fields.Char(string="Total Man Days required")
    can_be_use_existing_course_contents = fields.Boolean(string="Can be use existing course contents")
    topic_based_data_filtering = fields.Boolean(string="Topic Based Data Filtering")
    user_id = fields.Many2one('res.users',string="Associate Dean",default= lambda x: x.env.user.id)
    # subject_display_system_ids = fields.One2many('subject.display.system','course_frame_id',string="Subject display system")
    subject_specialization_ids = fields.Many2many('subject.specialization',string="Subject frame details")
    # subject_ids = fields.Many2many('op.subject',string='Subjects')
    # specialization_ids = fields.Many2many('op.specialization',string='Subjects')

    state = fields.Selection([('draft','Draft'),
        ('in_verification','Waiting for Verification'),
        ('md_verification','Waiting for MD Verification'),
        ('verified','Verified')],
        string="State", default='draft')
    it_verified = fields.Boolean(string='IT Verified')
    account_verified = fields.Boolean(string='Accounts Verified')
    admission_verified = fields.Boolean(string='Admission Verified')
    project_id = fields.Many2one('project.project',string="Project")

    company_id = fields.Many2one('res.company', string="Company", required=True)

    # default = lambda x:x.env.company)

    @api.model
    def create(self, vals):
        if self.env.context.get('flag_company_value'):
            if 'company_id' in vals:
                vals['company_id'] = self.env.company.id
                # vals.update({
                #     'company_id': self.env.company
                # })
        context = dict(self.env.context)
        if 'flag_company_value' in context:
            del context['flag_company_value']
        self.env.context = context
        return super(courseFrame, self).create(vals)

    def write(self, vals):
        if vals.get('company_id') or 'company_id' in vals:
            vals['company_id'] = self.env.company.id
            # for i in self:
            # self.company_id = self.env.company.id
        return super(courseFrame, self).write(vals)


class ShowingAs(models.Model):
    _name = 'showing.as'
    _inherit = ['mail.thread']
    _description = 'Showing As'

    name = fields.Char(string='Showing as', required=True)

class ShowingIn(models.Model):
    _name = 'showing.in'
    _inherit = ['mail.thread']
    _description = 'Showing In'

    name = fields.Char(string='Showing in', required=True)
class subjectSpecialization(models.Model):
    _name = 'subject.specialization'
    _description = 'Subject Specialization details'

    name = fields.Char(string="Name",required=True)
    code = fields.Char(string="Code",required=True)
    type = fields.Selection([('subject','Subject'),
        ('specialization','Specialization'),
        ('project','Project'),
        ('case_study','Case study')],
        string="Type",required=True)

    marks_in = fields.Char(string="Marks in")
    showing_as = fields.Many2one('showing.as',string="Showing as")
    showing_in = fields.Many2one('showing.in',string="Showing in")
    position = fields.Char(string="Position")
    show_in_main_sheet = fields.Boolean(default="True",string="Show in main sheet")
    show_in_mark_sheet = fields.Boolean(default="True",string="Show in mark sheet")
    show_in_consolidated = fields.Boolean(default="True",string="Show in Consolidated")

    grade_weightage = fields.Float('Grade Weightage')
    specialization_type = fields.Selection(
        [('theory', 'Theory'), ('practical', 'Practical'),
         ('both', 'Both'), ('other', 'Other')],
        'Type', default="theory", required=False)
    subject_type = fields.Selection(
        [('compulsory', 'Compulsory'), ('elective', 'Elective')],
        'Mode of Examination', default="compulsory", required=False)

    category = fields.Selection(
        [('specialization', 'Specialization'),('group', 'Group')],
        'Category', default="specialization", required=False)


    # course_frame_id = fields.Many2one('course.frame',string="Subject frame")
    specialization_id = fields.Many2one('op.specialization',string='Specialization')
    subject_id = fields.Many2one('op.subject',string="Subject")
    project_id = fields.Many2one('op.project',string="Project")
    case_study_id = fields.Many2one('op.case.study',string="Case Study")

class Project(models.Model):
    _name = 'op.project'
    _description = 'Project'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    marks_in = fields.Char(string="Marks in")
    showing_as = fields.Many2one('showing.as', string="Showing as")
    showing_in = fields.Many2one('showing.in', string="Showing in")
    position = fields.Char(string="Position")
    show_in_main_sheet = fields.Boolean(default="True", string="Show in main sheet")
    show_in_mark_sheet = fields.Boolean(default="True", string="Show in mark sheet")
    show_in_consolidated = fields.Boolean(default="True", string="Show in Consolidated")

class CaseStudy(models.Model):
    _name = 'op.case.study'
    _description = 'Case Study'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    marks_in = fields.Char(string="Marks in")
    showing_as = fields.Many2one('showing.as', string="Showing as")
    showing_in = fields.Many2one('showing.in', string="Showing in")
    position = fields.Char(string="Position")
    show_in_main_sheet = fields.Boolean(default="True", string="Show in main sheet")
    show_in_mark_sheet = fields.Boolean(default="True", string="Show in mark sheet")
    show_in_consolidated = fields.Boolean(default="True", string="Show in Consolidated")


# class subjectDisplaySystem(models.Model):
#     _name = 'subject.display.system'
#     _description = 'Subject display system'
#
#     name = fields.Char(string="Title name & code", required=True)
#     title_used_as = fields.Char(string="Title Used as")
#     marks_in = fields.Char(string="Marks in")
#     showing_as = fields.Char(string="Showing as")
#     showing_in = fields.Char(string="Showing in")
#     position = fields.Char(string="Position")
#     show_in_main_sheet = fields.Char(string="Show in main sheet")
#     show_in_mark_sheet = fields.Char(string="Show in mark sheet")
#     show_in_consolidated = fields.Char(string="Show in Consolidated")
#     course_frame_id = fields.Many2one('course.frame',string="Course frame")
