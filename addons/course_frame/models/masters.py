# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LearningPlatform(models.Model):
    _name = 'learning.platform'
    _description = 'Course Learning Platform'

    name = fields.Char('Platform Name')
    code = fields.Char('Code')


class CourseTag(models.Model):
    _name = 'course.tag'
    _description = 'Course Tag'

    name = fields.Char('Tag Name')
    code = fields.Char('Code')
    type = fields.Selection([('course','Course'),('job','Job')])
    color = fields.Integer(string='Colour')
    course_tag_id = fields.Many2one('course.frame')

class CourseFee(models.Model):
    _name = 'course.fee'
    _description = 'Course Fee'

    name = fields.Char('Name')
    code = fields.Char('Code')

# class CourseMode(models.Model):
#     _name = 'course.mode'
#     _description = 'Course Mode'
#
#     name = fields.Char('Mode Name')
#     code = fields.Char('Code')

class CourseModeType(models.Model):
    _name = 'course.mode.type'
    _description = 'Course Mode Type'

    name = fields.Char('Mode Name')
    code = fields.Char('Code')

class StudyMaterialType(models.Model):
    _name = 'study.material.type'
    _description = 'Study Material Type'

    name = fields.Char('Name')
    code = fields.Char('Code')

class SubjectPositions(models.Model):
    _name = 'subject.positions'
    _description = 'Subject Positions'

    _sql_constraints = [
        ('sequence_uniq', 'unique (sequence)', 'The Sequence must be unique !'),
    ]

    name = fields.Char('Name')
    code = fields.Char('Code')
    sequence = fields.Integer('Sequence')

class BudgetBudget(models.Model):
    _name = 'budget.budget'
    _description = 'Budget Master'


    name = fields.Char('Name')
    code = fields.Char('Code')

class RequestType(models.Model):
    _name = 'request.type'
    _description = 'Request Type'


    name = fields.Char('Name')
    code = fields.Char('Code')

class SubjectTopic(models.Model):
    _name = 'subject.topic'
    _description = 'Topic'


    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    subject_id = fields.Many2one('op.subject', required=True)

class SubjectUnit(models.Model):
    _name = 'subject.unit'
    _description = 'Unit'


    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    subject_id = fields.Many2one('op.subject', required=True)


class SubjectDisplaySystem(models.Model):
    _name = "subject.display.details"

    name = fields.Char('Name',readonly=True)
    type = fields.Selection([('subject','Subject'),('specialisation','Specialisation')],'Display Type',default='subject')
    subject_id = fields.Many2one('op.subject')
    specialisation_id = fields.Many2one('op.specialization', 'Specialisation',)

    @api.onchange('type','subject_id','specialisation_id')
    def onchange_type(self):
        for data in self:
            if data.type == 'subject' and data.subject_id:
                data.name = data.subject_id.name
            if data.type == 'specialisation' and data.specialisation_id:
                data.name = data.specialisation_id.name


class SubjectGrade(models.Model):
    _name = 'subject.grade'
    _description = 'Grade Master'


    name = fields.Char('Grade Name', required=True)
    code = fields.Char('Code')
    grade_lines = fields.One2many('subject.grade.lines','grade_id', required=True)


class SubjectGradeLines(models.Model):
    _name = "subject.grade.lines"

    grade_id = fields.Many2one('subject.grade')
    # name = fields.Char('Percentage of Marks')
    from_mark = fields.Float('Percentage of Marks From', required=True)
    to_mark = fields.Float('To', required=True)
    grade = fields.Selection(
        [('s', 'S'), ('a+', 'A+'), ('a', 'A'), ('b+', 'B+'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('f', 'F')],
        string='Grade', required=True)
    performance = fields.Char('Performance', required=True)
    grade_point = fields.Integer('Grade Point', required=True)

    @api.onchange('type','subject_id','specialisation_id')
    def onchange_type(self):
        for data in self:
            if data.type == 'subject' and data.subject_id:
                data.name = data.subject_id.name
            if data.type == 'specialisation' and data.specialisation_id:
                data.name = data.specialisation_id.name