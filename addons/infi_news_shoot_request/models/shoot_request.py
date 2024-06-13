from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ShootRequest(models.Model):
    _name = 'shoot.request'
    _description = 'Shoot Request'
    _order = 'id desc'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    issued_date = fields.Date(string='Issued Date', format='%d-%m-%y')
    request_date = fields.Date(string='Request Date', format='%d-%m-%y')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('shoot_req', 'Shoot Request'),
        ('to_storeperson', 'Request To store Person'),
        ('to_reporter', 'Assign To Reporter'),
        ('cancel', 'Canceled'),
        ('closed', 'Closed'),
    ], default='draft')

    kit_line_ids = fields.One2many('kit.line', 'request_id', string='Components')
    camera_unit_id = fields.Many2one('product.template', string="Camera Unit")
    boq_id = fields.Many2one('kit.component', string="Camera Unit")
    comment = fields.Text(string="Comment")
    # email_to = fields.Many2one('res.partner', string="To", required=True)
    is_to_store_in_charge = fields.Boolean(string="Store in charge")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False,
                                 default=lambda self: self.env.company)

    @api.onchange('boq_id')
    def _onchange_boq_id(self):
        if self.boq_id:
            self.kit_line_ids = [
                                    (0, 0, {
                                        'component_id': self.boq_id.product_id.id,  # Main product
                                        'quantity': 1,  # Quantity of main product (assuming it's always 1)
                                        'uom_id': self.boq_id.uom_id.id,  # UOM of main product
                                    })
                                ] + [
                                    (0, 0, {
                                        'component_id': line.product_id.id,
                                        'quantity': line.quantity,
                                        'uom_id': line.uom_id.id,
                                    }) for line in self.boq_id.product_line_ids
                                ]

    assignment_team_emails = fields.Many2many(
        'res.users', string='Assignment Team',
        compute='_compute_assignment_team_emails', store=True,
        relation='assignment_team_emails_relation'
    )

    @api.depends('company_id')
    def _compute_assignment_team_emails(self):
        assignment_team_group = self.env.ref('infinous_user_groups.assigment_team')
        self.assignment_team_emails = assignment_team_group.users


    def shoot_request_button(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_news_shoot_request.employee_resignation_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'shoot.request',
            'default_res_ids': [self.id],
            # 'default_partner_ids': [self.email_to.id],
            'default_shoot_req_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': None,
            'force_email': True,
            'default_email_from': self.env.user.partner_id.email,
            'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        }

        if ctx:
            context.update(ctx)
        print(context,'context')

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'views_id': compose_form_id,
            'target': 'new',
            'context': context,
        }
    def product_out(self):
        template_values = {
            'name': 'Confirmation Regarding shoot request frowarded to store person',
            'subject': 'Confirmation Regarding shoot request frowarded to store person',
            'body_html': """
                                                <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                                    <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                        <strong>Confirmation Regarding shoot request forwarded to store in Charge</strong>
                                                    </p>
                                                    <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                        <b>Dear %s,</b>
                                                    </p>
                                                    <br/>
                                                    <br/>
                                                    <p>
                                                        Your request has been forwarded to Store in charge
                                                    </p>
                                                    <br/>
                                                    <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                        Thank You
                                                    </p>
                                                </div>
                                            """ % (
                self.employee_id.name),
            'model_id': self.env.ref('hr.model_hr_employee').id,
            # Replace 'hr' and 'model_hr_employee' with your actual module and model names
        }
        email_template = self.env['mail.template'].create(template_values)
        mail_template = self.env['mail.template'].browse(email_template.id)

        # Render the email content
        rendered_message = mail_template.body_html

        mail = self.env['mail.mail'].sudo().create({
            'subject': mail_template.subject,
            'body_html': rendered_message,
            'email_from': self.env.user.email,  # Use the actual sender email
            'email_to': self.employee_id.work_email,
        })
        mail.send()

    store_incharge_emails = fields.Many2many(
        'res.users', string='Store Incharge',
        compute='_compute_store_incharge_emails', store=True,
        relation='store_incharge_emails_relation'
    )

    def _compute_store_incharge_emails(self):
        store_incharge_group = self.env.ref('infinous_user_groups.store_in_charge')
        self.store_incharge_emails = store_incharge_group.users

    def req_storeperson(self,ctx=None):
        self.is_to_store_in_charge = True
        self.product_out()
        template = self.env.ref('infi_news_shoot_request.camera_unit_store_person_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'shoot.request',
            'default_res_ids': [self.id],
            'default_shoot_req_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': None,
            'force_email': True,
            'default_email_from': self.env.user.partner_id.email,
            'default_partner_id_bool': True,
            'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        }

        if ctx:
            context.update(ctx)

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'views_id': compose_form_id,
            'target': 'new',
            'context': context,
        }

    def stock_out(self):
        self.issued_date = fields.Date.today()
        self.state = "to_reporter"
        template_values = {
            'name': 'Confirmation Regarding Camera Unit from Store In charge',
            'subject': 'Confirmation Regarding Camera Unit from Store In charge',
            'body_html': """
                                                        <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                                            <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                                <strong>Confirmation Regarding Camera Unit From store in charge</strong>
                                                            </p>
                                                            <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                                <b>Dear %s,</b>
                                                            </p>
                                                            <br/>
                                                            <br/>
                                                            <p>
                                                                Camera unit is successfully assigned to you
                                                            </p>
                                                            <br/>
                                                            <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                                Thank You
                                                            </p>
                                                        </div>
                                                    """ % (
                self.employee_id.name),
            'model_id': self.env.ref('hr.model_hr_employee').id,
            # Replace 'hr' and 'model_hr_employee' with your actual module and model names
        }
        email_template = self.env['mail.template'].create(template_values)
        mail_template = self.env['mail.template'].browse(email_template.id)

        # Render the email content
        rendered_message = mail_template.body_html

        mail = self.env['mail.mail'].sudo().create({
            'subject': mail_template.subject,
            'body_html': rendered_message,
            'email_from': self.env.user.email,  # Use the actual sender email
            'email_to': self.employee_id.work_email,
        })
        mail.send()

        _logger.debug("Default Source Location: %s", self.env.company.picking_type.default_location_src_id)

        picking_vals = {
            'picking_type_id': self.env.company.picking_type.id,
            'location_id': self.env.company.picking_type.default_location_src_id.id,
            'location_dest_id': self.env.company.picking_type.default_location_dest_id.id,
            'move_ids_without_package': [],
        }

        for kit_line in self.kit_line_ids:
            move_line_vals = {
                'name': 'Stock Transfer',
                'product_id': kit_line.component_id.id,
                'product_uom_qty': kit_line.quantity,
                'product_uom': kit_line.uom_id.id,
                'location_id': picking_vals['location_id'],
                'location_dest_id': picking_vals['location_dest_id'],
            }
            picking_vals['move_ids_without_package'].append((0, 0, move_line_vals))

        picking = self.env['stock.picking'].create(picking_vals)
        picking.button_validate()

    def stock_in(self):
        _logger.debug("Default destination Location: %s", self.env.company.picking_type.default_location_src_id)

        picking_vals = {
            'picking_type_id': self.env.company.picking_type.id,
            'location_id': self.env.company.picking_type.default_location_dest_id.id,
            'location_dest_id': self.env.company.picking_type.default_location_src_id.id,
            'move_ids_without_package': [],
        }

        for kit_line in self.kit_line_ids:
            move_line_vals = {
                'name': 'Stock Transfer',
                'product_id': kit_line.component_id.id,
                'product_uom_qty': kit_line.quantity,
                'product_uom': kit_line.uom_id.id,
                'location_id': picking_vals['location_id'],
                'location_dest_id': picking_vals['location_dest_id'],
            }
            picking_vals['move_ids_without_package'].append((0, 0, move_line_vals))

        picking = self.env['stock.picking'].create(picking_vals)
        picking.button_validate()
        self.write({'state': 'closed'})

    def cancel_button(self):
        self.state = 'cancel'
        template_values = {
            'name': 'Mail Regarding to Cancellation of Shoot Request',
            'subject': 'Mail regarding cancellation of shoot request',
            'body_html': """
                                        <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                            <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                <strong>Cancellation of shoot Request</strong>
                                            </p>
                                            <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                <b>Dear %s,</b>
                                            </p>
                                            <br/>
                                            <br/>
                                            <p>
                                                Camera unit request has been cancelled,Please Contact Concerned assignment team for further enquiries
                                            </p>
                                            <br/>
                                            <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                Thank You
                                            </p>
                                        </div>
                                    """ % (
             self.employee_id.name),
            'model_id': self.env.ref('hr.model_hr_employee').id,
            # Replace 'hr' and 'model_hr_employee' with your actual module and model names
        }
        email_template = self.env['mail.template'].create(template_values)
        mail_template = self.env['mail.template'].browse(email_template.id)

        # Render the email content
        rendered_message = mail_template.body_html

        mail = self.env['mail.mail'].sudo().create({
            'subject': mail_template.subject,
            'body_html': rendered_message,
            'email_from': self.env.user.email,  # Use the actual sender email
            'email_to': self.employee_id.work_email,
        })
        mail.send()


class HrEmployeeInherited(models.Model):
    _inherit = 'hr.employee'

    def smart_shoot_request(self):
        self.ensure_one()
        all_child = self.with_context(active_test=False).search([('id', 'in', self.ids)])

        action = self.env["ir.actions.act_window"]._for_xml_id("infi_news_shoot_request.shoot_request_action")
        action['domain'] = [
            ('employee_id', 'in', all_child.ids)
        ]
        action['context'] = {'search_default_employee_id': self.id}
        return action


    def action_shoot_request(self):
        request_record = self.env['shoot.request'].create({
            'employee_id': self.id,
        })

        view_id = self.env.ref('infi_news_shoot_request.shoot_request_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Shoot Request Form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'shoot.request',
            'target': 'current',
            'res_id': request_record.id,
            'context': {
                 'default_employee_id': self.id,
            }
        }


class KitLine(models.Model):
    _name = 'kit.line'

    component_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    request_id = fields.Many2one('shoot.request', string='Shoot Request')



class ResCompany(models.Model):
    _inherit = 'res.company'

    picking_type = fields.Many2one('stock.picking.type', string='Operation Type')




