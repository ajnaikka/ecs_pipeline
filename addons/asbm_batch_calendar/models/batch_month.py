# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BatchMonth(models.Model):
    _name = 'batch.exam.month'
    _inherit = "mail.thread"
    _description = 'Bach Exam Month'

    @api.depends('month','year')
    def _name_set(self):
        for rec in self:
            print()
            if rec.month and rec.month != '0':
                month =dict(self._fields['month'].selection).get(rec.month)
                rec.name = month +"'"+rec.year
            elif rec.month == '0':
                rec.name =dict(self._fields['month'].selection).get(rec.month)
            else:
                rec.name = False

    @api.model
    def year_selection(self):
        year = 2020  # replace 2000 with your a start year
        year_list = [('nill','Nill')]
        while year != 2050:  # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    name = fields.Char('Name',compute=_name_set)
    month = fields.Selection([('0','Not Available'),('1','Jan'),('2','Feb'),('3','Mar'),
                              ('4','Apr'),('5','May'),('6','Jun'),
                              ('7','Jul'),('8','Aug'),('9','Sep'),
                              ('10','Oct'),('11','Nov'),('12','Dec')])

    year = fields.Selection(
        year_selection,
        string="Year",
        default="2023")