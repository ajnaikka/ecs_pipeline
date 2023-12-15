from odoo import models, fields, api, _
import uuid
import werkzeug
from odoo.exceptions import UserError


class crmLead(models.Model):
    _inherit = "crm.lead"
    # _inherit = ["mail.thread"]

    partner_id = fields.Many2one(required=False)
    student_id = fields.Many2one('op.student', string="Student")
    partner_correspondence_address = fields.Many2one('res.partner', string="Partner Correspondence Address")
    partner_permanent_address = fields.Many2one('res.partner', string="Partner Permanent Address")
    branch = fields.Char(string="Branch")
    batch_code = fields.Char(string="Batch Code")
    admission_register = fields.Many2one('op.admission.register', string="Application for Admission", domain="[('state', 'in', ('application','admission')), ('company_id', '=', company_id)]")
    application_for_admission = fields.Many2one('op.course', string="Course", related='admission_register.course_id', store=True)
    course_fees = fields.Float(string='Course Fees', related='admission_register.product_id.lst_price', digits='Product Price', store=True)
    course_type = fields.Many2one('op.course.type', string="Course Type")
    user_id = fields.Many2one(string="Counsellor")

    specialization1 = fields.Many2one('op.specialization', string="Specialization1")
    specialization2 = fields.Many2one('op.specialization', string="Specialization2")
    specialization3 = fields.Many2one('op.specialization', string="Specialization3")
    specialization4 = fields.Many2one('op.specialization', string="Specialization3")

    dob = fields.Date(string='DOB')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender',  index=True, default='male')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
    ], string='Marital Status',  index=True, default='single')
    fath_or_hus_name = fields.Char(string="Father's / Husband's Name")
    residential_no = fields.Char(string="Residential No")
    facebook_id = fields.Char(string="Facebook Id")
    whatsapp_id = fields.Char(string="Whatsapp Id")
    nationality = fields.Many2one('res.country', 'Nationality')
    landmark = fields.Char(string="Landmark")


    house_no = fields.Char(string="House No")
    house_name = fields.Char(string="House Name")

    house_no_1 = fields.Char(string="House No")
    house_name_1 = fields.Char(string="House Name")
    street_or_road = fields.Char(string="Street or Road")
    landmark_1 = fields.Char(string="Landmark")
    place_1 = fields.Char(string="Place")
    city_1 = fields.Char(string="City")
    zip_1 = fields.Char(string='Zip',change_default=True)
    state_id_1 = fields.Many2one("res.country.state", 'State')
    is_student = fields.Boolean("Is a Student", default=False)
    send_status = fields.Boolean("send status")
    access_token = fields.Char('Access Token', default=lambda self: self._get_default_access_token(), copy=False)

    mail_website_val = fields.Char(string='Mail Website',compute="_get_lead_website_url", readonly=False)
    mail_student_emp_website_val = fields.Char(string='Website', compute="_get_student_employee_form_website_url", readonly=False)

    exam_option = fields.Selection([
        ('home', 'Home'),
        ('study_center', 'Study Center'),
        ('online', 'Online'),
    ], string='Exam Option', index=True, default='home')

    mode_of_payment = fields.Selection([
        ('by_cash', 'By Cash'),
        ('by_cheque', 'By Cheque/DD'),
        ('online_transfer', 'Online Transfer'),
    ], string='Mode of Payment', index=True, default='by_cash')

    bank_name = fields.Char(string="Bank Name")
    fees_paid = fields.Float(string="Fees Paid")

    pdc_first_cheque_no=fields.Char(string="Cheque No")
    pdc_first_cheque_date = fields.Date(string="Date")
    pdc_first_cheque_amount = fields.Float(string="Amount")

    pdc_second_cheque_no = fields.Char(string="Cheque No")
    pdc_second_cheque_date = fields.Date(string="Date")
    pdc_second_cheque_amount = fields.Float(string="Amount")

    pdc_third_cheque_no = fields.Char(string="Cheque No")
    pdc_third_cheque_date = fields.Date(string="Date")
    pdc_third_cheque_amount = fields.Float(string="Amount")

    submission_date = fields.Date(string="Date")
    place = fields.Char(string="Place")

    company_name = fields.Char(string="Company Name")
    company_add1 = fields.Char(string="Company Address1",store=True)
    company_add2 = fields.Char(string="Company Address2",store=True)
    company_add3 = fields.Char(string="Company Address3",store=True)
    company_add4 = fields.Char(string="Company Address4",store=True)
    company_add5 = fields.Char(string="Company Address4",store=True)

    company_phone_no = fields.Char(string="Phone",store=True)
    # designation = fields.Char(store='True')
    working_dept = fields.Char(store=True,string="Working Department")

    # contact1_no=fields.Char(store='True',string="Contact No.")
    # contact_off_no = fields.Char(store='True',string="Office No.")
    contact_ll_no = fields.Char(store=True,string="Land Line No.")

    reference_no1 = fields.Char(string="Reference 1",store=True)
    reference_no2 = fields.Char(string="Reference 2",store=True)
    reference_no3 = fields.Char(string="Reference 3",store=True)
    reference_no4 = fields.Char(string="Reference 4",store=True)
    reference_no5 = fields.Char(string="Reference 5",store=True)
    reference_no6 = fields.Char(string="Reference 6",store=True)

    def _get_default_access_token(self):
        access_token = str(uuid.uuid4())
        if self.env['access.token'].create({'name':access_token}):
            return access_token
        return False

    # def get_start_url(self):
    #     return '/survey/start/%s' % self.access_token

    def action_update_student(self):

        partner_data = {
            'name': self.partner_id.name,
            'batch_code': self.batch_code,
            'branch': self.branch,
            'application_for_admission': self.application_for_admission.id,
            'specialization1': self.specialization1.id,
            'specialization2': self.specialization2.id,
            'specialization3': self.specialization3.id,
            'specialization4': self.specialization4.id,
            'nationality': self.nationality.id,
            # 'gender': gender,
            'marital_status': self.marital_status,
            # 'house_no':house_no_1,
            # 'house_name':house_name_1,
            'type': 'contact',
            'street': self.street,
            'landmark': self.landmark,
            'street2': self.street2,
            'city': self.city,
            'zip': self.zip,
            'residential_no': self.residential_no,
            'phone': self.phone,
            'mobile': self.mobile,
            'facebook_id': self.facebook_id,
            'whatsapp_id': self.whatsapp_id,
            'dob': self.dob,
            'email': self.email_from,
            'is_parent': False,
            'is_student': True,
            'is_venue': False,
            'is_company': True,
            'partner_gid': 0,

            'fath_or_hus_name': self.fath_or_hus_name,

        }
        partner_id = int(self.partner_id.id)
        partner_obj = self.env['res.partner'].sudo().browse([partner_id])
        partner_obj.write(partner_data)
        # partner_result = self.env['res.partner'].create(partner_data)

        partner_corre_add_data = {

            'type': 'correspondence_address',
            'parent_id': partner_id,
            'house_no': self.house_no,
            'house_name': self.house_name,
            'street': self.street,
            'landmark': self.landmark,
            'street2': self.street2,
            'city': self.city,
            'zip': self.zip,
            'residential_no': self.residential_no,
            'phone': self.phone,
            'mobile': self.mobile,
            'dob': self.dob,
            'email': self.email_from,
            'is_company': False,

        }
        if self.partner_correspondence_address:
            partner_corr_obj = self.env['res.partner'].sudo().browse([self.partner_correspondence_address.id])
            partner_corr_obj.write(partner_corre_add_data)
        else:
            partner_corr_obj = self.env['res.partner'].create(partner_corre_add_data)
            lead_data = {
                'partner_correspondence_address': partner_corr_obj.id,
            }
            self.write(lead_data)

        partner_per_add_data = {

            'type': 'permanent',
            'parent_id': partner_id,
            'house_no': self.house_no_1,
            'house_name': self.house_name_1,
            'street': self.street_or_road,
            'landmark': self.landmark_1,
            'street2': self.place_1,
            'city': self.city_1,
            'zip': self.zip_1,
            'residential_no': self.residential_no,
            'phone': self.phone,
            'mobile': self.mobile,
            'dob': self.dob,
            'email': self.email_from,
            'is_company': False,

        }

        if self.partner_permanent_address:
            partner_per_obj = self.env['res.partner'].sudo().browse([self.partner_permanent_address.id])
            partner_per_obj.write(partner_per_add_data)
            partner_permanent = self.partner_permanent_address.id
        elif not self.partner_permanent_address and self.house_name_1:
            partner_permanent = self.env['res.partner'].create(partner_per_add_data).id
        else:
            partner_permanent = False
        gender = 'm'
        if self.gender == 'male':
            gender = 'm'
        elif self.gender == 'female':
            gender = 'f'
        student_data={
            'first_name': self.partner_id.name,
            'batch_code':self.batch_code,
            'branch': self.branch,
            'application_for_admission': self.application_for_admission.id,
            'specialization1': self.specialization1.id,
            'specialization2': self.specialization2.id,
            'specialization3': self.specialization3.id,
            'specialization4': self.specialization4.id,
            'birth_date': self.dob,
            'gender': gender,
            'marital_status': self.marital_status,
            'nationality': self.nationality.id,
            'house_no': self.house_no,
            'house_name': self.house_name,
            'street': self.street,
            'landmark': self.landmark,
            'street2': self.street2,
            'city': self.city,
            'zip': self.zip,
            'residential_no': self.residential_no,
            'email': self.email_from,
            'mobile': self.mobile,
            'facebook_id': self.facebook_id,
            'whatsapp_id': self.whatsapp_id,
            'partner_id': partner_id,
            'fath_or_hus_name': self.fath_or_hus_name,
        }
        self.student_id.write(student_data)

        lead_data = {
            'partner_permanent_address': partner_permanent,
        }
        self.write(lead_data)

    def action_create_student(self):
        student = self.env['op.student'].search([('partner_id', '=', self.partner_id.id)])
        user = self.env['res.users'].search([('partner_id', '=', self.partner_id.id)])
        student.user_id = user.id
        if not student:

            partner_data = {
                'name': self.partner_id.name,
                'batch_code': self.batch_code,
                'branch': self.branch,
                'application_for_admission': self.application_for_admission.id,
                'specialization1': self.specialization1.id,
                'specialization2': self.specialization2.id,
                'specialization3': self.specialization3.id,
                'specialization4': self.specialization4.id,
                'nationality': self.nationality.id,
                # 'gender': gender,
                'marital_status': self.marital_status,
                # 'house_no':house_no_1,
                # 'house_name':house_name_1,
                'type': 'contact',
                'street': self.street,
                'landmark': self.landmark,
                'street2': self.street2,
                'city': self.city,
                'zip': self.zip,
                'residential_no': self.residential_no,
                'phone': self.phone,
                'mobile': self.mobile,
                'facebook_id': self.facebook_id,
                'whatsapp_id': self.whatsapp_id,
                'dob': self.dob,
                'email': self.email_from,
                'is_parent': False,
                'is_student': True,
                'is_venue': False,
                'is_company': True,
                'partner_gid': 0,
                'fath_or_hus_name': self.fath_or_hus_name,

            }
            partner_id = int(self.partner_id.id)
            partner_obj = self.env['res.partner'].sudo().browse([partner_id])
            partner_obj.write(partner_data)
            # partner_result = self.env['res.partner'].create(partner_data)

            partner_corre_add_data = {

                'type': 'correspondence_address',
                'parent_id': partner_id,
                'house_no': self.house_no,
                'house_name': self.house_name,
                'street': self.street,
                'landmark': self.landmark,
                'street2': self.street2,
                'city': self.city,
                'zip': self.zip,
                'residential_no': self.residential_no,
                'phone': self.phone,
                'mobile': self.mobile,
                'dob': self.dob,
                'email': self.email_from,
                'is_company': False,

            }
            partner_correspondence = self.env['res.partner'].create(partner_corre_add_data)

            if self.house_name_1:
                partner_per_add_data = {

                    'type': 'permanent',
                    'parent_id': partner_id,
                    'house_no': self.house_no_1,
                    'house_name': self.house_name_1,
                    'street': self.street_or_road,
                    'landmark': self.landmark_1,
                    'street2': self.place_1,
                    'city': self.city_1,
                    'zip': self.zip_1,
                    'residential_no': self.residential_no,
                    'phone': self.phone,
                    'mobile': self.mobile,
                    'dob': self.dob,
                    'email': self.email_from,
                    'is_company': False,

                }
                partner_permanent = self.env['res.partner'].create(partner_per_add_data).id
            else:
                partner_permanent = False

            gender = 'm'
            if self.gender == 'male':
                gender = 'm'
            elif self.gender == 'female':
                gender = 'f'

            student_data={
                'first_name': self.partner_id.name,
                'batch_code':self.batch_code,
                'branch': self.branch,
                'application_for_admission': self.application_for_admission.id,
                'specialization1': self.specialization1.id,
                'specialization2': self.specialization2.id,
                'specialization3': self.specialization3.id,
                'specialization4': self.specialization4.id,
                'birth_date': self.dob,
                'gender': gender,
                'marital_status': self.marital_status,
                'nationality': self.nationality.id,
                'house_no': self.house_no,
                'house_name': self.house_name,
                'street': self.street,
                'landmark': self.landmark,
                'street2': self.street2,
                'city': self.city,
                'zip': self.zip,
                'residential_no': self.residential_no,
                'email': self.email_from,
                'mobile': self.mobile,
                'facebook_id': self.facebook_id,
                'whatsapp_id': self.whatsapp_id,
                'partner_id': partner_id,
                'user_id': user.id,
                'fath_or_hus_name': self.fath_or_hus_name,
            }
            student = self.env['op.student'].create(student_data)

            lead_data = {
                'is_student': True,
                'student_id': student.id,
                'partner_correspondence_address': partner_correspondence.id,
                'partner_permanent_address': partner_permanent,
            }
            self.write(lead_data)
        else:
            partner_correspondence = self.env['res.partner'].search([('type', '=', 'correspondence_address'),
                                                                     ('parent_id', '=', self.partner_id.id)])
            partner_permanent = self.env['res.partner'].search([('type', '=', 'permanent'),
                                                                ('parent_id', '=', self.partner_id.id)])
            lead_data = {
                'is_student': True,
                'student_id': student.id,
                'partner_correspondence_address': partner_correspondence.id if partner_correspondence else False,
                'partner_permanent_address': partner_permanent.id if partner_permanent else False,
            }
            self.write(lead_data)

    def get_start_url(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        base_url += '/application_form/'

        for i in self:
            lead_id = i.id
            url = base_url + str(lead_id)
        return url+'/%s' % self.access_token


    @api.depends('access_token')
    def _get_lead_website_url(self):

        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        base_url += '/application_form/'

        for i in self:
            lead_id=i.id
            url = base_url+str(lead_id)
            i.mail_website_val=werkzeug.urls.url_join(base_url,i.get_start_url()) if i.id else False
        return

    def action_send_mail(self):
        self.ensure_one()
        if not (self.branch and self.admission_register and self.application_for_admission):
            raise UserError(_("Please provide Branch, Application for Admission and Course details"))
        lead_data = {
            'send_status': False,
        }
        self.write(lead_data)

        self.write({'access_token':self._get_default_access_token()})
        template = self.env.ref('openeducat_custom.lead_info_email_template', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='crm.lead',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            #custom_layout="certificate_management.mail_template_data_email_certificate",
        )
        return {
            'name': ('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            # 'custom_layout': "openeducat_custom.mail_notification_lead_application",
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    academic_details_line = fields.One2many('academic.details', 'academic_details_id', string='Academic Details Line')
    work_experience_details_line = fields.One2many('work.experience.details', 'work_experience_details_id',
                                                   string='Work Experience Details Line')

    class Academic_details(models.Model):
        _name = 'academic.details'
        _description = 'academic_details'

        academic_details_id=fields.Many2one('crm.lead',string="Academic Details")
        degree = fields.Char(string='Degree')
        name_of_school = fields.Char(string='Name of School')
        exam_month=fields.Char(string='Exam Month')
        exam_year = fields.Char(string='Exam Year')
        subject = fields.Char(string='Subject')
        result = fields.Char(string='Result')


    class Work_experience_details(models.Model):
        _name = 'work.experience.details'
        _description = 'work_experience_details'

        work_experience_details_id = fields.Many2one('crm.lead', string="Work Experience Details")
        company_name = fields.Char(string='Company Name')
        designation = fields.Char(string='Designation')
        no_of_years = fields.Float(string='No of Years')
