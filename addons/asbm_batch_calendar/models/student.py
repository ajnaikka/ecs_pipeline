# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpStudent(models.Model):
    _inherit = "op.student"
    _description = "Student"

    corporate_id = fields.Many2one('res.corporate','Corporate User')