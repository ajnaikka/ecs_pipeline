# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class OpExam(models.Model):
    _inherit = "op.exam"

    survey_id = fields.Many2one('survey.survey', 'Exam template(1)', copy=False)
    session_code = fields.Char(string='Session Code(1)', copy=False)
    session_link = fields.Char(string='Session Link(1)', copy=False)
    first_exam_status = fields.Selection([('pass', 'Passed'), ('fail', 'Failed'), ('not_done', 'Not Done')],
                                         default='not_done', string="First Exam Status", copy=False)
    survey_id_shared = fields.Boolean(default=False, string="Survey ID Shared")

    survey_id_2 = fields.Many2one('survey.survey', 'Exam template(2)', copy=False)
    session_code_2 = fields.Char(string='Session Code(2)', copy=False)
    session_link_2 = fields.Char(string='Session Link(2)', copy=False)
    second_exam_status = fields.Selection([('pass', 'Passed'), ('fail', 'Failed'), ('not_done', 'Not Done')],
                                          default='not_done', string="Second Exam Status", copy=False)
    survey_id_2_shared = fields.Boolean(default=False, string="Survey ID 2 Shared")

    survey_id_3 = fields.Many2one('survey.survey', 'Exam template(3)', copy=False)
    session_code_3 = fields.Char(string='Session Code(3)', copy=False)
    session_link_3 = fields.Char(string='Session Link(3)', copy=False)
    third_exam_status = fields.Selection([('pass', 'Passed'), ('fail', 'Failed'), ('not_done', 'Not Done')],
                                         default='not_done', string="Third Exam Status", copy=False)
    survey_id_3_shared = fields.Boolean(default=False, string="Survey ID 3 Shared")

    def action_schedule_exam(self):
        for record in self:
            record.state = 'schedule'

    def action_send_exam_link(self):
        """ Open a window to compose an email, pre-filled with the survey message """
        # Ensure that this exam has at least one question.
        if self.survey_id_3:
            survey_id = self.survey_id_3
            exam_invite_attempt = '3'
        elif self.survey_id_2:
            survey_id = self.survey_id_2
            exam_invite_attempt = '2'
        else:
            survey_id = self.survey_id
            exam_invite_attempt = '1'
        if not survey_id.question_ids:
            raise UserError(_('You cannot send an invitation for an exam that has no questions.'))

        # Ensure that this survey has at least one section with question(s), if question layout is 'One page per section'.
        if survey_id.questions_layout == 'page_per_section':
            if not survey_id.page_ids:
                raise UserError(
                    _('You cannot send an invitation for a "One page per section" survey if the survey has no sections.'))
            if not survey_id.page_ids.mapped('question_ids'):
                raise UserError(
                    _('You cannot send an invitation for a "One page per section" survey if the survey only contains empty sections.'))

        if not survey_id.active:
            raise exceptions.UserError(_("You cannot send invitations for closed surveys."))

        template = self.env.ref('exam_scheduling.mail_template_student_input_invite', raise_if_not_found=False)

        local_context = dict(
            self.env.context,
            default_survey_id=survey_id.id,
            default_exam_id=self.id,
            default_partner_ids=[(4, self.admission_id.partner_id.id)],
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_email_layout_xmlid='mail.mail_notification_light',
            default_exam_invite_attempt=exam_invite_attempt,
        )
        return {
            'type': 'ir.actions.act_window',
            'name': _("Exam Invite"),
            'view_mode': 'form',
            'res_model': 'student.exam.invite',
            'target': 'new',
            'context': local_context,
        }


class OpExamAttendees(models.Model):
    _inherit = "op.exam.attendees"

    survey_user_input_id = fields.Many2one('survey.user_input', string="Survey User Input", copy=False)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    exam_attendees_id = fields.Many2one('op.exam.attendees', string="Exam attendees", copy=False)

    def _mark_done(self):
        super()._mark_done()
        for user_input in self:
            if user_input.exam_attendees_id:
                user_input.exam_attendees_id.marks = user_input.scoring_total
                if user_input.exam_attendees_id.marks >= user_input.exam_attendees_id.exam_id.min_marks:
                    user_input.exam_attendees_id.exam_id.state = 'held'
                    if user_input.survey_id == user_input.exam_attendees_id.exam_id.survey_id:
                        user_input.exam_attendees_id.exam_id.first_exam_status = 'pass'
                    elif user_input.survey_id == user_input.exam_attendees_id.exam_id.survey_id_2:
                        user_input.exam_attendees_id.exam_id.second_exam_status = 'pass'
                    else:
                        user_input.exam_attendees_id.exam_id.third_exam_status = 'pass'
                else:
                    if user_input.survey_id == user_input.exam_attendees_id.exam_id.survey_id:
                        user_input.exam_attendees_id.exam_id.first_exam_status = 'fail'
                    elif user_input.survey_id == user_input.exam_attendees_id.exam_id.survey_id_2:
                        user_input.exam_attendees_id.exam_id.second_exam_status = 'fail'
                    else:
                        user_input.exam_attendees_id.exam_id.third_exam_status = 'fail'
