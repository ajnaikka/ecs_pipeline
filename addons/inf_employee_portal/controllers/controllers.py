# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, Controller, request, route
import base64
from datetime import datetime,timedelta
from odoo import http, fields
import pytz

class CustomerPortal(Controller):


    @http.route('/my/mail', type='http', auth="user", website=True)
    def send_joining_letter_email(self):
        user = request.env.user
        joining_letter = request.env['joining.letter'].search(
            [('employee_id', '=', user.employee_id.id)], limit=1)

        if joining_letter:
            report = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
                'employee_joining_letter.action_print_joining_letter', [joining_letter.id])[0]

            report_base64 = base64.b64encode(report)

            mail_values = {
                'subject': 'Joining Letter',
                'body_html': '<p>Please find the joining letter attached.</p>',
                'email_to': user.partner_id.email,
                'attachment_ids': [(0, 0, {
                    'name': 'Joining_Letter.pdf',
                    'datas': report_base64,
                    'mimetype': 'application/pdf',
                    'type': 'binary',
                    'store_fname': report_base64,
                    'res_model': 'joining.letter',
                })],
            }


            request.env['mail.mail'].sudo().create(mail_values).send()

            joining_letter.write({'state': 'letter_generated'})

            return request.render('inf_employee_portal.certificate_application_submited_view', {
            'joining_letter': joining_letter})
        else:
            return "Joining letter not found for the current user."

    @http.route('/employee/timeoff/revoke_leave_request', type='http', auth="user", website=True)
    def revoke_leave_request(self, **post):
        leave_id = post.get('leave_id')
        leave_types = request.env['hr.leave.type'].sudo().search([])


        if leave_id:
            leave = request.env['hr.leave'].sudo().browse(int(leave_id))
            if leave:
                leave.sudo().write({'state': 'draft'})
        return request.render('inf_employee_portal.employee_timeoff_form',{'leave':leave,'leave_types':leave_types})


    @http.route('/employee/timeoff/confirm', type='http', auth="user", website=True)
    def revoke_leave_request_confirm(self, **post):
        leave_id = post.get('leave_id')
        leave_types = request.env['hr.leave.type'].sudo().search([])

        if leave_id:
            leave = request.env['hr.leave'].sudo().browse(int(leave_id))
            if leave:
                leave.sudo().write({'state': 'confirm'})
        return request.render('inf_employee_portal.employee_timeoff_form',{'leave':leave,'leave_types':leave_types})




    @http.route(['/my/employees'], type='http', auth='user', website=True)
    def employee(self):
        hr = request.env.user.employee_id.hr_manager_id
        employee = request.env.user.employee_id
        return request.render('inf_employee_portal.employee_list_form', {'hr': hr,'employee':employee,'email':hr.work_email})

    @http.route('/employee/timeoff/enter_details', auth='user', website=True)
    def enter_details_page(self, **kw):
        leaves = kw.get('leave_id')
        manager = request.env.user.employee_id.parent_id

        leave = request.env['hr.leave'].sudo().browse(int(leaves)) if leaves else False


        return request.render('inf_employee_portal.enter_details_template', { 'leave': leave,'revoke_manager': manager})


    @http.route(['/employee/timeoff_form'], type='http', auth='user', website=True)
    def employee_timeoff_form(self, leave_id=None, **post):
        hr = request.env.user.employee_id.hr_manager_id
        employee = request.env.user.employee_id
        leave_types = request.env['hr.leave.type'].sudo().search([])

        leave = request.env['hr.leave'].sudo().browse(int(leave_id)) if leave_id else False

        return request.render('inf_employee_portal.employee_timeoff_form',
                              {'hr': hr, 'employee': employee,'leave_types': leave_types,
                               'leave': leave})

    @http.route(['/employee/timeoff'], type='http', auth='user', website=True)
    def employee_timeoff(self, **post):
        employee = request.env.user.employee_id
        leave_types = request.env['hr.leave'].sudo().search([('employee_id','=',employee.id)],order='create_date desc')
        leave_type = request.env['hr.leave.type'].sudo().search([])

        return request.render('inf_employee_portal.time_off_tree_view',
                              {'leave_types': leave_types,'leave_type':leave_type})

    @http.route(['/employee/expense_form'], type='http', auth='user', website=True)
    def employee_expense_form(self, expense_id=None, **post):
        hr = request.env.user.employee_id.hr_manager_id
        employee_profile = request.env.user.employee_id.profile_id.id
        employee = request.env.user.employee_id.id
        exp_product = request.env['product.product'].sudo().search(
            [('can_be_expensed', '=', True), ('profile_id', '=', employee_profile)])
        company_id = request.env.company.id

        taxes = request.env['account.tax'].sudo().search(
            [('company_id', '=', company_id), ('type_tax_use', '=', 'purchase')])

        emp_operation = request.env['employee.profile'].sudo().search([('id','=',employee_profile)],limit=1)

        expense = request.env['hr.expense'].sudo().browse(int(expense_id)) if expense_id else False


        # files = []
        # for file in expense:
        #     download_url = '/web/content/%s/%s/file/%s' % (file._name, file.id, file.file_name) + '?download=true'
        #     image = '/web/image/%s/%s/image' % (file._name, file.id)
        #     files.append({
        #         'download_url': download_url,
        #         'image': image
        #     })
        #



        date_today = fields.Date.today()



        currency = request.env.company.currency_id

        return request.render('inf_employee_portal.employee_expenses_form',
                              {'hr': hr, 'employee': employee, 'exp_product': exp_product,
                               'expense': expense, 'date_today': date_today, 'emp_operation': emp_operation, 'taxes': taxes,
                               'currency': currency
                               })

    @http.route(['/employee/expenses'], type='http', auth='user', website=True)
    def employee_expenses(self, **post):
        employee = request.env.user.employee_id
        expense = request.env['hr.expense'].sudo().search([('employee_id','=',employee.id)])
        return request.render('inf_employee_portal.expense_tree_view',
                              {'expenses': expense})

    @http.route(['/employee/timeoff/submit'], type='http', auth='user', website=True)
    def employee_timeoff_submit(self, **post):

        time_off_type = post.get('time_off_type')
        request_date_from_period = post.get('request_date_from_period')
        date_from = post.get('date_from')
        date_to = post.get('date_to')
        attachments = request.httprequest.files.getlist('attachment')
        half_day = post.get('halfDay')
        full_day = post.get('fullDay')
        description = post.get('description')
        employee = request.env.user.employee_id
        company = request.env.company.id
        type = request.env['hr.leave.type'].sudo().search([('id', '=', time_off_type)])

        hour_from = post.get('hourFrom')
        hour_to = post.get('hourTo')

        attachment_ids = []
        for attachment in attachments:
            attachment_data = {
                'name': attachment.filename,
                'datas': base64.b64encode(attachment.read()),
                'res_model': 'hr.leave',
            }
            attachment_id = request.env['ir.attachment'].sudo().create(attachment_data)
            attachment_ids.append(attachment_id.id)

        time_off_obj = request.env['hr.leave']
        time_off_obj.sudo().create({
            'holiday_status_id': type.id,
            'request_date_from': date_from,
            'request_date_to': date_to if date_to else date_from,
            'request_unit_half': half_day if half_day else False,
            'request_unit_hours': full_day if full_day else False,
            'employee_id': employee.id,
            'name': description,
            'company_id': company,
            'request_hour_from': hour_from if hour_from else False,
            'request_hour_to': hour_to if hour_to else False,
            'request_date_from_period': request_date_from_period,
            'supported_attachment_ids': [(6, 0, attachment_ids)]
        })

        return request.render('inf_employee_portal.certificate_application_submited_view',
                              {'time_off_type': time_off_type})



        return request.render('inf_employee_portal.certificate_application_submited_view', {'time_off_type': time_off_type})

    @http.route(['/employee/expense/submit'], type='http', auth='user', website=True)
    def employee_expense_submit(self, **post):

        exp_cat_id = int(post.get('cat_type'))
        exp_cat = request.env['product.product'].sudo().browse(exp_cat_id)

        taxes = [(6, 0, [int(post.get('taxes'))]) if post.get('taxes') else False]
        total = float(post.get('total'))
        description = post.get('description')
        attachments = request.httprequest.files.getlist('attachments')

        exp_type = post.get('expense_type')


        employee = request.env.user.employee_id

        expense_vals = {
            'product_id': exp_cat.id,
            'employee_id': employee.id,
            # 'tax_ids': taxes,
            'total_amount': total,
            'description': description,
            'type': exp_type,

        }

        expense_obj = request.env['hr.expense'].sudo()
        new_expense = expense_obj.create(expense_vals)

        attachment_ids = []
        for attachment in attachments:
            attachment_data = {
                'name': attachment.filename,
                'datas': base64.b64encode(attachment.read()),
                'res_model': 'hr.expense',
                'res_id': new_expense.id,
            }
            attachment_id = request.env['ir.attachment'].sudo().create(attachment_data)
            attachment_ids.append(attachment_id.id)

        new_expense.attachment_ids = [(6, 0, attachment_ids)]

        new_expense.action_submit_expenses()
        if new_expense.sheet_id:
            new_expense.sheet_id.action_submit_sheet()

        return request.render('inf_employee_portal.certificate_application_submited_view', {'exp_cat_id': exp_cat_id})




    @http.route(['/my/notification'], type='http', auth='user', website=True)
    def notification(self):
        today = datetime.now().date()

        current_user = request.env.user.name
        month_day = (today.month, today.day)
        employees_birthday = request.env['hr.employee'].sudo().search([
            ('birthday', 'like', '-{:02d}-{:02d}'.format(*month_day))
        ])
        employees_work_anniversary = request.env['hr.employee'].sudo().search([('current_contract_start', 'like', '-{:02d}-{:02d}'.format(*month_day))])

        user_tz = pytz.timezone(request.env.user.tz or 'UTC')

        now = datetime.now(user_tz)


        tomorrow_start = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        tomorrow_end = tomorrow_start.replace(hour=23, minute=59, second=59, microsecond=0)



        tomorrow_start_utc = tomorrow_start.astimezone(pytz.UTC)
        tomorrow_end_utc = tomorrow_end.astimezone(pytz.UTC)


        public_holidays = request.env['resource.calendar.leaves'].sudo().search([
            ('date_from', '>=', tomorrow_start_utc),
            ('date_to', '<=', tomorrow_end_utc)
        ])

        employee_announcements = request.env['hr.employee.announcement'].sudo().search([
            ('date', '=', today)
        ])


        notification_count = len(employees_birthday) + len(employees_work_anniversary) + len(public_holidays) +  len(employee_announcements)
        employee = request.env.user.employee_id
        if not employee.have_agreed_policy:
            return request.redirect('/my')
        else:
            return request.render('inf_employee_portal.notification_template', {
                'employees_birthday': employees_birthday,
                'employees_work_anniversary': employees_work_anniversary,
                'public_holidays': public_holidays,
                'employee_announcements': employee_announcements,
                'notification_count': notification_count,
                'current_user': current_user
            })

    @http.route(['/my/welcome_page'], type='http', auth='user', website=True)
    def welcome_page(self):
        employee = request.env.user.employee_id
        if not employee.have_agreed_policy:
            return request.redirect('/my')
        else:
            return request.render('inf_employee_portal.infinews_welcome_page')

    @http.route('/my/employee_list', type='http', auth='user', website=True)
    def show_employee_list(self, **kw):
        employees = request.env['hr.employee'].sudo().search([('user_id', '=', http.request.env.user.id)],limit=1)
        today = datetime.now().date()

        month_day = (today.month, today.day)
        employees_birthday = request.env['hr.employee'].sudo().search([
            ('birthday', 'like', '-{:02d}-{:02d}'.format(*month_day))
        ])
        employees_work_anniversary = request.env['hr.employee'].sudo().search(
            [('current_contract_start', 'like', '-{:02d}-{:02d}'.format(*month_day))])

        user_tz = pytz.timezone(request.env.user.tz or 'UTC')

        now = datetime.now(user_tz)

        tomorrow_start = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        tomorrow_end = tomorrow_start.replace(hour=23, minute=59, second=59, microsecond=0)

        tomorrow_start_utc = tomorrow_start.astimezone(pytz.UTC)
        tomorrow_end_utc = tomorrow_end.astimezone(pytz.UTC)

        public_holidays = request.env['resource.calendar.leaves'].sudo().search([
            ('date_from', '>=', tomorrow_start_utc),
            ('date_to', '<=', tomorrow_end_utc)
        ])

        employee_announcements = request.env['hr.employee.announcement'].sudo().search([
            ('date', '=', today)
        ])

        notification_count = len(employees_birthday) + len(employees_work_anniversary) + len(public_holidays) + + len(
            employee_announcements)
        employee = request.env.user.employee_id
        if not employee.have_agreed_policy:
            return request.redirect('/my')
        else:
            return request.render('inf_employee_portal.employee_list_template', {'employees': employees,'notification_count': notification_count})

    @http.route('/send_email_notification', type='http', auth="public", website=True)
    def send_email_notification(self, **post):
        subject = post.get('subject')
        description = post.get('description')
        employee_email = post.get('employee_email')

        mail_values = {
            'subject': subject,
            'email_to': employee_email,
            'body_html': description,
        }

        mail = request.env['mail.mail'].sudo().create(mail_values)
        mail.send()

        return request.render('inf_employee_portal.certificate_application_submited_view', {
            'subject': subject})

    @http.route('/revoke_request', type='http', auth='user', website=True)
    def revoke_request_form(self, **post):

        manager = post.get('revoke_hr_manager')
        attachments = request.httprequest.files.getlist('attachments')
        sub = post.get('subject')
        description = post.get('description')

        manager_emp = request.env['hr.employee'].sudo().browse(int(manager)) if manager else False

        if manager_emp.user_id.partner_id:
            attachment_ids = []

            for attachment in attachments:
                attachment_data = {
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'mail.mail',
                }
                attachment_id = request.env['ir.attachment'].sudo().create(attachment_data)
                attachment_ids.append(attachment_id.id)

            att = request.env['ir.attachment'].sudo().browse(attachment_ids)
            att.write({'public': True})

            mail_user = manager_emp.user_id.id
            user_revoke = request.env['res.users'].sudo().browse(mail_user)

            message_post = request.env.user.partner_id.message_post(
                body=description,
                subject=sub,
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
                author_id=request.env.user.partner_id.id
            )


            if message_post:
                notification_values = []
                for user in user_revoke:
                    existing_notification = request.env['mail.notification'].sudo().search([
                        ('res_partner_id', '=', user.partner_id.id),
                        ('mail_message_id', '=', message_post.id)
                    ])
                    if not existing_notification:
                        notification_values.append({
                            'res_partner_id': user.partner_id.id,
                            'mail_message_id': message_post.id
                        })

                if notification_values:
                    message_post.sudo().notification_ids = [(0, 0, vals) for vals in notification_values]

            mail_values = {
                'author_id': request.env.user.partner_id.id,
                'auto_delete': True,
                'body_html': description,
                'email_from': request.env.user.email_formatted,
                'email_to': manager_emp.work_email,
                'subject': sub,
                'attachment_ids': [(6, 0, attachment_ids)],
            }


            request.env['mail.mail'].sudo().create(mail_values).send()

        return request.render('inf_employee_portal.certificate_application_submited_view',
                              {'revoke_hr_manager': manager})


    @http.route('/my/send_mail', type='http', auth='user', website=True)
    def submit(self, **kw):
        email = kw.get('email')
        subject = kw.get('subject')
        description = kw.get('description')
        attachments = request.httprequest.files.getlist('attachments')


        try:
            mail_values = {
                'author_id': request.env.user.partner_id.id,
                'email_from': request.env.user.email_formatted,
                'auto_delete': True,
                'email_to': email,
                'subject': subject,
                'body_html': description,
            }
            mail = request.env['mail.mail'].sudo().create(mail_values)

            vals = {
                'send_to':request.env.user.employee_id.hr_manager_id.user_id.employee_id.id,
                'date': fields.Date.today(),
                'company_id': request.env.user.company_id.id,
                'user_id':request.env.user.id

            }



            test = request.env['employee.certificate.details'].sudo().create(vals)



            attachment_ids = []

            if attachments:
                for attachment in attachments:
                    attachment_data = {
                        'name': attachment.filename,
                        'datas': base64.b64encode(attachment.read()),
                        'res_model': 'mail.mail',
                        'res_id': mail.id,
                    }
                    attachment_id = request.env['ir.attachment'].sudo().create(attachment_data)
                    attachment_ids.append(attachment_id.id)

                mail.attachment_ids = [(6, 0, attachment_ids)]
                test.attachment_ids = [(6, 0, attachment_ids)]



            mail.send()

            return request.render('inf_employee_portal.certificate_application_submited_view')

        except Exception as e:
            error_message = f"An error occurred while sending the email: {str(e)}"
            return error_message




