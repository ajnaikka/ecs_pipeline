from odoo import models, fields, api
import uuid


class CrmLead(models.Model):
    _inherit = "crm.lead"

    attachments_details_line = fields.One2many('lead.documents', 'lead_id', string='Attachments Details Line')
    signature = fields.Image('Signature', help='Signature received through the portal.', copy=False, attachment=True,
                             max_width=1024, max_height=1024)
    signature2 = fields.Image('Signature2', help='Signature received through the portal.', copy=False, attachment=True,
                              max_width=1024, max_height=1024)
    signed_by = fields.Char('Signed By', help='Name of the person that signed the Application Form.', copy=False)
    signed_on = fields.Datetime('Signed On', help='Date of the signature.', copy=False)

    def get_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):

        for record in self:
            access_token = str(uuid.uuid4())
            access_url = '/application_form/%s/%s' % (record.id, record.access_token)
            url = access_url + '%s' % (
                suffix if suffix else '',
            )
            url = access_url + '%s?access_token=%s%s%s%s%s' % (
                suffix if suffix else '',
                access_token,
                '&report_type=%s' % report_type if report_type else '',
                '&download=true' if download else '',
                query_string if query_string else '',
                '#%s' % anchor if anchor else ''
            )
            return url


class AttachmentsDetails(models.Model):
    _name = 'lead.documents'

    lead_id = fields.Many2one('crm.lead', string="Attachments Details")
    name = fields.Char(string="Name")
    # type=fields.Binary("Type")
    datas = fields.Binary(string="File Content")
    # file_size=fields.Integer(string="File Size")
    res_model = fields.Char(string="Resource Model")









