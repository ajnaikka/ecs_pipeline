# -*- coding: utf-8 -*-
from datetime import date, datetime, time
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MarkListWizard(models.TransientModel):
    _name = 'mark.list.wizard'
    _description = 'Mark List Wizard'

    name = fields.Char('Name')
    certificate_id = fields.Many2one('course.certificate','Course Certificate')
    user_id = fields.Many2one('res.users','User')



