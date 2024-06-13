# -*- coding: utf-8 -*-
import base64
from io import BytesIO
from venv import logger
from odoo import http, fields
from odoo.http import content_disposition, Controller, request, route
import datetime
from odoo.addons.portal.controllers.portal import CustomerPortal, pager


def get_month_list():
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    return months


def get_year_list(start_year, end_year):
    years = [str(year) for year in range(start_year, end_year + 1)]
    return years


def is_month_in_date_range(month, year, start_date, end_date):
    # Convert start_date and end_date to datetime objects
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    # Create datetime object for the given month
    given_month = datetime.datetime(year, datetime.datetime.strptime(month, "%B").month, 1)

    # Check if the given month falls within the date range
    return start_date <= given_month <= end_date


class PayslipPortal(CustomerPortal):

    @http.route(['/my/employees/payslip'], type='http', auth='user', website=True)
    def employee_payslip(self, **kwargs):
        months = get_month_list()
        start_year = 2016
        end_year = 2035
        years = get_year_list(start_year, end_year)
        employee = request.env.user.employee_id

        employee_payslips = request.env['hr.payslip'].sudo().search(
            [("employee_id", "=", employee.id), ("state", "=", 'paid')])
        payslip_list = []
        for payslip in employee_payslips:
            attachment = request.env['ir.attachment'].sudo().search([("res_id", "=", payslip.id)], limit=1)
            if kwargs.get('month') or kwargs.get('year'):
                if kwargs.get('month') != 'select' and kwargs.get('year') != 'select':
                    start_date = str(payslip.date_from)
                    end_date = str(payslip.date_to)
                    month = kwargs.get('month')
                    year = int(kwargs['year'])

                    if is_month_in_date_range(month, year, start_date, end_date):
                        pdata = {
                            "id": payslip.id,
                            "display_name": payslip.display_name,
                            "from": payslip.date_from,
                            "to": payslip.date_to,
                            "attachment": attachment.id
                        }
                        payslip_list.append(pdata)
        data = {
            "months": months,
            "years": years,
            "payslips": payslip_list if employee_payslips else False
        }
        return http.request.render('loyal_portal_payslip_generate.portal_my_payslips', data)

    @http.route(['/my/payslip/<int:payslip_id>'], type='http', auth="public", website=True)
    def employee_payslip_generate(self, **kwargs):
        payslip_id = kwargs.get('payslip_id')
        if payslip_id:
            payslip = request.env['hr.payslip'].sudo().browse(int(payslip_id))
            if payslip:
                attachment = request.env['ir.attachment'].sudo().search([("res_id", "=", payslip.id)], limit=1)
                data = {
                    "id": payslip.id,
                    "attachment": attachment
                }
                return http.request.render('loyal_portal_payslip_generate.portal_my_payslip', data)

    @http.route('/website/download_pdf/<int:attachment_id>', type='http', auth='public')
    def download_pdf(self, attachment_id, **kwargs):
        # Fetch the attachment by id
        attachment = request.env['ir.attachment'].sudo().browse(attachment_id)
        if attachment and attachment.mimetype == 'application/pdf':
            # Return the PDF content as a file download response
            return http.send_file(BytesIO(base64.b64decode(attachment.datas)), filename=attachment.name,
                                  as_attachment=True)
        else:
            # Handle case where attachment is not found or is not a PDF
            return request.not_found()

    @http.route("/my/payslip/print/<int:payslip_id>", auth="public", type="http")
    def print_payslip_pdf(self, payslip_id, report_type=None, access_token=None, download=False, **kw):
        payslip = request.env['hr.payslip'].sudo().browse(payslip_id)
        return self._show_report(model=payslip, report_type='pdf',
                                 report_ref='infinous_user_groups.infi_payroll_template',
                                 download=download)
