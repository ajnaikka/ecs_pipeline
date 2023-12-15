# -*- code:utf-8 -*-
from odoo import models,fields,api,_
from odoo.exceptions import UserError

class Course(models.Model):
    _inherit = 'op.course'

    project_course_ids = fields.Many2many('op.project',string='Projects')
    case_study_course_ids = fields.Many2many('op.case.study',string='Case Study')

    name = fields.Char(string="Preferable Course Name", required=True)
    # suitable_for = fields.Char(string="Course is suitable for (Over view)")
    type = fields.Selection([('subject','Subject'),
        ('specialization','Specialization')],string="Type")
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
