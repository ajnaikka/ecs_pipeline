# -*- coding: utf-8 -*-
from odoo.http import request, Response
from datetime import datetime, date
from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.website.controllers.main import QueryURL
from collections import OrderedDict
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


PPG = 10


class StudentExamPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):

        values = super(StudentExamPortal, self)._prepare_portal_layout_values()
        user = request.env.user
        student_id = request.env["op.student"].sudo().search(
            [('user_id', '=', user.id)])
        exam_count = request.env['op.exam'].sudo().search_count(
            [('admission_id.student_id', '=', student_id.id)])
        values['student_exam_count'] = exam_count
        return values

    def _parent_prepare_portal_layout_values(self, student_id=None):

        val = super(StudentExamPortal, self)._parent_prepare_portal_layout_values(student_id)

        exam_count = request.env['op.exam'].sudo().search_count(
            [('admission_id.student_id', '=', student_id.id)])
        val['student_exam_count'] = exam_count
        return val

    def get_search_domain_student_exam(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', ('exam_code', 'ilike', srch),
                    ('subject_id.name', 'ilike', srch), ('state', 'ilike', srch)
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

    @http.route(['/student/exam_details/',
                 '/student/exam_details/<int:student_id>',
                 '/student/exam_details/page/<int:page>',
                 '/student/exam_details/<int:student_id>/page/<int:page>'],
                type='http', auth="user", website=True)
    def student_portal_exam_list(self, student_id=None, date_begin=None, date_end=None,
                                 page=0, search='', search_in='exam_code', ppg=False,
                                 sortby=None, filterby=None, groupby='none', **post):
        if student_id:
            val = self._parent_prepare_portal_layout_values(student_id)
        else:
            values = self._prepare_portal_layout_values()

        user = request.env.user
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        searchbar_sortings = {
            'exam_code': {'label': _('Exam code'),
                           'order': 'exam_code asc'},
            'subject': {'label': _('Subject'), 'order': 'subject_id'},
            'exam_date': {'label': _('Exam Date'),
                               'order': 'exam_date desc'},
            'state': {'label': _('State'), 'order': 'state'}
        }

        now = datetime.now()
        today = date.today()

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'today': {'label': _('Today'),
                      'domain': [('exam_date', '=', today)]},
        }

        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        if not sortby:
            sortby = 'exam_date'
        order = searchbar_sortings[sortby]['order']

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])

        searchbar_inputs = {
            'exam_code': {'input': 'exam_code',
                            'label': _('Search in Exam code')},
            'subject': {'input': 'subject_id',
                           'label': _('Search in Subject')},
            'state': {'input': 'State',
                       'label': _('Search in State')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'state': {'input': 'state', 'label': _('State')},
        }

        domain += self.get_search_domain_student_exam(search, attrib_values)

        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'exam_code'):
                search_domain = expression.OR(
                    [search_domain, [('exam_code', 'ilike', search)]])
            if search_in in ('all', 'subject'):
                search_domain = expression.OR(
                    [search_domain, [('subject_id.name', 'ilike', search)]])
            if search_in in ('all', 'state'):
                search_domain = expression.OR(
                    [search_domain, [('state', 'ilike', search)]])
            domain += search_domain

        if student_id:
            keep = QueryURL('/student/exam_details/%s' % student_id,
                            search=search, amenity=attrib_list,
                            order=post.get('order'))
            domain += [('admission_id.student_id', '=', student_id)]
            total = request.env['op.exam'].sudo().search_count(domain)
            pager = portal_pager(
                url="/student/exam_details/%s" % student_id,
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in, }, total=total, page=page, step=ppg)
        else:
            keep = QueryURL('/student/exam_details/', search=search,
                            amenity=attrib_list, order=post.get('order'))
            student = request.env["op.student"].sudo().search(
                [('user_id', '=', user.id)])
            domain += [('admission_id.student_id', '=', student.id)]
            total = request.env['op.exam'].sudo().search_count(domain)

            pager = portal_pager(
                url="/student/exam_details/",
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in, }, total=total, page=page, step=ppg)

        if groupby == 'None':
            order = "state %s" % order

        if student_id:
            student_access = self.get_student(student_id=student_id)
            if student_access is False:
                return request.render('website.404')
            exam_id = request.env['op.exam'].sudo().search(
                domain, order=order, limit=ppg, offset=pager['offset'])
        else:
            exam_id = request.env['op.exam'].sudo().search(
                domain, order=order, limit=ppg, offset=pager['offset'])

        if groupby == 'None':
            grouped_tasks = [
                request.env['op.exam'].sudo().concat(*g)
                for k, g in groupbyelem(exam_id, itemgetter('None'))]
        else:
            grouped_tasks = [exam_id]

        if student_id:
            val.update({
                'date': date_begin,
                'exam_ids': exam_id,
                'page_name': 'Student_Exam_List',
                'pager': pager,
                'ppg': ppg,
                'stud_id': student_id,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/student/exam_details/%s' % student_id,
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
            return request.render("exam_student_portal.student_exam_portal_list", val)
        else:
            values.update({
                'date': date_begin,
                'exam_ids': exam_id,
                'page_name': 'Student_Exam_List',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/student/exam_details/',
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

            return request.render("exam_student_portal.student_exam_portal_list", values)

    def check_student_exam_access(self, exam_id=None):

        op_exam_id = request.env['op.exam'].sudo().search(
            [('id', '=', exam_id)])
        user = request.env.user
        user_list = []
        count = 0
        for rec in op_exam_id.admission_id.student_id:
            if rec.user_id:
                user_list.append(rec.user_id)

        if user.partner_id.is_parent:
            parent_id = request.env['op.parent'].sudo().search(
                [('name', '=', user.partner_id.id)])
            for student_id in parent_id.student_ids:
                if student_id.user_id in user_list:
                    count += 1
            if count > 0:
                return True
            else:
                return False
        else:
            if user not in user_list:
                return False
            else:
                return True

    @http.route(['/student/exam_details/data/<int:exam_id>',
                 '/student/exam_details/data/<int:student_id>/<int:exam_id>', ],
                type='http', auth="user", website=True)
    def portal_student_exam_details_form(self, student_id=None, exam_id=None, ):

        exam_instance = request.env['op.exam'].sudo().search(
            [('id', '=', exam_id)])
        access_role = self.check_student_exam_access(exam_instance.id)
        if access_role is False:
            return Response("[Bad Request]", status=404)

        return request.render(
            "exam_student_portal.student_exam_portal_details",
            {'exam_details_id': exam_instance,
             'student': student_id,
             'page_name': 'exam_info'})
#     @http.route('/exam_student_portal/exam_student_portal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exam_student_portal/exam_student_portal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exam_student_portal.listing', {
#             'root': '/exam_student_portal/exam_student_portal',
#             'objects': http.request.env['exam_student_portal.exam_student_portal'].search([]),
#         })

#     @http.route('/exam_student_portal/exam_student_portal/objects/<model("exam_student_portal.exam_student_portal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exam_student_portal.object', {
#             'object': obj
#         })
