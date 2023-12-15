# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpAssignemnt(models.Model):
    _inherit = 'op.assignment'
    _description = 'Assignemnt Customization'

class OpSession(models.Model):
    _inherit = 'op.session'
    _description = 'Session Customization'

class OpBath(models.Model):
    _inherit = 'op.batch'
    _description = 'Batch Customization'

class OpFaculty(models.Model):
    _inherit = 'op.faculty'
    _description = 'Faculty Customization'

class OpMediaMovement(models.Model):
    _inherit = 'op.media.movement'
    _description = 'Media management Customization'

class OpActivity(models.Model):
    _inherit = 'op.activity'
    _description = 'Activity Customization'

class OpStudentFeesDetails(models.Model):
    _inherit = 'op.student.fees.details'
    _description = 'Fee Details Customization'

