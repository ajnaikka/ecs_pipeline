from odoo import models, fields, api


class OpStudentFeesDetails(models.Model):
    _inherit = "op.student.fees.details"

    op_admission_id = fields.Many2one('op.admission', string="Admission Application")












