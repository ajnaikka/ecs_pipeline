# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"
    _description = "User"

    courses_id = fields.Many2one('op.course')
    students_id = fields.Many2one('op.student')



