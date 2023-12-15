# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Channel(models.Model):
    _inherit = 'slide.channel'

    nbr_subsection = fields.Integer("Number of subsections", compute='_compute_slides_statistics', store=True)
    # nbr_sub_selection = fields.Integer("Number of sub selections", compute='_compute_slides_statistics', store=True)
