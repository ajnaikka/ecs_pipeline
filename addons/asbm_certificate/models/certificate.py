# -*- coding: utf-8 -*-
import logging

from num2words import num2words

from odoo import models, fields, api
from datetime import date, datetime, time



class CourseCertificate(models.Model):
    _name = 'course.certificate'
    _description = 'Course Certificate'


    @api.depends('student_id')
    def _compute_student_code(self):
        for data in self:
            admission = self.env['op.admission'].search([('course_id','=',data.course_id.id),('student_id','=',data.student_id.id)],limit=1)
            data.student_code = admission.enrollment_number

    name = fields.Char(index=True, default_export_compatible=True)
    date = fields.Date('Date',default=date.today())
    student_code = fields.Char('Student Code',compute='_compute_student_code')
    certificate_type = fields.Selection([('main','Main Certificate'),('marksheet','Mark Sheet'),('consolidated','Consolidated Sheet')],'Certificate Type')
    student_id = fields.Many2one('op.student','Student')
    course_id = fields.Many2one('op.course','Course')
    company_id = fields.Many2one('res.company', 'Company',default=lambda self: self.env.company)
    line_ids = fields.One2many('subject.score.lines','certificate_id',string='Score lines')
    mark_sheet_ids = fields.Many2many('mark.sheet.lines','certificate_id',string='Mark Sheet lines')
    attachment_id = fields.Binary('Certificate Template')
    grade_id = fields.Many2one('subject.grade','Grade')
    month_year = fields.Many2one('batch.exam.month', 'Month & Year')
    template_id = fields.Many2one('certificate.template','Report Template')
    main_report_id  = fields.Many2one('ir.actions.report','Main Report Template',domain="[('model', '=', 'course.certificate')]")
    mark_sheet_report_id  = fields.Many2one('ir.actions.report','Mark Sheet Report Template',domain="[('model', '=', 'course.certificate')]")
    consolidate_report_id  = fields.Many2one('ir.actions.report','Consolidate Report Template',domain="[('model', '=', 'course.certificate')]")
    main_certificate = fields.Boolean('Main Certificate')
    mark_sheet = fields.Boolean('Mark Sheet')
    consolidate_sheet = fields.Boolean('Consolidate Sheet')
    is_marklist_genarated = fields.Boolean(default=False,copy=False)
    certificate_status = fields.Selection([('draft','Draft'),('generated','Certificate Generated'),('send','Certificate Sent'),('delivered','Certificate Delivered')])
    percentage = fields.Float('Total Percentage')
    grade = fields.Char(string='Grade Achieved',compute='compute_grade')
    @api.depends('grade_id')
    def compute_grade(self):
        for data in self:
            grade = ''
            if data.grade_id:
                for line in data.grade_id.grade_lines:
                    if data.percentage >= line.from_mark and data.percentage < line.to_mark:
                        data.grade = str(line.grade)
                        grade = dict(line._fields['grade'].selection).get(line.grade)
            data.grade = grade



    @api.depends('line_ids')
    def genarate_mark_list(self):
        for data in self:
            dic = []
            for line in data.line_ids:
                if line.showing_as_id.id not in dic:
                    dic.append(line.showing_as_id.id)
            if dic:
                sheet = []
                for i in dic:
                    line_ids = data.line_ids.filtered(lambda m: m.showing_as_id.id == i)
                    value = {'name':line_ids[0].showing_as_id.name,
                             'certificate_id': data.id,
                             'showing_as_id': i,
                             'line_ids': line_ids
                             }
                    s = self.env['mark.sheet.lines'].create(value)
                    sheet.append(s.id)
                data.is_marklist_genarated = True
                data.mark_sheet_ids = sheet
                data.certificate_status = 'generated'

    def send_mark_list(self):
        for data in self:
            data.certificate_status = 'send'

    def deliver_marklist(self):
        for data in self:
            data.certificate_status = 'delivered'


    def print_mark_sheet(self):
        if self.mark_sheet_ids:
            for rec in self.mark_sheet_ids:
                return self.env.ref('asbm_certificate.marklist_certificate_print_menu_in_marklist').report_action(rec)

    def integer_to_text(self, amount):
        self.ensure_one()

        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""
        integer_value = int(amount)

        # lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', 'en')])
        amount_words = _num2words(integer_value, lang='en')
        return amount_words

    def convert_number_to_hyphenated_words(self,number):
        digits_to_words = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
        }

        number_str = str(number)
        hyphenated_words = " ".join([digits_to_words[digit] for digit in number_str])
        return hyphenated_words

    # def int_to_en(self,num):
    #     d = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    #          6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}
    #     k = 1000
    #     m = k * 1000
    #     b = m * 1000
    #     t = b * 1000
    #
    #     assert (0 <= num)
    #
    #     if (num < 20):
    #         return d[num]
    #
    #     if (num < 100):
    #         if num % 10 == 0:
    #             return d[num]
    #         else:
    #             return d[num // 10 * 10] + '-' + d[num % 10]
    #
    #     # if (num < k):
    #     #     if num % 100 == 0:
    #     #         return d[num // 100] + ' hundred'
    #     #     else:
    #     #         return d[num // 100] + ' hundred and ' + self.int_to_en(num % 100)
    #     #
    #     # if (num < m):
    #     #     if num % k == 0:
    #     #         return self.int_to_en(num // k) + ' thousand'
    #     #     else:
    #     #         return self.int_to_en(num // k) + ' thousand, ' + self.int_to_en(num % k)
    #     #
    #     # if (num < b):
    #     #     if (num % m) == 0:
    #     #         return self.int_to_en(num // m) + ' million'
    #     #     else:
    #     #         return self.int_to_en(num // m) + ' million, ' + self.int_to_en(num % m)
    #     #
    #     # if (num < t):
    #     #     if (num % b) == 0:
    #     #         return self.int_to_en(num // b) + ' billion'
    #     #     else:
    #     #         return self.int_to_en(num // b) + ' billion, ' + self.int_to_en(num % b)
    #     #
    #     # if (num % t == 0):
    #     #     return self.int_to_en(num // t) + ' trillion'
    #     # else:
    #     #     return self.int_to_en(num // t) + ' trillion, ' + self.int_to_en(num % t)
    #     # raise AssertionError('num is too large: %s' % str(num))


    def open_mark_lists(self):
        return {
            'name': 'Mark Lists',
            'domain': [('certificate_id', 'in', [self.id])],
            'context': {'search_default_certificate_id': self.id},
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mark.sheet.lines',
            'type': 'ir.actions.act_window',
        }

    @api.onchange('template_id')
    def onchange_certificate_template(self):
        for data in self:
            data.main_certificate = data.template_id.main_certificate
            data.mark_sheet = data.template_id.mark_sheet
            data.consolidate_sheet = data.template_id.consolidate_sheet
            data.main_report_id = data.template_id.main_report_id.id
            data.mark_sheet_report_id = data.template_id.mark_sheet_report_id.id
            data.consolidate_report_id = data.template_id.consolidate_report_id.id

class SubjectScoreLines(models.Model):
    _name = 'subject.score.lines'
    _description = 'Subject Score Lines'

    certificate_id = fields.Many2one('course.certificate')
    sheet_id = fields.Many2one('mark.sheet.lines')
    sl_no = fields.Integer('Sl No')
    subject_code = fields.Char('Subject Code')
    subject_id = fields.Many2one('op.subject','Subject')
    max_marks = fields.Integer('Max Marks')
    showing_as_id = fields.Many2one('showing.as', 'Showing As',related='subject_id.showing_as_id')
    max_awarded = fields.Integer('Marks Awarded')
    month_year = fields.Many2one('batch.exam.month','Month & Year')


class SubjectScoreLines(models.Model):
    _name = 'mark.sheet.lines'
    _description = 'Mark Sheet Score Lines'

    name = fields.Char('Name')
    certificate_id = fields.Many2one('course.certificate')
    showing_as_id = fields.Many2one('showing.as', 'Showing As')

    line_ids = fields.One2many('subject.score.lines', 'sheet_id', string='Score lines')