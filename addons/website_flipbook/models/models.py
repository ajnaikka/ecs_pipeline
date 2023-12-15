# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.addons.http_routing.models.ir_http import slug, unslug


class FlipBook(models.Model):
    _inherit = 'flip.book'

    # website_id = fields.Many2one("website", string="Website")
    # website_url = fields.Char('Website URL', compute='_compute_website_url',
    #                           help='The full URL to access the document through the website.')
    visibility = fields.Selection([
        ('public', 'Open To All'), ('members', 'Members Only')],
        default='public', string='Visibility', required=True,
        help='Defines who can access your courses and their content.')

    @api.depends('name', 'website_id.domain')
    def _compute_website_url(self):
        super(FlipBook, self)._compute_website_url()
        for record in self:
            if record.id:  # avoid to perform a slug on a not yet saved record in case of an onchange.
                base_url = record.get_base_url()
                record.website_url = '%s/flipbook/%s' % (base_url, slug(record))

    @api.model
    def _search_get_detail(self, website, order, options):
        with_description = options['displayDescription']
        search_fields = ['name']
        fetch_fields = ['id', 'name', 'website_url']
        is_public = options.get('is_public')
        domain = [website.website_domain()]
        mapping = {
            'name': {'name': 'name', 'type': 'text', 'match': True},
            'website_url': {'name': 'website_url', 'type': 'text', 'truncate': False},
        }
        if with_description:
            search_fields.append('remark')
            fetch_fields.append('remark')
            mapping['description'] = {'name': 'remark', 'type': 'text', 'html': True, 'match': True}

        if is_public:
            domain.append([('visibility', '=', 'public')])
        if not is_public and self.env.user._is_public():
            domain.append([('visibility', '=', 'public')])

        return {
            'model': 'flip.book',
            'base_domain': domain,
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'fa-graduation-cap',
        }


class Website(models.Model):
    _inherit = "website"

    def get_suggested_controllers(self):
        suggested_controllers = super(Website, self).get_suggested_controllers()
        suggested_controllers.append((_('Flipbook'), url_for('/flipbook'), 'website_flipbook'))
        return suggested_controllers

    def _search_get_details(self, search_type, order, options):
        result = super()._search_get_details(search_type, order, options)
        if search_type in ['flipbook', 'flipbook_only', 'all']:
            result.append(self.env['flip.book']._search_get_detail(self, order, options))
        return result
