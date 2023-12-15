# -*- coding: utf-8 -*-
from datetime import date, datetime, time
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CourseFrameWizard(models.TransientModel):
    _name = 'course.frame.wizard'
    _description = 'Course Frame Wizard'

    name = fields.Char('Name')
    course_frame_id = fields.Many2one('course.frame','Course Frame')
    user_id = fields.Many2one('res.users','User')
    is_create_course = fields.Boolean('Create Course')
    is_create_lms = fields.Boolean('Create LMS')
    is_course_created = fields.Boolean('Course Created', related='course_frame_id.is_course_created')
    is_lms_created = fields.Boolean('LMS Created', related='course_frame_id.is_lms_created')

    def action_create_course(self):
        for data in self:
            if data.is_create_lms and not data.course_frame_id.is_lms_created:
                lms = self.env['slide.channel'].create({
                    'name': self.course_frame_id.name,
                    'course_frame_id': self.course_frame_id.id,
                })
                subject_ids = []
                for subject in self.course_frame_id.subject_line.filtered(lambda l: l.type == 'subject'):
                    subject_ids.append((0, 0, {
                        'slide_category': 'subject',
                        'slide_type': 'flip_book',
                        'subject_id': subject.subject_id.id,
                        'name': subject.subject_id.name
                    }))
                lms.write({
                    'slide_ids': subject_ids
                })
                self.course_frame_id.is_lms_created = True
            if data.is_create_course and not data.course_frame_id.is_course_created:
                course = self.env['op.course'].create({
                    'name': self.course_frame_id.name,
                    'course_frame_id': self.course_frame_id.id,
                    'code': self.course_frame_id.course_code,
                    'fees_term_id': self.course_frame_id.course_fee_id.id,
                    'evaluation_type': 'normal',
                })
                subject_ids = []
                for subject in self.course_frame_id.subject_line.filtered(lambda l: l.type=='subject'):
                    subject.subject_id.course_id = course.id
                    subject.subject_id.total_marks = subject.total_marks
                    subject.subject_id.passing_marks = subject.passing_marks
                    subject.subject_id.showing_as_id = subject.showing_as_id.id
                    subject_ids.append((4, subject.subject_id.id))
                course.write({
                    'subject_ids': subject_ids
                })
                self.course_frame_id.is_course_created = True
            return data.course_frame_id.action_move_to_study_material()


