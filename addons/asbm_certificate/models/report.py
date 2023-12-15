# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, time



class IrActionReport(models.Model):
    _inherit = 'ir.actions.report'
    _description = 'Report Customization'

    is_main_certificate = fields.Boolean('Main Certificate')
    is_marksheet = fields.Boolean('Mark Sheet')
    is_consolidate_marksheet = fields.Boolean('Consolidate MarkSheet')