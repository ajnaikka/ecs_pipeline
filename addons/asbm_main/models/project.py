# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'

    course_id = fields.Many2one('op.course',string="Course")
    # course_frame_id = fields.Many2one('course.frame',string='Course Frame')
    def createCourse(self):
        data = self.create_course_frame_details()
        print('datadata',data)
        # print('datadata',data.dd)
        self.course_id = self.env['op.course'].create({
        'name':self.name,
        'is_product':False,
        'subject_ids':data['subject_ids'],
        'specialization_ids':data['specialization_ids'],
        'project_course_ids':data['project_ids'],
        'case_study_course_ids':data['case_study_ids']
        }).id

    def create_course_frame_details(self):
        data = {'subject_ids':[],
                'specialization_ids':[],
                'project_ids':[],
                'case_study_ids':[]}
        for line in self.course_frame_id.subject_specialization_ids:
            if line.type == 'subject':
                if not line.subject_id:
                    vals = {
                        'name':line.name,
                        'code':line.code,
                        'type':line.specialization_type,
                        'subject_type':line.subject_type,
                        'grade_weightage':line.grade_weightage,
                        'marks_in':line.marks_in,
                        'showing_as':line.showing_as,
                        'showing_in':line.showing_in,
                        'position':line.position,
                        'show_in_main_sheet':line.show_in_main_sheet,
                        'show_in_mark_sheet':line.show_in_mark_sheet,
                        'show_in_consolidated':line.show_in_consolidated
                    }
                    subject_id = self.env['op.subject'].create(vals)
                    data['subject_ids'].append(subject_id.id)
                    line.write({'subject_id':subject_id.id})
                else:
                    data['subject_ids'].append(line.subject_id.id)

            elif line.type == 'specialization':
                if not line.specialization_id:
                    vals = {
                        'name':line.name,
                        'code':line.code,
                        'category':line.category,
                        'type':line.specialization_type,
                        'subject_type':line.subject_type,
                        'grade_weightage':line.grade_weightage,
                        'marks_in':line.marks_in
                    }
                    specialization_id = self.env['op.specialization'].create(vals)
                    data['specialization_ids'].append(specialization_id.id)
                    line.write({'specialization_id':specialization_id.id})
                else:
                    data['specialization_ids'].append(line.specialization_id.id)

            elif line.type == 'project':
                if not line.project_id:
                    vals = {
                        'name':line.name,
                        'code':line.code,
                        'marks_in':line.marks_in,
                        'showing_as':line.showing_as,
                        'showing_in':line.showing_in,
                        'position':line.position,
                        'show_in_main_sheet':line.show_in_main_sheet,
                        'show_in_mark_sheet':line.show_in_mark_sheet,
                        'show_in_consolidated':line.show_in_consolidated
                    }
                    project_id = self.env['op.project'].create(vals)
                    data['project_ids'].append(project_id.id)
                    line.write({'project_id':project_id.id})
                else:
                    data['project_ids'].append(line.project_id.id)

            elif line.type == 'case_study':
                if not line.case_study_id:
                    vals = {
                        'name':line.name,
                        'code':line.code,
                        'marks_in':line.marks_in,
                        'showing_as':line.showing_as,
                        'showing_in':line.showing_in,
                        'position':line.position,
                        'show_in_main_sheet':line.show_in_main_sheet,
                        'show_in_mark_sheet':line.show_in_mark_sheet,
                        'show_in_consolidated':line.show_in_consolidated
                    }
                    case_study_id = self.env['op.case.study'].create(vals)
                    data['case_study_ids'].append(case_study_id.id)
                    line.write({'case_study_id':case_study_id.id})
                else:
                    data['case_study_ids'].append(line.case_study_id.id)

        return data
