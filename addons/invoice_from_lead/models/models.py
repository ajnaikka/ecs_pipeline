from odoo import models, fields, api


class crmLead(models.Model):
    _inherit = "crm.lead"

    invoice_line_ids = fields.One2many('account.move', 'lead_id', string='Invoice Line')

    invoice_count = fields.Integer(compute='_get_invoiced', string='Invoice Count', copy=False, default=0)
    invoice_ids = fields.Many2many('account.move',  string='Bills', copy=False, store=True)


    def _get_invoiced(self):
        print('inside _get_invoiced')
        for lead in self:
            invoices = lead.invoice_line_ids.filtered(
                lambda r: r.move_type in ('out_invoice', 'out_refund'))
            # lead.invoice_ids = invoices
            lead.invoice_count = len(invoices)


    def action_create_invoice(self):
        if self.application_for_admission:
            invoice = self.env['account.move'].create({
                # 'name': self.name,
                'move_type': 'out_invoice',
                'partner_id': self.partner_id.id,
                'lead_id': self.id,
                'invoice_line_ids': [(0, 0, {
                    'name': self.application_for_admission.name,
                    'product_id':self.application_for_admission.product_id.id,
                    'price_unit':self.application_for_admission.list_price,
                    'quantity': 1.0,
                    'discount': 0.0,
                })],
            })
            return self.action_view_invoice(invoice)



    def action_view_invoice(self, invoices=False):
        if not invoices:
            self.sudo()._read(['invoice_ids'])
            invoices = self.invoice_ids

        result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
        # choose the view_mode accordingly
        if len(invoices) > 1:
            result['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = invoices.id
        else:
            result = {'type': 'ir.actions.act_window_close'}

        return result

    # def action_crm_view_invoice(self):
    #     for i in self:
    #         return







