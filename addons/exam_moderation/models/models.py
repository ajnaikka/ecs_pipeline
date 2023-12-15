# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpExam(models.Model):
    _inherit = "op.exam"

    moderation_exam_status = fields.Selection([('pass', 'Passed'), ('fail', 'Failed'), ('not_done', 'Not Done')],
                                         default='not_done', string="Moderation Exam Status")
