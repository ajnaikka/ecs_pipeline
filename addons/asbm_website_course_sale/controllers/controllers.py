# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class AsbmWebsiteSale(WebsiteSale):

    @http.route()
    def shop_payment_confirmation(self, **post):
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            order.partner_id.is_student = True

            if len(order.partner_id.name.split()) >= 3:
                x = order.partner_id.name.split()
                first_name = x[0]
                last_name = x[len(x)-1]
                x.pop(0)
                x.pop(len(x)-1)
                second_name = ' '.join(x)
            elif len(order.partner_id.name.split()) == 2:
                x = order.partner_id.name.split()
                first_name = x[0]
                last_name = x[1]
                second_name = False
            else:
                first_name = order.partner_id.name
                last_name = '.'
                second_name = False
            student_user = request.env['res.users'].sudo().search([('partner_id', '=', order.partner_id.id)])
            vals = {
                'first_name': first_name,
                'middle_name': second_name,
                'last_name': last_name,
                'birth_date': order.partner_id.dob,
                'gender': 'f' if order.partner_id.gender == 'female' else 'm',
                'image_1920': order.partner_id.image_1920 or False,
                'user_id': student_user.id,
                'company_id': request.env.company.id,
                'partner_id': order.partner_id.id,
                'mobile': order.partner_id.phone,
                'email': order.partner_id.email,
            }
            student_id = request.env['op.student'].sudo().create(vals).id

        return super().shop_payment_confirmation(**post)


