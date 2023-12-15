# -*- coding: utf-8 -*-
from datetime import date, datetime, time

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    api_key = fields.Char('Flip Book API Key', copy=False, tracking=True, required=True)