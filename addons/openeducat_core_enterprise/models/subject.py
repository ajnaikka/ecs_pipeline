
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class OpSubject(models.Model):
    _inherit = "op.subject"

    course_id = fields.Many2many(comodel_name='op.course', relation='course_subject_rel', column1='subject_id',
                                 column2='course_id', string=' Course')
    # course_ids = fields.Many2many('op.course', string='Courses')
    credit_point = fields.Float('Credit')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, vals):
        res = super(OpSubject, self).create(vals)
        for course in res.course_id:
            course.write({'subject_ids': [(4, res.id)]})
        return res

    def write(self, vals):
        for course in self.course_id:
            course.write({'subject_ids': [(3, self.id)]})
        super(OpSubject, self).write(vals)
        for course in self.course_id:
            course.write({'subject_ids': [(4, self.id)]})
        return self

    def action_onboarding_subject_layout(self):
        self.env.user.company_id.onboarding_subject_layout_state = 'done'
