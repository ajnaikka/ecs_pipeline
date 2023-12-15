
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo import http, _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
import dateutil.parser
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.website.controllers.main import QueryURL
from odoo.osv import expression
from collections import OrderedDict
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


class AdmissionRegistration(http.Controller):

    @http.route(['/admissionregistration'], type='http',
                auth='public', website=True)
    def admission_registration(self, **post):
        register_ids = request.env['op.admission.register'].sudo().search(
            [('state', '=', 'application')])
        country_ids = request.env['res.country'].sudo().search([])
        student_id = request.env['op.student'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id)])
        post.update({
            'register_ids': register_ids,
            'countries': country_ids,
            'student_id': student_id,
            'partner_id': request.env.user.partner_id,
        })
        return request.render(
            "openeducat_online_admission.admission_registration", post)

    @http.route(['/get/application_data'],
                type='json', auth="none", website=True)
    def get_application_data(self, application, **kw):

        student_id = request.env['op.student'].sudo().search_read(
            domain=[('partner_id', '=', int(application))],
            fields=['first_name', 'middle_name', 'last_name',
                    'gender', 'email', 'mobile', 'phone', 'street', 'city',
                    'zip', 'country_id', 'birth_date', 'partner_id', 'user_id'])

        country_id = request.env['res.country'].sudo().search_read(domain=[],
                                                                   fields=['name'])

        if application != '0':
            return {'student_id': student_id,
                    'country_id': country_id}
        else:
            return {'country': country_id}

    @http.route(['/check/birthdate'],
                type='json', auth="none", website=True)
    def check_birthdate(self, birthdate, register):
        today_date = datetime.today().date()
        birth_date = dateutil.parser.parse(birthdate).strftime(
            DEFAULT_SERVER_DATE_FORMAT)
        birth_date = datetime.strptime(
            birth_date, DEFAULT_SERVER_DATE_FORMAT).date()
        register_id = request.env['op.admission.register'].sudo().search(
            [('id', '=', int(register))])
        day = (today_date - birth_date).days
        years = day // 365
        if years < register_id.minimum_age_criteria:
            return {'birthdate': True,
                    'age': register_id.minimum_age_criteria}
        else:
            return {'birthdate': False}


class WebsiteSale(WebsiteSale):

    @http.route()
    def address(self, **kw):
        res = super(WebsiteSale, self).address(**kw)
        if request.session.get('data'):
            name = request.session['data']['first_name'] + ' ' + request.session[
                'data']['middle_name'] + ' ' + request.session[
                'data']['last_name']
            country = request.env['res.country'].sudo().search(
                [('id', '=', int(request.session['data']['country_id']))])
            res.qcontext.update({
                'checkout': {
                    'name': name,
                    'email': request.session['data']['email'],
                    'phone': request.session['data']['phone'],
                    'street': request.session['data']['street'],
                    'zip': request.session['data']['zip'],
                    'city': request.session['data']['city'],
                },
                'country': country
            })
            request.session.pop('data')
        return res

    @http.route()
    def confirm_order(self, **post):
        val = post.copy()
        admission_id = False
        if val and val.get('register_id', False):
            register = request.env['op.admission.register'].sudo().search(
                [('id', '=', int(val['register_id']))])
            product_id = register.product_id
            lst_price = register.product_id.lst_price
            val.update({'register_id': register.id,
                        'course_id': register.course_id.id,
                        'application_date': datetime.today(),
                        'fees': product_id and lst_price or 0.0,
                        'name': post.get('first_name') + ' ' + post.get(
                            'middle_name') + ' ' + post.get('last_name'),
                        'fees_term_id': register.course_id.fees_term_id.id,
                        'student_id': post.get('student_id'),
                        'company_id': register.company_id.id,
                        'state': 'online'})

            if not val['student_id']:
                val['birth_date'] = dateutil.parser.parse(val['birth_date']). \
                    strftime(DEFAULT_SERVER_DATE_FORMAT)
            admission_id = request.env['op.admission'].sudo().create(val)
            prod_id = False
            if register.course_id.reg_fees:
                prod_id = register.course_id.product_id.id
            else:
                return request.render(
                    "openeducat_online_admission.application_confirmed",
                    {'admission_id': admission_id})
            add_qty = 1
            set_qty = 0
            if not register.course_id.product_id.website_published:
                register.course_id.product_id.website_published = True
            request.website.sale_get_order(force_create=1)._cart_update(
                product_id=int(prod_id), add_qty=float(add_qty),
                set_qty=float(set_qty))

            order = request.website.sale_get_order()

            if order and admission_id:
                admission_id.write({'order_id': order.id})

            redirection = self.checkout_redirection(order)
            if redirection:
                return redirection

            if order.partner_id.id == \
                    request.website.user_id.sudo().partner_id.id:
                request.session['data'] = post
                return request.redirect('/shop/address')

            for f in self._get_mandatory_billing_fields():
                if not order.partner_id[f]:
                    request.session['data'] = post
                    return request.redirect(
                        '/shop/address?partner_id=%d' % order.partner_id.id)

            values = self.checkout_values(**post)

            if post.get('express'):
                return request.redirect('/shop/confirm_order')

            values.update({'website_sale_order': order})

            # Avoid useless rendering if called in ajax
            if post.get('xhr'):
                return 'ok'
            return request.render("website_sale.checkout", values)

        order = request.website.sale_get_order()
        if not order:
            return request.redirect("/shop")
        if order and admission_id:
            admission_id.write({'order_id': order.id})
            if request.env.uid:
                user = request.env['res.users'].browse(request.env.uid)
                partner_id = user.partner_id.id
            else:
                partner_id = request.env['res.partner'].sudo().create(post).id
            order.write({'partner_invoice_id': partner_id,
                         'partner_id': partner_id})
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection
        order.order_line._compute_tax_id()
        request.session['sale_last_order_id'] = order.id
        request.website.sale_get_order(update_pricelist=True)
        extra_step = request.env.ref('website_sale.extra_info_option')
        if extra_step.sudo().active:
            return request.redirect("/shop/extra_info")
        return request.redirect("/shop/payment")


PPG = 10  # record per page


class StudentRegistration(CustomerPortal):

    def get_search_domain_admission_registration(self, search, attrib_values):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', ('application_number', 'ilike', srch),
                    ('admission_date', 'ilike', srch), ('course_id', 'ilike', srch),
                    ('state', 'ilike', srch), ('application_date', 'ilike', srch)
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

    def _prepare_portal_layout_values(self):
        values = super(StudentRegistration, self).\
            _prepare_portal_layout_values()
        user = request.env.user
        student = request.env['op.student'].sudo().search([
            ('partner_id', '=', user.partner_id.id)])
        if student:
            admission_count = request.env['op.admission'].sudo().search_count(
                ['|', ('create_uid', '=', user._uid),
                 ('student_id', '=', student.id)])
        else:
            admission_count = request.env['op.admission'].sudo().search_count(
                [('create_uid', '=', user._uid)])
        values['admission_count'] = admission_count
        return values

    def _parent_prepare_portal_layout_values(self, student_id=None):

        val = super(StudentRegistration, self).\
            _parent_prepare_portal_layout_values(student_id)
        student = request.env['op.student'].sudo().search(
            [('id', '=', student_id)])

        admission_count = request.env['op.admission'].sudo().search_count(
            ['|', ('create_uid', '=', student.user_id.id),
             ('student_id', '=', student_id)])
        val['admission_count'] = admission_count
        return val

    @http.route(['/student/registration/info/',
                 '/student/registration/info/<int:student_id>',
                 '/student/registration/info/page/<int:page>',
                 '/student/registration/info/<int:student_id>/page/<int:page>'
                 ], type='http',
                auth='public', website=True)
    def student_registration_list_data123(
            self, date_begin=None, student_id=None, date_end=None, page=1,
            search='', ppg=False, sortby=None, filterby=None,
            search_in='application_number', groupby='course_id', **post):
        if student_id:
            val = self._parent_prepare_portal_layout_values(student_id)
        else:
            values = self._prepare_portal_layout_values()
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        user = request.env.user
        is_student = request.env['op.student'].sudo().search([
            ('user_id', '=', user.id)])

        if student_id:
            student = request.env['op.student'].sudo().search([
                ('id', '=', student_id)])
            domain = ['|', ('create_uid', '=', student.user_id.id),
                      ('student_id', '=', student_id)]

        elif is_student:
            user = request.env.user.partner_id
            student = request.env['op.student'].sudo().search([
                ('partner_id', '=', user.id)])
            domain = ['|', ('create_uid', '=', user._uid),
                      ('student_id', '=', student.id)]

        else:
            user = request.env.user
            domain = [('create_uid', '=', user._uid)]

        searchbar_sortings = {
            'student_id': {'label': _('Student'), 'order': 'student_id'},
            'application_number': {'label': _('Application No'),
                                   'order': 'application_number'},
            'admission_date': {'label': _('Admission Date'),
                               'order': 'admission_date'},
            'application_date': {'label': _('Application Date'),
                                 'order': 'application_date'},
            'state': {'label': _('State'), 'order': 'state'}
        }

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'state': {'label': _('Enroll'), 'domain': [('state', '=', 'done')]},
            'state online': {'label': _('Online Admission'),
                             'domain': [('state', '=', 'online')]},
        }
        courses = request.env['op.admission'].sudo().search(domain)
        for course in courses:
            searchbar_filters.update({
                str(course.course_id.id):
                    {'label': course.course_id.name,
                     'domain': [('course_id', '=', course.course_id.id)]},
            })

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if not sortby:
            sortby = 'student_id'
        order = searchbar_sortings[sortby]['order']

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])

        searchbar_inputs = {
            'application_number': {'input': 'application_number',
                                   'label': _('Search  (in Application No)')},
            'admission_date': {'input': 'Admission Date',
                               'label': _('Search in Admission Date')},
            'application_date': {'input': 'Application Date',
                                 'label': _('Search in Application Date')},
            'course_id': {'input': 'Course', 'label': _('Search in Course')},
            'state': {'input': 'State', 'label': _('Search in State')},
            'all': {'input': 'All', 'label': _('Search in All')},
        }

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'course_id': {'input': 'course_id', 'label': _('Course')},
        }

        domain += self.get_search_domain_admission_registration(
            search, attrib_values)

        if student_id:
            keep = QueryURL('/student/registration/info/%s' % student_id,
                            search=search, amenity=attrib_list,
                            order=post.get('order'))

            total = request.env['op.admission'].sudo().search_count(domain)

            pager = portal_pager(
                url="/student/registration/info/%s" % student_id,
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
                step=ppg
            )

        else:
            keep = QueryURL('/student/registration/info/', search=search,
                            amenity=attrib_list, order=post.get('order'))

            total = request.env['op.admission'].sudo().search_count(domain)

            pager = portal_pager(
                url="/student/registration/info/",
                url_args={'date_begin': date_begin, 'date_end': date_end,
                          'sortby': sortby, 'filterby': filterby,
                          'search': search, 'search_in': search_in},
                total=total,
                page=page,
                step=ppg
            )
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        if search and search_in:
            search_domain = []
            if search_in in ('all', 'application_number'):
                search_domain = expression.OR(
                    [search_domain, [('application_number', 'ilike', search)]])
            if search_in in ('all', 'admission_date'):
                search_domain = expression.OR(
                    [search_domain, [('admission_date', 'ilike', search)]])
            if search_in in ('all', 'course_id'):
                search_domain = expression.OR(
                    [search_domain, [('course_id', 'ilike', search)]])
            if search_in in ('all', 'application_date'):
                search_domain = expression.OR(
                    [search_domain, [('application_date', 'ilike', search)]])
            if search_in in ('all', 'state'):
                search_domain = expression.OR(
                    [search_domain, [('state', 'ilike', search)]])
            domain += search_domain

        if groupby == 'course_id':
            order = "course_id, %s" % order

        register_ids = request.env['op.admission'].sudo().search(
            domain, order=order, limit=ppg, offset=pager['offset'])

        if groupby == 'course_id':
            grouped_tasks = [
                request.env['op.admission'].sudo().concat(*g)
                for k, g in groupbyelem(register_ids, itemgetter('course_id'))]
        else:
            grouped_tasks = [register_ids]

        if student_id:
            student_access = self.get_student(student_id=student_id)
            if student_access is False:
                return request.render('website.404')
            val.update({
                'date': date_begin,
                'registration_id': register_ids,
                'page_name': 'Student Admission register info',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'stud_id': student_id,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/student/registration/info/%s' % student_id,
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
            return request.render(
                "openeducat_online_admission.openeducat_student_registration_list_data",
                val)
        else:
            values.update({
                'date': date_begin,
                'registration_id': register_ids,
                'page_name': 'Student Admission register info',
                'pager': pager,
                'ppg': ppg,
                'keep': keep,
                'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
                'filterby': filterby,
                'default_url': '/student/registration/info/',
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
            return request.render(
                "openeducat_online_admission.openeducat_student_registration_list_data",
                values)
