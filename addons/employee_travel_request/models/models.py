# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, RedirectWarning


class TravelRequest(models.Model):
    _name = 'travel.request'
    _description = 'Travel Request'
    _order = 'id desc'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    travel_place_ids = fields.One2many('travel.place', 'place_id', string='Travel Details')

    @api.model
    def default_get(self, fields_list):
        res = super(TravelRequest, self).default_get(fields_list)
        vals = [
            (0, 0, {'name': 'Place of Travel 1'}),
            (0, 0, {'name': 'Place of Travel 2'}),
            (0, 0, {'name': 'Place of Travel 3'})
        ]
        res.update({'travel_place_ids': vals})
        return res

    request_date = fields.Date(string='Request Date', format='%d-%m-%y', default=lambda self: fields.Date.today(),
                               readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', default=lambda self: self.env.user.employee_id,
                                  readonly=True)
    description = fields.Char(string="Description", )
    refuse_reason = fields.Char(string="Refuse Reason", )
    start_date = fields.Date(string='Travel Start Date')
    end_date = fields.Date(string='Travel End Date')
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('travel_req', 'Travel Approve Request to Manager'),
        ('approve_manager', 'Approved by Manager'),
        ('refuse_manager', 'Refused by Manager'),

    ], default='draft')

    comment = fields.Text(string="Comment")
    # email_to = fields.Many2one('res.partner', string="To", required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False,
                                 default=lambda self: self.env.company)

    def generate_travel_request_button(self, ctx=None):
        self.request_date = fields.Date.today()

        # Prepare email body
        email_body = f"""Dear Manager,<br/><br/>
    Please review and proceed with my travel request to {','.join(line.place_name for line in self.travel_place_ids if line.place_name)} for the following date period:<br/>
    <br/>
    Travel Description: {self.description}<br/>

    Start Date: {self.start_date}<br/>
    End Date: {self.end_date}<br/>
    <br/>
    Best regards,<br/>
    {self.employee_id.name}<br/>
    """

        # Send email
        mail_values = {
            'subject': 'Travel Approval request',
            'body_html': email_body,
            'email_from': self.employee_id.work_email,
            'email_to': self.employee_id.parent_id.work_email,
        }
        self.env['mail.mail'].create(mail_values).send()

        self.write({'state': 'travel_req'})

        return True

    def approve_travel_request_button(self, ctx=None):
        # Prepare email body
        email_body = f"""Dear {self.employee_id.name},<br/><br/>
          Your travel request to {','.join(line.place_name for line in self.travel_place_ids if line.place_name)} for the following date period has been approved:<br/>
                    Travel Description: {self.description}<br/>

          Start Date: {self.start_date}<br/>
          End Date: {self.end_date}<br/>
          <br/>
          Best regards,<br/>
          Manager <br/>
          """

        # Send email
        mail_values = {
            'subject': 'Travel Approval request',
            'body_html': email_body,
            'email_from': self.employee_id.parent_id.work_email,
            'email_to': self.employee_id.work_email,
        }
        self.env['mail.mail'].create(mail_values).send()

        self.write({'state': 'approve_manager'})

        return True

    def refuse_travel_request_button(self, ctx=None):
        self.request_date = fields.Date.today()
        if not self.refuse_reason:
            raise UserError("Please provide a reason to refuse the travel request.")

        # Prepare email body
        email_body = f"""Dear {self.employee_id.name},<br/><br/>
         Your travel request to {','.join(line.place_name for line in self.travel_place_ids if line.place_name)} for the following date period has been refused. <br/>
         
         Travel Description: {self.description}<br/>

       Start Date: {self.start_date}<br/>
       End Date: {self.end_date}<br/>
       Reason to Refuse :{self.refuse_reason}<br/>
       <br/>
       Best regards,<br/>
         Manager <br/>
       """

        # Send email
        mail_values = {
            'subject': 'Travel Approval request',
            'body_html': email_body,
            'email_from': self.employee_id.parent_id.work_email,
            'email_to': self.employee_id.work_email,
        }
        self.env['mail.mail'].create(mail_values).send()

        self.write({'state': 'refuse_manager'})

        return True


class TravelActivity(models.Model):
    _name = 'travel.place'
    _description = 'Travel Activity'

    name = fields.Char(string='Travel Places', required=1)
    place_name = fields.Char(string='Description',required=0)
    place_id = fields.Many2one('travel.request', string='Travel Place')
