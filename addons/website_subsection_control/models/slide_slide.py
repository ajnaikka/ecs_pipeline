# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models



class Slide(models.Model):
    _inherit = 'slide.slide'

    # name = fields.Char(compute='_compute_name', readonly=False, store=True)
    slide_category = fields.Selection(selection_add=[
        ('subsection', 'subsection'),
        # ('subselection', 'Sub Selection')
    ], ondelete={'subsection': 'set default'})
    slide_type = fields.Selection(selection_add=[
        ('subsection', 'subsection'),
        # ('subselection', 'Sub Selection')
    ], ondelete={'subsection': 'set null'})
    nbr_subsection = fields.Integer("Number of subsections", compute='_compute_slides_statistics', store=True)



    def _compute_mark_complete_actions(self):
        slides_subsection = self.filtered(lambda slide: slide.slide_category == 'subsection')
        slides_subsection.can_self_mark_uncompleted = False
        slides_subsection.can_self_mark_completed = False
        super(Slide, self - slides_subsection)._compute_mark_complete_actions()

    @api.depends('slide_category')
    def _compute_is_preview(self):
        for slide in self:
            if slide.slide_category == 'subsection' or not slide.is_preview:
                slide.is_preview = False

    @api.depends('slide_category', 'source_type')
    def _compute_slide_type(self):
        super(Slide, self)._compute_slide_type()
        for slide in self:
            if slide.slide_category == 'subsection':
                slide.slide_type = 'subsection'

    @api.model_create_multi
    def create(self, vals_list):
        slides = super().create(vals_list)
        # slides_with_survey = slides.filtered('survey_id')
        # slides_with_survey.slide_category = 'subsection'
        # slides.slide_category = 'subsection'
        slides._ensure_challenge_category()
        return slides



    def _ensure_challenge_category(self, old_surveys=None, unlink=False):
        """ If a slide is linked to a survey that gives a badge, the challenge category of this badge must be
        set to 'slides' in order to appear under the subsection badge list on ranks_badges page.
        If the survey is unlinked from the slide, the challenge category must be reset to 'subsection'"""
        if old_surveys:
            old_subsection_challenges = old_surveys.mapped('subsection_badge_id').challenge_ids
            old_subsection_challenges.write({'challenge_category': 'subsection'})
