
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import common


class TestActivityCommon(common.SavepointCase):
    def setUp(self):
        super(TestActivityCommon, self).setUp()
        self.op_activity = self.env['op.activity']
        self.op_progression_activity = self.env['op.student.progression']
        self.op_progression_wizard = self.env['activity.progress.wizard']
