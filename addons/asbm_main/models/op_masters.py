# -*- coding: utf-8 -*-

from odoo import models, fields, api

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

