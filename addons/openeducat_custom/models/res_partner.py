from odoo import models, fields, api


class PartnerTemplate(models.Model):
    _inherit = 'res.partner'

    branch = fields.Char(store='True', string="Branch")
    batch_code = fields.Char(store='True', string="Batch Code")
    application_for_admission = fields.Many2one('op.course', string="Application For Admission")

    specialization1 = fields.Many2one('op.specialization', string="Specialization1")
    specialization2 = fields.Many2one('op.specialization', string="Specialization2")
    specialization3 = fields.Many2one('op.specialization', string="Specialization3")
    specialization4 = fields.Many2one('op.specialization', string="Specialization4")

    dob = fields.Date(string='DOB')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender',  index=True, default='male')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
    ], string='Marital Status',  index=True, default='single')
    fath_or_hus_name = fields.Char(store='True', string="Father's / Husband's Name")
    residential_no = fields.Char(store='True', string="Residential No")
    facebook_id = fields.Char(store='True', string="Facebook Id")
    whatsapp_id = fields.Char(store='True', string="Whatsapp Id")
    nationality = fields.Many2one('res.country', 'Nationality')
    landmark = fields.Char(store='True', string="Landmark")

    house_no = fields.Char(store='True', string="House No")
    house_name = fields.Char(store='True', string="House Name")
    type = fields.Selection(selection_add=[('correspondence_address', 'Correspondence Address'),('permanent', 'Permanent Address')])















