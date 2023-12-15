
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from logging import info

from .test_activity_common import TestActivityCommon


class TestActivity(TestActivityCommon):

    def setUp(self):
        super(TestActivity, self).setUp()

    def test_case_activity_1(self):
        activity = self.op_activity.search([])
        info('Details of Activity')
        for record in activity:
            info('      Progression No : %s' % record.progression_id.name)
            info('      Student : %s' % record.student_id.name)
            info('      Faculty : %s' % record.faculty_id.name)
            info('      Activity Type : %s' % record.type_id.name)
            record.onchange_student_activity_progrssion()


class TestProgressionActivity(TestActivityCommon):

    def setUp(self):
        super(TestProgressionActivity, self).setUp()

    def test_case_progression_activity_1(self):
        progression_activity = self.op_progression_activity.search([])
        if not progression_activity:
            raise AssertionError(
                'Error in data, please check for reference ')
        info('Details of Achievement')
        for record in progression_activity:
            info('      Achievements : %s' %
                 record.activity_lines.type_id.name)
            info('      Total Activity Counts : %s' % record.total_activity)
            record._compute_total_activity()

    def test_case_1_progression_wizard(self):
        progression = self.op_progression_wizard.create({
            'student_id': self.env.ref('openeducat_core.op_student_1').id,
        })
        progression._get_default_student()
