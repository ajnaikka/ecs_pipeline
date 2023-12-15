# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CourseCategory(models.Model):
    _name = 'course.category'
    _inherit = "mail.thread"
    _description = 'Course Category'

    # @api.onchange('course_ids')
    # def course_ids_onchange(self):
    #     for rec in self:
    #         courses = self.env['op.course'].search([('course_category_id','=',rec.id)]).mapped('id')
    #         print('courses',courses)
    #         domain = [('id','in',courses)]
    #         return domain

    name = fields.Char('Name')
    course_ids = fields.Many2many('op.course','course_category_id',string='Related Courses')
    user_id = fields.Many2one('res.users','User',default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.company)
    parent_id = fields.Many2one('course.category','Parent Category')