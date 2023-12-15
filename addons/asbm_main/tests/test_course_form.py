# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase

class TestCourseFrame(TransactionCase):
    def test_create_course_frame(self):
        test_course_frame_id = self.env['course.frame'].create({'name':'Course#1'})
        self.assertEqual(test_course_frame_id.name,'Course#1')
        test_course_frame_id.action_submit()
        test_course_frame_id.action_it_verification()
        test_course_frame_id.action_admission_verification()
        test_course_frame_id.action_account_verification()
        print('Successfully verified')
        test_course_frame_id.action_md_verification()
        print('Successfully MD verified')
        test_course_frame_id.project_id.createCourse()
        print('Course has been created')
        print('Your test was successfull')
