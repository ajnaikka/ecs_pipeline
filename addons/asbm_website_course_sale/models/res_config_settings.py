# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    payment_notification_users = fields.Many2many(
        'res.users', string='Users', domain=lambda self: "[('groups_id', '=', {}),('company_id', '=', id)]".format(
                                  self.env.ref("base.group_user").id))


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    payment_notification_users = fields.Many2many(
        'res.users', string='Email To (Account Users)', related='company_id.payment_notification_users',
        domain=lambda self: "[('groups_id', '=', {}),('company_id', '=', company_id)]".format(
                                  self.env.ref("base.group_user").id), readonly=False)
