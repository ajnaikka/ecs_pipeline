# -*- coding: utf-8 -*-

import logging

from odoo import http, tools, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.website_profile.controllers.main import WebsiteProfile
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteFlipbook(WebsiteProfile):

    _flipbook_order_by_criterion = {
        'date': 'create_date desc',
    }

    def sitemap_slide(env, rule, qs):
        Channel = env['flip.book']
        dom = sitemap_qs2dom(qs=qs, route='/flipbook/', field=Channel._rec_name)
        dom += env['website'].get_current_website().website_domain()
        for channel in Channel.search(dom):
            loc = '/flipbook/%s' % slug(channel)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}
    def _flipbook_render_context_base(self):
        return {
            # current user info
            'user': request.env.user,
            'is_public_user': request.website.is_public_user(),
        }

    @http.route('/flipbook', type='http', auth="public", website=True, sitemap=True)
    def flipbook_home(self, **post):
        """ Home page for flipbook. Is mainly a container page, does not allow search / filter. """
        if request.env.user._is_public():
            domain = [('visibility', '=', 'public')]
        else:
            domain = []
        flipbook_all = tools.lazy(lambda: request.env['flip.book'].sudo().search(domain))

        render_values = self._flipbook_render_context_base()
        render_values.update(self._prepare_user_values(**post))
        render_values.update({
            'flipbook_all': flipbook_all,
        })

        return request.render('website_flipbook.flipbook_home', render_values)

    @http.route(['/flipbook/all', '/flipbook/all/tag/<string:slug_tags>'], type='http', auth="public", website=True,
                sitemap=True)
    def flipbook_all(self, slug_tags=None, **post):
        if slug_tags and request.httprequest.method == 'GET':
            # Redirect `tag-1,tag-2` to `tag-1` to disallow multi tags
            # in GET request for proper bot indexation;
            # if the search term is available, do not remove any existing
            # tags because it is user who provided search term with GET
            # request and so clearly it's not SEO bot.
            tag_list = slug_tags.split(',')
            if len(tag_list) > 1 and not post.get('search'):
                url = QueryURL('/flipbook/all', ['tag'], tag=tag_list[0])()
                return request.redirect(url, code=302)
        render_values = self.flipbook_all_values(slug_tags=slug_tags, **post)
        return request.render('website_flipbook.flipbook_all', render_values)

    def flipbook_all_values(self, slug_tags=None, **post):

        options = {
            'displayDescription': True,
            'displayDetail': False,
            'displayExtraDetail': False,
            'displayExtraLink': False,
            'displayImage': False,
            'allowFuzzy': not post.get('noFuzzy'),
            'tag': slug_tags or post.get('tag'),
            'is_public': True if request.env.user._is_public() else False,
        }
        search = post.get('search')
        order = self._flipbook_order_by_criterion.get(post.get('sorting'))
        _, details, fuzzy_search_term = request.website._search_with_fuzzy("flipbook_only", search,
                                                                           limit=1000, order=order, options=options)
        flipbooks = details[0].get('results', request.env['flip.book'])

        render_values = self._flipbook_render_context_base()
        render_values.update(self._prepare_user_values(**post))
        render_values.update({
            'flipbooks': flipbooks,
            'search_term': fuzzy_search_term or search,
            'original_search': fuzzy_search_term and search,
            'top3_users': self._get_top3_users(),
            'flipbook_query_url': QueryURL('/flipbook/all', ['tag']),
        })

        return render_values

    def _prepare_user_values(self, **kwargs):
        values = super(WebsiteFlipbook, self)._prepare_user_values(**kwargs)
        flipbook = self._get_flipbook(**kwargs)
        if flipbook:
            values['flipbook'] = flipbook
        return values

    def _get_flipbook(self, **kwargs):
        flipbookes = []
        if kwargs.get('flipbook'):
            flipbookes = kwargs['flipbook']
        elif kwargs.get('flipbook_id'):
            flipbookes = tools.lazy(lambda: request.env['flip.book'].browse(int(kwargs['flipbook_id'])))
        return flipbookes

    def _get_top3_users(self):
        return request.env['res.users'].sudo().search_read([
            ('karma', '>', 0),
            ('website_published', '=', True)], ['id'], limit=3, order='karma desc')

    @http.route([
        '/flipbook/<model("flip.book"):flipbook>',
        '/flipbook/<model("flip.book"):flipbook>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=sitemap_slide)
    def flipbook(self, flipbook, page=1, sorting=None, search=None, **kw):
        """
        Will return all necessary data to display the requested flipbook.
        """
        render_values = self._flipbook_render_context_base()
        render_values.update({
            'flipbook': flipbook,
            'main_object': flipbook,
            'active_tab': kw.get('active_tab', 'home'),
            # search
            'search': search,
        })
        return request.render('website_flipbook.flipbook_main', render_values)
