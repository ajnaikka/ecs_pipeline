
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
from odoo.tests import common


class TestFeesCommon(common.SavepointCase):
    def setUp(self):
        super(TestFeesCommon, self).setUp()
        self.op_fees_template = self.env['op.fees.template.line']
        self.op_fees_term_line = self.env['op.fees.terms.line']
        self.op_fees_term = self.env['op.fees.terms']
