# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectClosingStage(http.Controller):
#     @http.route('/project_closing_stage/project_closing_stage', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_closing_stage/project_closing_stage/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_closing_stage.listing', {
#             'root': '/project_closing_stage/project_closing_stage',
#             'objects': http.request.env['project_closing_stage.project_closing_stage'].search([]),
#         })

#     @http.route('/project_closing_stage/project_closing_stage/objects/<model("project_closing_stage.project_closing_stage"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_closing_stage.object', {
#             'object': obj
#         })
