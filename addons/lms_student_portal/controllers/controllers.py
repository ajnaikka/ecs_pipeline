# -*- coding: utf-8 -*-
# from odoo.http import request
# from odoo.addons.portal.controllers.portal import CustomerPortal
#
#
# class LmsStudentPortal(CustomerPortal):
#
#     def _prepare_portal_layout_values(self):
#         user = request.env.user
#         partner_id = user.partner_id.id
#         values = super(LmsStudentPortal, self)._prepare_portal_layout_values()
#         course_count = request.env['slide.channel.partner'].sudo().search_count(
#             [('partner_id', '=', partner_id)])
#         values['course_count'] = course_count
#         return values

