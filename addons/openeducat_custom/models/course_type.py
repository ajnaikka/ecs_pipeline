
from odoo import models,fields,api,_
from odoo.exceptions import UserError

class CourseType(models.Model):
    _name='op.course.type'

    name = fields.Char(string="Course Type Name", required=True)
    code = fields.Selection(
        [('asbm', 'ASBM'), ('aste', 'ASTE')],
        'Code', default="asbm", required=True)



class Course(models.Model):
    _inherit='op.course'

    course_type = fields.Many2one('op.course.type',string="Course Type", required=False)
