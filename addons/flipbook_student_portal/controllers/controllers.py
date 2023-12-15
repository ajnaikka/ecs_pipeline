# -*- coding: utf-8 -*-
from odoo.http import request, Response
from datetime import datetime, date
from odoo import http, tools, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.website.controllers.main import QueryURL
from collections import OrderedDict
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


PPG = 10

class StudyMaterialPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):

        values = super(StudyMaterialPortal, self)._prepare_portal_layout_values()
        user = request.env.user
        student_id = request.env["op.student"].sudo().search(
            [('user_id', '=', user.id)])
        course_ids = [course.course_id.id for course in student_id.course_detail_ids]
        material_count = request.env['flip.book'].sudo().search_count(
            [('course_id', 'in', course_ids)])
        values['material_count'] = material_count
        return values

    @http.route(['/student/study_materials/', '/student/study_materials/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_study_material_list(self, date_begin=None, date_end=None,
                                 page=0, search='', search_in='exam_code', ppg=False,
                                 sortby=None, filterby=None, groupby='none', **post):
        """ Home page for flipbook. Is mainly a container page, does not allow search / filter. """
        values = self._prepare_portal_layout_values()
        user = request.env.user
        student_id = request.env["op.student"].sudo().search(
            [('user_id', '=', user.id)])
        course_ids = [course.course_id.id for course in student_id.course_detail_ids]
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG
        searchbar_sortings = {
            'name': {'label': _('Material Code'), 'order': 'name asc'},
            'subject': {'label': _('Subject'), 'order': 'subject_id'},
            'course': {'label': _('Course'), 'order': 'course_id'}
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []}
        }
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']
        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])
        searchbar_inputs = {
            'name': {'input': 'name',
                          'label': _('Search in Material Code')},
            'subject_id': {'input': 'subject_id',
                        'label': _('Search in Subject')},
            'course_id': {'input': 'course_id',
                      'label': _('Search in Course')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'subject_id': {'input': 'subject_id', 'label': _('Subject')},
            'course_id': {'input': 'course_id', 'label': _('Course')},
        }
        domain += self.get_search_domain_study_material(search, attrib_values)

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'name'):
                search_domain = expression.OR(
                    [search_domain, [('name', 'ilike', search)]])
            if search_in in ('all', 'subject_id'):
                search_domain = expression.OR(
                    [search_domain, [('subject_id.name', 'ilike', search)]])
            if search_in in ('all', 'course_id'):
                search_domain = expression.OR(
                    [search_domain, [('course_id.name', 'ilike', search)]])
            domain += search_domain
        keep = QueryURL('/student/study_materials', search=search,
                        amenity=attrib_list, order=post.get('order'))
        domain += [('course_id', 'in', course_ids)]
        total = request.env['flip.book'].sudo().search_count(domain)
        pager = portal_pager(
            url="/student/study_materials",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby, 'filterby': filterby,
                      'search': search, 'search_in': search_in, }, total=total, page=page, step=ppg)
        if groupby == 'None':
            order = "state %s" % order
        flip_books = request.env['flip.book'].sudo().search(
            domain, order=order, limit=ppg, offset=pager['offset'])
        if groupby == 'None':
            grouped_tasks = [
                request.env['flip.book'].sudo().concat(*g)
                for k, g in groupbyelem(flip_books, itemgetter('None'))]
        else:
            grouped_tasks = [flip_books]
        values.update({
            'date': date_begin,
            'material_ids': flip_books,
            'page_name': 'material_detail',
            'pager': pager,
            'ppg': ppg,
            'keep': keep,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'default_url': '/student/study_materials/',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'grouped_tasks': grouped_tasks,
            'searchbar_groupby': searchbar_groupby,
            'groupby': groupby,
        })

        return request.render("flipbook_student_portal.student_material_portal_list", values)

    def get_search_domain_study_material(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', ('name', 'ilike', srch),
                    ('subject_id.name', 'ilike', srch), ('course_id.name', 'ilike', srch)
                ]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]
        return domain
    def check_student_material_access(self, flip_book_id=None):

        flip_book_id = request.env['flip.book'].sudo().search(
            [('id', '=', flip_book_id)])
        user = request.env.user
        student_id = request.env["op.student"].sudo().search(
            [('user_id', '=', user.id)])
        course_ids = [course.course_id.id for course in student_id.course_detail_ids]

        if flip_book_id.course_id.id not in course_ids:
            return False
        else:
            return True

    @http.route(['/student/study_materials/data/<int:material_id>',
                 '/student/study_materials/data/<int:student_id>/<int:material_id>', ],
                type='http', auth="user", website=True)
    def portal_study_material_form(self, student_id=None, material_id=None, ):

        flip_book = request.env['flip.book'].sudo().search(
            [('id', '=', material_id)])
        access_role = self.check_student_material_access(flip_book.id)
        if access_role is False:
            return Response("[Bad Request]", status=404)

        return request.render(
            "flipbook_student_portal.portal_study_material_details",
            {'study_material_details_id': flip_book,
             'student': student_id,
             'page_name': 'material_info'})
