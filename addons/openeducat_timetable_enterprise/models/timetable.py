# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
from odoo import models, fields, api


class OpSession(models.Model):
    _inherit = 'op.session'
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    section_ids = fields.Many2many('op.section',
                                   string='Section',
                                   domain="[('subject_id', '=', subject_id)]")
    batch_id = fields.Many2one('op.batch', required=False,
                               domain="[('course_id' , '=' , course_id)]")
    course_id = fields.Many2one('op.course', required=False)
    student_count = fields.Integer(compute='_compute_count_student')

    @api.model
    def create(self, values):
        res = super(OpSession, self).create(values)
        return res

    @api.onchange('section_ids')
    def onchange_section(self):
        if self.section_ids:
            self.batch_id = False
            self.course_id = False

    @api.onchange('subject_id')
    def onchange_subject_id(self):
        self.section_ids = False
        if self.subject_id:
            section_id = self.env['op.section']. \
                search([('subject_id', '=', self.subject_id.id)])
            return {'domain': {'section_ids': [('id', 'in', section_id.ids)]}}

    def get_student(self):
        action = self.env.ref(
            'openeducat_core.'
            'act_open_op_student_course_view').read()[0]
        for record in self:
            if record.section_ids:
                courses, batches, students = [], [], []
                for course in record.section_ids.course_ids:
                    courses.append(course.id)
                for batch in record.section_ids.batch_ids:
                    batches.append(batch.id)
                for student in record.section_ids.student_course_ids:
                    students.append(student.student_id.id)
                action['domain'] = [('course_id', 'in', courses),
                                    ('batch_id', 'in', batches),
                                    ('student_id', 'in', students),
                                    ('subject_ids', 'in',
                                     record.section_ids.subject_id.id)]
            else:
                action['domain'] = [('course_id', '=', record.course_id.id),
                                    ('batch_id', '=', record.batch_id.id)]
        return action

    def _compute_count_student(self):
        for record in self:
            if record.section_ids:
                courses, batches, students = [], [], []
                for course in record.section_ids.course_ids:
                    courses.append(course.id)
                for batch in record.section_ids.batch_ids:
                    batches.append(batch.id)
                for student in record.section_ids.student_course_ids:
                    students.append(student.student_id.id)
                record.student_count = self.env['op.student.course'].search_count(
                    [('course_id', 'in', courses), ('batch_id', 'in', batches),
                     ('student_id', 'in', students),
                     ('subject_ids', 'in', record.section_ids.subject_id.id)])
            else:
                record.student_count = self.env['op.student.course']. \
                    search_count(
                    [('course_id', '=', record.course_id.id),
                     ('batch_id', '=', record.batch_id.id)])
