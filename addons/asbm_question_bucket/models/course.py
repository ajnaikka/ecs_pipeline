# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpCourse(models.Model):
    _inherit = 'op.course'
    _description = 'Course Customization'

    corporate_id = fields.Many2one('res.corporate', 'Corporate User')