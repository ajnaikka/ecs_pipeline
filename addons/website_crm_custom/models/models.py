# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Channel(models.Model):
    """ A channel is a container of slides. """
    _inherit = 'slide.channel'

    hide_enroll_course = fields.Boolean(default=True, help="Hides enroll button in website")
