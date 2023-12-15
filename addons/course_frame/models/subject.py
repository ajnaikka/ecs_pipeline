# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OPSubject(models.Model):
    _inherit = 'op.subject'

    total_marks = fields.Float('Total Marks', required=True)
    passing_marks = fields.Float('Passing Marks', required=True)
    showing_as_id = fields.Many2one('showing.as','Semester/Year')