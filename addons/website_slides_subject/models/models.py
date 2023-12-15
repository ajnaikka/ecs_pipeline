# -*- coding: utf-8 -*-

from odoo import models, fields, api
from markupsafe import Markup


class Channel(models.Model):
    _inherit = 'slide.channel'

    nbr_subject = fields.Integer("Number of Subjects", compute='_compute_slides_statistics', store=True)


class Slide(models.Model):
    _inherit = 'slide.slide'

    slide_category = fields.Selection(selection_add=[
        ('subject', 'Subject')
    ], ondelete={'subject': 'set default'})
    slide_type = fields.Selection(selection_add=[
        ('flip_book', 'Flip Book')
    ], ondelete={'subject': 'set null'})
    subject_id = fields.Many2one('op.subject', 'Subject')
    nbr_subject = fields.Integer("Number of Subjects", compute='_compute_slides_statistics', store=True)
    flip_book_id = fields.Many2one('flip.book', string="Flip Book", domain="[('subject_id', '=', subject_id)]")

    @api.depends('subject_id')
    def _compute_flip_book(self):
        for slide in self:
            if slide.subject_id:
                flip_book = self.env['flip.book'].search([('subject_id', '=', slide.subject_id.id)], limit=1)
                slide.flip_book_id = flip_book.id if flip_book else False
            else:
                slide.flip_book_id = False

    def _compute_mark_complete_actions(self):
        slides = self.filtered(lambda slide: slide.slide_category == 'subject')
        slides.can_self_mark_uncompleted = True
        slides.can_self_mark_completed = True
        super(Slide, self - slides)._compute_mark_complete_actions()

    # @api.depends('slide_category')
    # def _compute_is_preview(self):
    #     for record in self:
    #         if record.slide_category == 'subject' or not record.is_preview:
    #             record.is_preview = True
    #         else:
    #             super(Slide, record)._compute_is_preview()

    @api.depends('slide_category', 'source_type')
    def _compute_slide_type(self):
        super(Slide, self)._compute_slide_type()
        for slide in self:
            if slide.slide_category == 'subject':
                slide.slide_type = 'flip_book'

    @api.depends('subject_id')
    def _compute_name(self):
        super(Slide, self)._compute_slide_type()
        for slide in self:
            if not slide.name and slide.subject_id:
                slide.name = slide.subject_id.name

    @api.depends('subject_id', 'flip_book_id')
    def _compute_embed_code(self):
        super()._compute_embed_code()
        for slide in self:
            if slide.slide_category == 'subject':
                embed_code = False
                embed_code_external = False
                if slide.subject_id and slide.flip_book_id:
                    embed_code = Markup('<iframe src="{}" width="100%" height="480" seamless="seamless" scrolling="no" frameborder="0" allowfullscreen="true"></iframe>'.format(slide.flip_book_id.url))
                slide.embed_code = embed_code
                slide.embed_code_external = embed_code_external or embed_code
