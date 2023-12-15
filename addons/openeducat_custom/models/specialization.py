
from odoo import models,fields,api,_
from odoo.exceptions import UserError


class specialization(models.Model):
    _name = 'op.specialization'

    name = fields.Char(string="Specialization Name", required=True)
    code = fields.Char(string="Code", required=True)
    grade_weightage = fields.Float('Grade Weightage')
    type = fields.Selection(
        [('theory', 'Theory'), ('practical', 'Practical'),
         ('both', 'Both'), ('other', 'Other')],
        'Type', default="theory", required=True)
    subject_type = fields.Selection(
        [('compulsory', 'Compulsory'), ('elective', 'Elective')],
        'Subject Type', default="compulsory", required=True)

    category = fields.Selection(
        [('specialization', 'Specialization'),('group', 'Group')],
        'Category', default="specialization", required=True)
    marks_in = fields.Char(string="Marks in")
    course_id = fields.Many2one('op.course', string='Course')

    @api.model
    def create(self, vals):
        res = super(specialization, self).create(vals)
        res.course_id.write({'specialization_ids': [(4, res.id)]})
        return res

    def write(self, vals):
        self.course_id.write({'specialization_ids': [(3, self.id)]})
        super(specialization, self).write(vals)
        self.course_id.write({'specialization_ids': [(4, self.id)]})
        return self


class opcourse(models.Model):
    _inherit = 'op.course'
    specialization_ids = fields.Many2many('op.specialization', string='Specialization(s)')
