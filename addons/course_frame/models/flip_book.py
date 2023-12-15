# -*- coding: utf-8 -*-
from datetime import date, datetime, time
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FlipBook(models.Model):
    _name = 'flip.book'
    _inherit = ['mail.thread', 'mail.activity.mixin',
                'website.cover_properties.mixin',
                'website.seo.metadata',
                'website.published.multi.mixin',
                'website.searchable.mixin',
                ]
    _description = 'Flip Book Library'

    name = fields.Char('Name', copy=False, tracking=True, required=True, default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'),
                              ('assigned', 'Assigned'),
                              ('uploaded', 'PDF Uploaded'),
                              ('generated', 'FB Generated'),
                              ('ready', 'FB Ready')],
                             copy=False, tracking=True, default='draft')
    date = fields.Date('Date', default=date.today())
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', 'Team Lead', required=True, tracking=True,
                              default=lambda self: self.env.user, domain=lambda self: [
            ("groups_id", "=", self.env.ref("course_frame.group_academy_team_lead").id)])
    content_developer_id = fields.Many2one('res.users', 'Content Developer', required=True, tracking=True,
                                           domain=lambda self: [("groups_id", "=", self.env.ref(
                                               "course_frame.group_academy_content_writer").id)])
    course_id = fields.Many2one('op.course', 'Course')
    subject_id = fields.Many2one('op.subject', 'Subject')
    unit_id = fields.Many2one('subject.unit', 'Unit')
    topic_id = fields.Many2one('subject.topic', 'Topic')
    attachment_id = fields.Many2many('ir.attachment', string='Attachment', ondelete='cascade')
    api_code = fields.Char('Api Key', related='company_id.api_key')
    url = fields.Char('Url')
    remark = fields.Text('Remark')
    flip_book = fields.Text('Flip Book')
    is_content_developer = fields.Boolean('Is Content Developer', compute='compute_is_content_developer')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('flip.book') or _('New')
        request = super(FlipBook, self).create(vals)
        return request

    # def compute_url(self):
    #     for data in self:
    #         if data.attachment_id and data.api_code:
    #             a = self.env['ir.config_parameter'].get_param('web.base.url')
    #             b = self.env['ir.attachment'].browse(data.attachment_id.id)
    #             pdf_link = str(a) + str(b.local_url)
    #             # pdf_link = 'http://3.6.233.15/web/image/3454?unique=6114011ca1d119beb759daa24b84b71a89612857'
    #             key = data.api_code
    #             get_project_url = "https://heyzine.com/api1/rest?pdf=" + pdf_link + "&k=" + key
    #             headers = {
    #                 'User-Agent': 'My User Agent 1.0',
    #                 'Accept-Encoding': 'gzip, deflate',
    #                 'Connection': 'keep-alive',
    #                 'Authorization': 'Bearer my-access-token'
    #             }
    #             response = requests.get(url=get_project_url, headers=headers)
    #             data_received = response.json()
    #             print(data_received)
    #             # data.url = 'https://heyzine.com/flip-book/ea25138512.html'
    #             if data_received['success'] != False:
    #                 data.url = data_received['url']
    #             else:
    #                 data.url = ' '
    #         else:
    #             data.url = ''

    def action_assign(self):
        for data in self:
            if not data.content_developer_id:
                raise UserError(_("Please select the Content Developer."))
            partners = []
            subtype_ids = self.env['mail.message.subtype'].search(
                [('res_model', '=', 'flip.book')]).ids
            for user in data.content_developer_id:
                self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                partners.append(user.partner_id.id)
            body = _(
                u'Hello ' + data.content_developer_id.name + ', ' + data.user_id.name + ' Assigns the Flip Book Creation ' + data.name + '. And assigned it to you Please do the needful.')
            data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'assigned'})

    def action_upload_pdf(self):
        for data in self:
            if not data.attachment_id:
                raise UserError(_("Please upload the PDF Document."))
            return data.write({'state': 'uploaded'})

    def action_fb_generate(self):
        for data in self:
            if data.url:
                data.get_default_flipbook()
                partners = []
                subtype_ids = self.env['mail.message.subtype'].search(
                    [('res_model', '=', 'flip.book')]).ids
                for user in data.user_id:
                    self.message_subscribe(partner_ids=[user.partner_id.id], subtype_ids=subtype_ids)
                    partners.append(user.partner_id.id)
                body = _(
                    u'Hello ' + data.user_id.name + ', ' + data.content_developer_id.name + 'Prepare the Flip Book ' + data.name + '. Please Check.')
                data.message_post(body=body, partner_ids=partners)
            return data.write({'state': 'generated'})

    def action_regenerate(self):
        for data in self:
            return data.write({'state': 'uploaded'})

    def get_default_flipbook(self):
        for data in self:
            if data.url:
                val = data.url
                result = """
                    <div class="text-monospace pt8 bg-light">
                          <iframe src="{}" width="100%" height="480" seamless="seamless" scrolling="no" frameborder="0" allowfullscreen=""></iframe>
                        </div>
                    """.format(val)
                data.flip_book = result
            else:
                data.flip_book = ''

    def compute_is_content_developer(self):
        for data in self:
            if data.content_developer_id.id == self.env.user.id:
                data.is_content_developer = True
            else:
                data.is_content_developer = False
