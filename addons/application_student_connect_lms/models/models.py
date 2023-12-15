# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpAdmission(models.Model):
    _inherit = "op.admission"

    lms_connected = fields.Boolean(default=False, string="LMS Connected", copy=False)


class SlideChannelInvite(models.TransientModel):
    _inherit = 'slide.channel.invite'

    admission_id = fields.Many2one(comodel_name='op.admission', string="Application ID")

    def action_invite(self):
        res = super().action_invite()
        if self.admission_id:
            self.admission_id.lms_connected = True
        return res
