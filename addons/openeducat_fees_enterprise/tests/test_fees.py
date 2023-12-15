
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from logging import info

from .test_fees_common import TestFeesCommon


class TestFeesTemplate(TestFeesCommon):

    def setUp(self):
        super(TestFeesTemplate, self).setUp()

    def test_fees_template(self):
        template = self.op_fees_template.create({
            'line_id': self.env.ref('openeducat_fees.op_fees_term_line_1').id,
            'duration_type': 'before',
            'days': '5',
        })
        info('  Details Of Fees Template:.....')
        for record in template:
            info('      Fees Line : %s' % record.line_id)
            info('      Duration Type : %s' % record.duration_type)
            info('      Days : %s' % record.days)


class TestFeesTermLine(TestFeesCommon):

    def setUp(self):
        super(TestFeesTermLine, self).setUp()

    def test_fees_term_line(self):
        term = self.op_fees_term_line.search([])
        if not term:
            raise AssertionError(
                'Error in data, please check for Fees Term Line')
        info('  Details Of Fees Term Line:.....')
        for record in term:
            info('      Lines : %s' % record.line_ids)


class TestFeesTerm(TestFeesCommon):

    def setUp(self):
        super(TestFeesTerm, self).setUp()

    def test_fees_term(self):
        fees = self.op_fees_term.search([])
        if not fees:
            raise AssertionError(
                'Error in data, please check for Fees Term')
        info('  Details Of Fees Term:.....')
        for record in fees:
            record.run_send_fees_reminder()
