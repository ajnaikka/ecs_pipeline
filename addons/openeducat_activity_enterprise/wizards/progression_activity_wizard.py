
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import models, fields, api


class ProgressActivityWiz(models.TransientModel):
    """ Progression Activity """
    _name = "activity.progress.wizard"
    _description = "Activity Progress Wizard"

    @api.model
    def _get_default_student(self):
        ctx = self._context
        if ctx.get('active_model') == 'op.student.progression':
            obj = self.env['op.student.progression']\
                .browse(ctx.get('active_ids')[0])
            return obj.student_id

    student_id = fields.Many2one('op.student',
                                 string="Student Name",
                                 default=_get_default_student)
    activity_ids = fields.Many2many('op.activity',
                                    string='Activity')

    def Add_activity(self):
        core = self.env['op.student.progression'].\
            browse(self.env.context['active_ids'])
        for i in core:
            i.activity_lines = self.activity_ids
