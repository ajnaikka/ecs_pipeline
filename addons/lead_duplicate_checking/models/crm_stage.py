# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    avoid_duplicate_check = fields.Boolean(string="Avoid Duplicate Checking", default=False)
    duplicate_stage = fields.Boolean(default=False, string="Duplicate Stage")
