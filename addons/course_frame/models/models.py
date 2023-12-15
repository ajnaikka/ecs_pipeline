# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpSpecialisation(models.Model):
    _inherit = 'op.specialization'
    _description = 'Op Specialization'

    is_show_in_main_sheet = fields.Boolean('Main Sheet')
    is_show_in_mark_sheet = fields.Boolean('Mark Sheet')
    is_show_in_consolidate_sheet = fields.Boolean('Consolidate Sheet')


class OpCourse(models.Model):
    _inherit = 'op.course'

    course_frame_id = fields.Many2one(comodel_name='course.frame', string='Course Frame', copy=False)


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    course_frame_id = fields.Many2one(comodel_name='course.frame', string='Course Frame', copy=False)
