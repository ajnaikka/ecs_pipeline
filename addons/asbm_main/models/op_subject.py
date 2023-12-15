# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class OPSubject(models.Model):
    _inherit = 'op.subject'

    marks_in = fields.Char(string="Marks in")
    showing_as = fields.Char(string="Showing as")
    showing_in = fields.Char(string="Showing in")
    position = fields.Char(string="Position")
    show_in_main_sheet = fields.Char(string="Show in main sheet")
    show_in_mark_sheet = fields.Char(string="Show in mark sheet")
    show_in_consolidated = fields.Char(string="Show in Consolidated")
    # course_frame_id = fields.Many2one('course.frame',string="Course frame")
    
