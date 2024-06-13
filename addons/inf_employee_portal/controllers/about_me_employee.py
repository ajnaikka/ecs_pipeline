# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, Controller, request, route
import base64
from datetime import datetime, timedelta
from odoo import http, fields
from werkzeug.utils import secure_filename


class CustomerPortal(Controller):

    @http.route('/send_email_to_hr', type='http', auth='user', website=True)
    def send_email_to_hr(self, **post):
        hr_manager_email = request.env.user.employee_id.hr_manager_id.work_email
        hr_manager = request.env.user.employee_id.hr_manager_id
        employee_id = request.env.user.employee_id
        description = post.get('description')
        subject = f'{employee_id.name} Profile Update Notification'
        body = f'Description: {description}'


        mail_user = hr_manager.user_id.id
        user_revoke = request.env['res.users'].sudo().browse(mail_user)

        message_post = request.env.user.partner_id.message_post(
            body=description,
            subject=subject,
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
            author_id=request.env.user.partner_id.id
        )

        if message_post:
            notification_values = [{
                'res_partner_id': user.partner_id.id,
                'mail_message_id': message_post.id
            } for user in user_revoke]

            message_post.sudo().notification_ids = [(0, 0, vals) for vals in notification_values]

        mail = request.env['mail.mail'].sudo().create({
            'email_from': request.env.user.email_formatted,
            'email_to': hr_manager_email,
            'subject': subject,
            'body_html': body,
            'author_id': request.env.user.partner_id.id,
            'auto_delete': True,
        })

        mail.send()

        employee_id.sudo().write({'enable_emp_profile_edit':True})




        return request.render('inf_employee_portal.certificate_application_submited_view', {
            'hr_manager_email': hr_manager_email})

    @http.route('/my/employees/about_me', type='http', auth='user', website=True)
    def employee_about_me(self):
        employee_id = request.env.user.employee_id
        work_locations = request.env['hr.work.location'].sudo().search([])
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        bank_accounts = request.env['res.partner.bank'].sudo().search([])
        work_country_id = employee_id.address_id.country_id.id
        work_state_id = employee_id.address_id.state_id.id
        pan_card_attachments = employee_id.pan_card.ids if employee_id.pan_card else []

        employee = request.env.user.employee_id
        if not employee.have_agreed_policy:
            return request.redirect('/my')
        else:
            return request.render('inf_employee_portal.view_about_me_form', {
                'employee': employee_id,
                'countries': countries,
                'states': states,
                'bank_accounts': bank_accounts,
                'work_locations': work_locations,
                'work_location_id': employee_id.work_location_id.id,
                'work_country_id': work_country_id,
                'work_state_id': work_state_id,
                'pan_card_attachments': pan_card_attachments,

            })



    # @http.route('/employee/form', type='http', auth='user', website=True)
    # def employee_form_sub(self, **post):
    #     employee_id = request.env.user.employee_id
    #     work_email = post.get('work_email')
    #     work_phone = post.get('work_phone')
    #     street = post.get('street')
    #     street2 = post.get('street2')
    #     city = post.get('city')
    #     zip_code = post.get('zip')
    #     state_id = post.get('state')
    #     country_id = post.get('country')
    #     work_location_id = post.get('work_location')
    #
    #     father_attachment = request.httprequest.files.getlist('father_attachment')
    #     mother_attachment = request.httprequest.files.getlist('mother_attachment')
    #     spouse_attachment = request.httprequest.files.getlist('spouse_attachment')
    #     # work_permit = request.httprequest.files.getlist('work_permit_file')
    #     aadhar_attachment = request.httprequest.files.getlist('aadhar_attachment')
    #     tenth_cer_attachment = request.httprequest.files.getlist('10th_certificate')
    #     plus_two_cer_attachment = request.httprequest.files.getlist('plus_two_certificate')
    #     graduation_attachment = request.httprequest.files.getlist('graduation_certificate')
    #     exp_attachment = request.httprequest.files.getlist('experience_certificate')
    #
    #     pan_card_attachment = request.httprequest.files.getlist('pan_card_attachment')
    #
    #     country = request.env['res.country'].sudo().browse(int(country_id))
    #     state = request.env['res.country.state'].sudo().browse(int(state_id))
    #     work_loc = request.env['hr.work.location'].sudo().browse(int(work_location_id))
    #
    #     children_data = []
    #
    #     child_first_names = request.httprequest.form.getlist('child_first_name[]')
    #     child_middle_names = request.httprequest.form.getlist('child_middle_name[]')
    #     child_last_names = request.httprequest.form.getlist('child_last_name[]')
    #     child_genders = request.httprequest.form.getlist('child_gender[]')
    #     child_attachments = request.httprequest.files.getlist('child_attachment[]')
    #
    #
    #     for i in range(len(child_first_names)):
    #         child_data = {
    #             'employee_id': employee_id.id,
    #             'first_name': child_first_names[i],
    #             'mid_name': child_middle_names[i],
    #             'last_name': child_last_names[i],
    #             'child_gender': child_genders[i],
    #             'children_attachment_ids': child_attachments[i],
    #         }
    #         if child_attachments and child_attachments[i]:
    #             attachment_data = {
    #                 'name': child_attachments[i].filename,
    #                 'datas': base64.b64encode(child_attachments[i].read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             attachment_id = request.env['ir.attachment'].sudo().create(attachment_data)
    #             child_data['children_attachment_ids'] = [(4, attachment_id.id)]
    #
    #         children_data.append((0, 0, child_data))
    #
    #     employee_id.write({'children_ids': children_data})
    #
    #
    #
    #     private_address_data = {
    #         'private_street': post.get('street'),
    #         'private_street2': post.get('street2'),
    #         'private_city': post.get('city'),
    #         'private_zip': post.get('zip'),
    #         'private_state_id': int(post.get('state')) if post.get('state') else None,
    #         'private_country_id': int(post.get('country')) if post.get('country') else None,
    #     }
    #
    #     marital_status = post.get('marital_status')
    #
    #     employee_id.write(private_address_data)
    #     father_attachment_ids = []
    #     if father_attachment and father_attachment[0]:
    #         for attachment_father in father_attachment:
    #             attachment_data_father = {
    #                 'name': attachment_father.filename,
    #                 'datas': base64.b64encode(attachment_father.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             attachment_id = request.env['ir.attachment'].sudo().create(attachment_data_father)
    #             father_attachment_ids.append(attachment_id.id)
    #
    #     aadhar_attachment_ids = []
    #     if aadhar_attachment and aadhar_attachment[0]:
    #         for attachment_aadar in aadhar_attachment:
    #             attachment_aadar_father = {
    #                 'name': attachment_aadar.filename,
    #                 'datas': base64.b64encode(attachment_aadar.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             attachment_id_aadhar = request.env['ir.attachment'].sudo().create(attachment_aadar_father)
    #             aadhar_attachment_ids.append(attachment_id_aadhar.id)
    #
    #     pan_attachment_ids = []
    #     if pan_card_attachment and pan_card_attachment[0]:
    #         for attachment_pan in pan_card_attachment:
    #             attachment_pan_data = {
    #                 'name': attachment_pan.filename,
    #                 'datas': base64.b64encode(attachment_pan.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             attachment_id_pan = request.env['ir.attachment'].sudo().create(attachment_pan_data)
    #             pan_attachment_ids.append(attachment_id_pan.id)
    #
    #     mother_attachment_ids = []
    #     if mother_attachment and mother_attachment[0]:
    #         for attachment_mother in mother_attachment:
    #             attachment_data_mother = {
    #                 'name': attachment_mother.filename,
    #                 'datas': base64.b64encode(attachment_mother.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             attachment_id = request.env['ir.attachment'].sudo().create(attachment_data_mother)
    #             mother_attachment_ids.append(attachment_id.id)
    #
    #     spouse_attachment_ids = []
    #     if spouse_attachment and spouse_attachment[0]:
    #         for attachment_spouse in spouse_attachment:
    #             attachment_data_spouse = {
    #                 'name': attachment_spouse.filename,
    #                 'datas': base64.b64encode(attachment_spouse.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #                 'type': 'binary',
    #             }
    #             attachment_id_spouse = request.env['ir.attachment'].sudo().create(attachment_data_spouse)
    #             spouse_attachment_ids.append(attachment_id_spouse.id)
    #
    #     tenth_cer_attachment_ids = []
    #     if tenth_cer_attachment and tenth_cer_attachment[0]:
    #
    #         for tenth_attachment in tenth_cer_attachment:
    #             tenth_attachment_data = {
    #                 'name': tenth_attachment.filename,
    #                 'datas': base64.b64encode(tenth_attachment.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             tenth_attachment_record = request.env['ir.attachment'].sudo().create(tenth_attachment_data)
    #             tenth_cer_attachment_ids.append(tenth_attachment_record.id)
    #
    #     plus_two_cer_attachment_ids = []
    #     if plus_two_cer_attachment and plus_two_cer_attachment[0]:
    #         for plus_two_attachment in plus_two_cer_attachment:
    #             plus_two_attachment_data = {
    #                 'name': plus_two_attachment.filename,
    #                 'datas': base64.b64encode(plus_two_attachment.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             plus_two_attachment_record = request.env['ir.attachment'].sudo().create(plus_two_attachment_data)
    #             plus_two_cer_attachment_ids.append(plus_two_attachment_record.id)
    #
    #     graduation_attachment_ids = []
    #     if graduation_attachment and graduation_attachment[0]:
    #
    #         for graduation_attachment in graduation_attachment:
    #             graduation_attachment_data = {
    #                 'name': graduation_attachment.filename,
    #                 'datas': base64.b64encode(graduation_attachment.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             graduation_attachment_record = request.env['ir.attachment'].sudo().create(graduation_attachment_data)
    #             graduation_attachment_ids.append(graduation_attachment_record.id)
    #
    #     exp_attachment_ids = []
    #     if exp_attachment and exp_attachment[0]:
    #
    #         for exp_attachment in exp_attachment:
    #             exp_attachment_data = {
    #                 'name': exp_attachment.filename,
    #                 'datas': base64.b64encode(exp_attachment.read()),
    #                 'res_model': 'hr.employee',
    #                 'res_id': employee_id.id,
    #             }
    #             exp_attachment_record = request.env['ir.attachment'].sudo().create(exp_attachment_data)
    #             exp_attachment_ids.append(exp_attachment_record.id)
    #
    #     family_data = {
    #         'mother_first_name': post.get('mother_first_name'),
    #         'mother_middle_name': post.get('mother_middle_name'),
    #         'mother_last_name': post.get('mother_last_name'),
    #         'mother_gender': post.get('mother_gender'),
    #         'mother_attachment_ids': [(6, 0, mother_attachment_ids)],
    #         'aadhar_card': [(6, 0, aadhar_attachment_ids)],
    #         'pan_card': [(6, 0, pan_attachment_ids)],
    #         'tenth_cer': [(6, 0, tenth_cer_attachment_ids)],
    #         'plus_two_cer': [(6, 0, plus_two_cer_attachment_ids)],
    #         'graduation': [(6, 0, graduation_attachment_ids)],
    #         'exp': [(6, 0, exp_attachment_ids)],
    #         'father_first_name': post.get('father_first_name'),
    #         'father_middle_name': post.get('father_middle_name'),
    #         'father_last_name': post.get('father_last_name'),
    #         'father_gender': post.get('father_gender'),
    #         'father_attachment_ids': [(6, 0, father_attachment_ids)],
    #         'spouse_first_name': post.get('spouse_first_name'),
    #         'spouse_middle_name': post.get('spouse_middle_name'),
    #         'spouse_last_name': post.get('spouse_last_name'),
    #         'spouse_gender': post.get('spouse_gender'),
    #         'spouse_attachment_ids': [(6, 0, spouse_attachment_ids)],
    #     }
    #
    #
    #     informations = {
    #         'marital': marital_status,
    #         'children': int(post.get('dependent_children')) if post.get('dependent_children') else 0,
    #         'l10n_in_residing_child_hostel': int(post.get('children_hostel')) if post.get('children_hostel') else 0,
    #         'emergency_contact': post.get('emergency_contact_name'),
    #         'l10n_in_relationship': post.get('emergency_relationship'),
    #         'emergency_phone': post.get('emergency_contact_phone'),
    #         'certificate': post.get('certificate_level'),
    #         'study_field': post.get('field_of_study'),
    #         'study_school': post.get('school'),
    #         'visa_no': post.get('visa_no'),
    #         'permit_no': post.get('work_permit_no'),
    #         'visa_expire': post.get('visa_exp_date'),
    #         'work_permit_expiration_date': post.get('work_permit_exp_date'),
    #         'country_id': int(post.get('nationality')) if post.get('nationality') else None,
    #         'identification_id': post.get('uan_no'),
    #         'l10n_in_esic_number': post.get('esic_number'),
    #         'pf_number': post.get('pf_no'),
    #         'insurance_number': post.get('insurance_no'),
    #         'ssnid': post.get('eso_no'),
    #         'passport_id': post.get('passport_no'),
    #         'gender': post.get('gender'),
    #         'birthday': post.get('dob'),
    #         'place_of_birth': post.get('place_of_birth'),
    #         'country_of_birth': int(post.get('country_of_birth')) if post.get('country_of_birth') else None,
    #         'is_non_resident': post.get('non_resident') == 'on',
    #         'work_email': work_email,
    #         'work_phone': work_phone,
    #         'work_location_id': work_loc.id if work_loc else False,
    #
    #     }
    #
    #     employee_id.sudo().write(informations)
    #     employee_id.sudo().write(family_data)
    #
    #
    #
    #     address_id = employee_id.address_id
    #     address_id.sudo().write({
    #         'street': street,
    #         'street2': street2,
    #         'city': city,
    #         'zip': zip_code,
    #         'state_id': state.id if state else False,
    #         'country_id': country.id if country else False,
    #     })
    #
    #     return request.render('inf_employee_portal.certificate_application_submited_view',
    #                           {'work_location_id': work_location_id})


