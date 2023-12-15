
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpAdmission(models.Model):
    _inherit = "op.admission"

    state = fields.Selection(selection_add=[
        ('draft', 'Draft'), ('online', 'Online Admission'),
        ('submit', 'Submitted'), ('confirm', 'Confirmed'),
        ('admission', 'Admission Confirm'), ('reject', 'Rejected'),
        ('pending', 'Pending'), ('cancel', 'Cancelled'), ('done', 'Done')],
        default='draft', tracking=True)
    order_id = fields.Many2one('sale.order', 'Registration Fees Ref')
    application = fields.Char()


class OpBatch(models.Model):
    _inherit = "op.batch"


class OpStudentCourse(models.Model):
    _inherit = "op.student.course"


class OpSubject(models.Model):
    _inherit = "op.subject"
