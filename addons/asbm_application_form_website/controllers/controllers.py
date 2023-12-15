# -*- coding: utf-8 -*-
import binascii

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import Response, request
import json
import base64


class ApplicationForm(http.Controller):
    # @http.route('/application_form', auth="public", csrf_token=False,website=True)
    @http.route('/student_employee_form/<int:lead_id>', type='http', auth="public", csrf_token=False,
                website=True)
    def student_employee_form(self, **kw):
        _course_result = http.request.env['op.course'].sudo().search([])
        _specialization_result = http.request.env['op.specialization'].sudo().search([])
        _nationality_result = http.request.env['res.country'].sudo().search([])
        lead_id = request.env['crm.lead'].sudo().browse([kw.get('lead_id')])
        # answer_token = request.httprequest.cookies.get('application_form_%s' % lead_token)
        token_obj = request.env['access.token']
        # token = token_obj.sudo().search([('name', '=', lead_token)])

        return request.render('asbm_application_form_website.student_employee_form', {
            'specializations': _specialization_result,
            'courses': _course_result,
            'nationality': _nationality_result,
            'lead_id': lead_id})

    @http.route('/application_form_signature/<int:lead_id>/<string:lead_token>', type='http', auth="public", csrf_token=False,
                website=True)
    def application_form_signature(self, lead_token, **kw):
        _course_result = http.request.env['op.course'].sudo().search([])
        admission_register = http.request.env['op.admission.register'].sudo().search(
            [('state', 'in', ('application', 'admission'))])
        _specialization_result = http.request.env['op.specialization'].sudo().search([])
        _nationality_result = http.request.env['res.country'].sudo().search([])
        lead_id = request.env['crm.lead'].sudo().browse([kw.get('lead_id')])

        token_obj = request.env['access.token']
        token = token_obj.sudo().search([('name', '=', lead_token)])

        return request.render('asbm_application_form_website.application_form_step_two', {
            'specializations': _specialization_result,
            'courses': _course_result,
            'admission_register': admission_register,
            'nationality': _nationality_result,
            'lead_id': lead_id})

    @http.route('/application_form/<int:lead_id>/<string:lead_token>', type='http', auth="public", csrf_token=False, website=True)
    def application_form(self, lead_token, **kw):
        _course_result = http.request.env['op.course'].sudo().search([])
        admission_register = http.request.env['op.admission.register'].sudo().search([('state', 'in', ('application', 'admission'))])
        _specialization_result = http.request.env['op.specialization'].sudo().search([])
        _nationality_result = http.request.env['res.country'].sudo().search([])
        lead_id = request.env['crm.lead'].sudo().browse([kw.get('lead_id')])

        # answer_token = request.httprequest.cookies.get('application_form_%s' % lead_token)
        token_obj = request.env['access.token']
        token = token_obj.sudo().search([('name', '=', lead_token)])

        return request.render('asbm_application_form_website.application_form', {
            'specializations': _specialization_result,
            'courses': _course_result,
            'admission_register': admission_register,
            'nationality': _nationality_result,
            'lead_id': lead_id})
        if token:
            if not token_obj.validate_token(token):
                token.sudo().unlink()
                return request.render('asbm_application_form_website.token_expire_msg')
            else:
                return request.render('asbm_application_form_website.application_form', {
                    'specializations': _specialization_result,
                    'courses': _course_result,
                    'admission_register': admission_register,
                    'nationality': _nationality_result,
                    'lead_id': lead_id})
        # if lead_id.send_status==False:

    @http.route(['/application_form/<int:lead_id>/<string:lead_token>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, lead_id, access_token=None, name=None, signature=None):
        # get from query string if not on json param
        lead_obj = request.env['crm.lead'].sudo().browse([lead_id])

        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            lead_obj.write({
                # 'signed_by': name,
                # 'signed_on': fields.Datetime.now(),
                'signature2': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}
        query_string = '&message=sign_ok'
        return {
            'force_refresh': True,
            # 'redirect_url': lead_obj.get_portal_url(query_string=query_string),
        }
        # return request.redirect(lead_obj.get_portal_url())

    @http.route('/submit_form', type='http', auth="user", website=True, methods=['POST'], csrf_token=False)
    def submit_data(self, **kw):
        # Do rest of the code here
        # Here is the lead id, use ro update the records
        lead_id = int(kw.get('lead_id'))
        lead_obj = request.env['crm.lead'].sudo().browse([lead_id])

        partner_id = lead_obj.partner_id.id
        partner_obj = request.env['res.partner'].sudo().browse([partner_id])
        student_name = kw.get('student_name')

        batch_code = kw.get('batch_code')
        branch = kw.get('branch')
        name_counselor = kw.get('name_counselor')
        application_for_admission = kw.get('application_for_admission')
        admission_register = kw.get('admission_register')
        if application_for_admission == 'None':
            application_for_admission = None
        else:
            application_for_admission = int(application_for_admission)
        if admission_register == 'None':
            admission_register = None
        else:
            admission_register = int(admission_register)
        specialization1 = kw.get('specializations1')
        if specialization1 == 'None':
            specialization1 = None
        # specialization2 = kw.get('specializations2')
        # if specialization2 == 'None':
        #     specialization2 = None
        # specialization3 = kw.get('specializations3')
        # if specialization3 == 'None':
        #     specialization3 = None
        # specialization4 = kw.get('specializations4')
        # if specialization4 == 'None':
        #     specialization4 = None
        dob = kw.get('dob')
        nationality = kw.get('nationality')
        if nationality == 'None':
            nationality = None

        gender = kw.get('gender')

        marital_status = kw.get('marital_status')

        house_no = kw.get('house_no_1')
        house_name = kw.get('house_name_1')
        street = kw.get('street1_1')
        land_mark = kw.get('land_mark_1')
        street2 = kw.get('street2_1')
        city = kw.get('city_1')
        state = kw.get('state_1')
        zip = kw.get('zip_1')

        house_no_1 = kw.get('house_no_2')
        house_name_1 = kw.get('house_name_2')
        street_1 = kw.get('street1_2')
        land_mark_1 = kw.get('land_mark_2')
        street2_1 = kw.get('street2_2')
        city_1 = kw.get('city_2')
        state_1 = kw.get('state_2')
        zip_1 = kw.get('zip_2')

        residential_no = kw.get('residential_no')
        phone = kw.get('office_no')
        mobile = kw.get('mobile_no')
        facebook_id = kw.get('facebook_id')
        whatsapp_id = kw.get('whatsapp_id')
        email = kw.get('email')
        fath_or_hus_name = kw.get('fath_or_hus_name')

        exam_option = kw.get('exam_option')
        mode_of_payment = kw.get('mode_of_payment')
        bank_name = kw.get('bank_name')
        fees_paid = kw.get('fees_paid')

        pdc_first_cheque_no = kw.get('pdc_first_cheque_no')
        pdc_first_cheque_date = kw.get('pdc_first_cheque_date')
        pdc_first_cheque_amount = kw.get('pdc_first_cheque_amount')

        pdc_second_cheque_no = kw.get('pdc_second_cheque_no')
        pdc_second_cheque_date = kw.get('pdc_second_cheque_date')
        pdc_second_cheque_amount = kw.get('pdc_second_cheque_amount')

        pdc_third_cheque_no = kw.get('pdc_third_cheque_no')
        pdc_third_cheque_date = kw.get('pdc_third_cheque_date')
        pdc_third_cheque_amount = kw.get('pdc_third_cheque_amount')

        submission_date = kw.get('submission_date')
        submission_place = kw.get('submission_place')

        # ACADEMIC DETAILS
        academic_line_vals = []
        if kw.get('degree1') != '':
            academic_line_vals.append((0, 0, {
                'degree': kw.get('degree1'),
                'name_of_school': kw.get('name_of_school1'),
                'exam_month': kw.get('exam_month1'),
                'exam_year': kw.get('exam_year1'),
                'subject': kw.get('subject1'),
                'result': kw.get('result1'),
            }))

        if kw.get('degree2') != '':
            academic_line_vals.append((0, 0, {
                'degree': kw.get('degree2'),
                'name_of_school': kw.get('name_of_school2'),
                'exam_month': kw.get('exam_month2'),
                'exam_year': kw.get('exam_year2'),
                'subject': kw.get('subject2'),
                'result': kw.get('result2'),
            }))

        if kw.get('degree3') != '':
            academic_line_vals.append((0, 0, {
                'degree': kw.get('degree3'),
                'name_of_school': kw.get('name_of_school3'),
                'exam_month': kw.get('exam_month3'),
                'exam_year': kw.get('exam_year3'),
                'subject': kw.get('subject3'),
                'result': kw.get('result3'),
            }))

        # WORK EXPERIENCE DETAILS
        work_experience_line_vals = []
        if kw.get('company_name1') != '':
            work_experience_line_vals.append((0, 0, {
                'company_name': kw.get('company_name1'),
                'designation': kw.get('designation1'),
                'no_of_years': kw.get('no_of_years1'),
            }))

        if kw.get('company_name2') != '':
            work_experience_line_vals.append((0, 0, {
                'company_name': kw.get('company_name2'),
                'designation': kw.get('designation2'),
                'no_of_years': kw.get('no_of_years2'),
            }))

        if kw.get('company_name3') != '':
            work_experience_line_vals.append((0, 0, {
                'company_name': kw.get('company_name3'),
                'designation': kw.get('designation3'),
                'no_of_years': kw.get('no_of_years3'),
            }))
        partner_image = None
        if 'wizard-picture' in request.params:
            attached_files = request.httprequest.files.getlist('wizard-picture')
            if attached_files:
                attached_file = attached_files[0].read()
                partner_image = base64.b64encode(attached_file)

        partner_data = {
            'name': student_name,
            'image_1920': partner_image if partner_image else False,
        }

        lead_data = {
            'work_experience_details_line': work_experience_line_vals,
            'academic_details_line': academic_line_vals,
            'batch_code': batch_code,
            'branch': branch,
            'application_for_admission': application_for_admission,
            'admission_register': admission_register,
            'specialization1': specialization1,
            # 'specialization2': specialization2,
            # 'specialization3': specialization3,
            # 'specialization4': specialization4,
            'dob': dob,
            'gender': gender,
            'marital_status': marital_status,
            'nationality': nationality,

            'house_no': house_no,
            'house_name': house_name,
            'street': street,
            'landmark': land_mark,
            'street2': street2_1,
            'zip': zip,
            'city': city,

            'house_no_1': house_no_1,
            'house_name_1': house_name_1,
            'street_or_road': street_1,
            'landmark_1': land_mark_1,
            'place_1': street2,
            'zip_1': zip_1,
            'city_1': city_1,

            'residential_no': residential_no,
            'phone': phone,
            'mobile': mobile,
            'facebook_id': facebook_id,
            'whatsapp_id': whatsapp_id,
            'send_status': True,
            # 'user_id': cls.user_sales_leads.id,
            # 'team_id': cls.sales_team_1.id,
            'fath_or_hus_name': fath_or_hus_name,
            'exam_option': exam_option,
            'mode_of_payment': mode_of_payment,
            'bank_name': bank_name,
            'fees_paid': fees_paid,
            'pdc_first_cheque_no': pdc_first_cheque_no,
            'pdc_first_cheque_date': pdc_first_cheque_date,
            'pdc_first_cheque_amount': pdc_first_cheque_amount,
            'pdc_second_cheque_no': pdc_second_cheque_no,
            'pdc_second_cheque_date': pdc_second_cheque_date,
            'pdc_second_cheque_amount': pdc_second_cheque_amount,
            'pdc_third_cheque_no': pdc_third_cheque_no,
            'pdc_third_cheque_date': pdc_third_cheque_date,
            'pdc_third_cheque_amount': pdc_third_cheque_amount,
            'submission_date': submission_date,
            'place': submission_place,
            'application_status': 'submitted',
        }
        # if lead_obj.signature2:
        #     lead_data.update({
        #         'signed_by': student_name,
        #         'signed_on': fields.Datetime.now(),
        #         'signature': lead_obj.signature2,
        #     })
        lead_obj.write(lead_data)
        # lead_obj.write({
        #     'signature2': False
        # })

        partner_obj.write(partner_data)

        if 'attachment' in request.params:
            attached_files = request.httprequest.files.getlist('attachment')
            for attachment in attached_files:
                attached_file = attachment.read()
                request.env['lead.documents'].sudo().create({
                    'name': attachment.filename,
                    'res_model': 'crm.lead',
                    'lead_id': lead_id,
                    # 'type': 'binary',
                    # 'store_fname': attachment.filename,
                    # 'datas': attached_file.encode('base64'),
                    'datas': attached_file
                })
        return request.redirect('/application_form_signature/%s/%s' % (lead_id, lead_obj.access_token))

    @http.route('/submit_form/signature', type='http', auth="user", website=True, methods=['POST'], csrf_token=False)
    def submit_signature_data(self, **kw):
        lead_id = int(kw.get('lead_id'))
        lead_obj = request.env['crm.lead'].sudo().browse([lead_id])
        lead_data = {}
        if lead_obj.signature2:
            lead_data.update({
                'signed_by': lead_obj.partner_id.name,
                'signed_on': fields.Datetime.now(),
                'signature': lead_obj.signature2,
            })
        lead_obj.write(lead_data)
        lead_obj.write({
            'signature2': False
        })
        return request.redirect('/student_employee_form/%s' % (lead_id))

        # return request.redirect('/contactus-thank-you')

    @http.route('/submit_student_employee_form', type='http', auth="user", website=True, methods=['POST'], csrf_token=False)
    def submit_student_employment_data(self, **kw):
        # Do rest of the code here
        # Here is the lead id, use ro update the records
        lead_id = int(kw.get('lead_id'))
        lead_obj = request.env['crm.lead'].sudo().browse([lead_id])

        partner_id = lead_obj.partner_id.id
        partner_obj = request.env['res.partner'].sudo().browse([partner_id])
        student_name = kw.get('student_name')
        course_enrolled=kw.get('course_enrolled')

        mobile = kw.get('mobile')
        residential_no = kw.get('residential_no')
        contact_ll_no = kw.get('contact_ll_no')

        company_name = kw.get('company_name')
        company_add1 = kw.get('company_add1')
        company_add2 = kw.get('company_add2')
        company_add3 = kw.get('company_add3')
        company_add4 = kw.get('company_add4')
        company_add5 = kw.get('company_add5')

        company_phone_no = kw.get('company_phone_no')
        function = kw.get('function')
        working_dept = kw.get('working_dept')

        reference_no1 = kw.get('reference_no1')
        reference_no2 = kw.get('reference_no2')
        reference_no3 = kw.get('reference_no3')
        reference_no4 = kw.get('reference_no4')
        reference_no5 = kw.get('reference_no5')
        reference_no6 = kw.get('reference_no6')

        lead_data = {
            'mobile': mobile,
            'residential_no': residential_no,
            'contact_ll_no': contact_ll_no,
            'company_name': company_name,
            'company_add1': company_add1,
            'company_add2': company_add2,
            'company_add3': company_add3,
            'company_add4': company_add4,
            'company_add5': company_add5,
            'company_phone_no': company_phone_no,
            'function': function,
            'working_dept': working_dept,

            'reference_no1': reference_no1,
            'reference_no2': reference_no2,
            'reference_no3': reference_no3,
            'reference_no4': reference_no4,
            'reference_no5': reference_no5,
            'reference_no6': reference_no6,

        }
        lead_obj.write(lead_data)

        return request.redirect('/contactus-thank-you')
