
from odoo import models, fields, api


class StudentInvoiceWizard(models.TransientModel):
    _name = "op.student.invoice.wizard"
    _description = "Generate Student Invoice"

    student_ids = fields.Many2many('op.student', string="Students")
    fees_selection_type = fields.Selection([
        ('batch_wise', 'Batch'), ('course_wise', 'Course')], string="Fees Selection")
    course_id = fields.Many2one('op.course', 'Course')
    batch_id = fields.Many2one('op.batch', 'Batch')

    @api.onchange('batch_id', 'course_id')
    def onchange_students(self):
        student_ids = []
        if self.fees_selection_type == 'batch_wise':
            batch_wise = self.env['op.student.fees.details'].search(
                [('batch_id', '=', self.batch_id.id)])
            for student in batch_wise:
                student_ids.append(student.student_id.id)
        self.student_ids = [(6, 0, student_ids)]
        if self.fees_selection_type == 'course_wise':
            course_wise = self.env['op.student.fees.details'].search(
                [('course_id', '=', self.course_id.id)])
            for student in course_wise:
                student_ids.append(student.student_id.id)
        self.student_ids = [(6, 0, student_ids)]

    def create_student_invoice_wizard(self):
        for rec in self:
            fees = self.env['op.student.fees.details'].search(
                [('student_id', 'in', rec.student_ids.ids)])
            for fee in fees:
                fee.get_invoice()
