# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, time



class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Company Customization'

    is_main_certificate = fields.Boolean('Main Certificate')
    is_marksheet = fields.Boolean('Mark Sheet')
    is_consolidate_marksheet = fields.Boolean('Consolidate MarkSheet')