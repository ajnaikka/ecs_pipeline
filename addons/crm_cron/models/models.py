from odoo import _, api, fields, models,exceptions
from collections import defaultdict


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    check_duplicate = fields.Boolean(store='True',string="Check for Duplicate")
    fresh_lead = fields.Boolean(store='True',readonly=False, string="Is New Stage")




    @api.onchange('fresh_lead')
    def _check_new_stage(self):
        for val in self:
            check_new=0
            stage_data = self.env['crm.stage'].search([])
            if(stage_data):
                for data in stage_data:
                    if (data.fresh_lead):
                        data.fresh_lead=0;


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = ['crm.lead2opportunity.partner']


    def _combine_each_user_lead(self,user_records,total_leads_count=0):
        _total_leads_tobe_assigned=0
        for record in user_records:
            _stage_won = self.env['crm.stage'].search([('is_won', '=', True)])

            _user_Leads_count = self.env['crm.lead'].search_count([('user_id', '=', record.id),('type', '=', 'opportunity'),('stage_id', '!=', _stage_won.id)])
            if total_leads_count != 0:
                _lead_per = ((_user_Leads_count) / (total_leads_count)) * 100
            else:
                _lead_per =0

            _lead_tobe_assigned_per = 100 - _lead_per
            _total_leads_tobe_assigned = _total_leads_tobe_assigned + _lead_tobe_assigned_per




        return _total_leads_tobe_assigned

    def _Lead_Seperation(self):
        _lead_all_with_dup = self.env['crm.lead'].search([('type', '=', 'lead')], order='id asc')
        _stage_won = self.env['crm.stage'].search([('is_won', '=', True)])
        if _lead_all_with_dup:
            for _lead_rec in _lead_all_with_dup:
                email_from = _lead_rec.email_from
                phone = _lead_rec.phone

                if email_from and phone:

                    last_ten_phone = phone[-10:]

                    check_stage_ids = self.env['crm.lead'].search(
                        [('stage_id.check_duplicate', '=', True), ('type', '=', 'opportunity'),
                         ('stage_id', '!=', _stage_won.id),
                         ('email_from', '=', email_from),
                         ('phone', 'like', last_ten_phone)])
                    if check_stage_ids:
                        for _check_stage_ids_rec in check_stage_ids:
                            _lead_rec.write({
                                'lead_status': 'Duplication',
                                'user_id': _check_stage_ids_rec.user_id.id,
                            })
                            if _check_stage_ids_rec.user_id:
                                # Send Notification
                                notification_ids = []
                                notification_ids.append((0, 0, {
                                    'res_partner_id': _check_stage_ids_rec.user_id.partner_id.id,
                                    'notification_status': 'exception'}))

                                _check_stage_ids_rec.message_post(
                                    body="You received duplicate lead notification",
                                    subject=_('Duplicate Lead'),
                                    message_type='comment',
                                    author_id=_check_stage_ids_rec.user_id.partner_id.id,
                                    partner_ids=_check_stage_ids_rec.user_id.partner_id.ids,
                                    subtype_id=self.env.ref('mail.mt_comment').id,
                                    notification_ids=notification_ids,
                                )

                    else:
                        _lead_rec.write({
                            'lead_status': 'Fresh',
                        })




                elif email_from:
                    check_stage_ids = self.env['crm.lead'].search(
                        [('stage_id.check_duplicate', '=', True), ('type', '=', 'opportunity'),
                         ('stage_id', '!=', _stage_won.id),
                         ('email_from', '=', email_from)])
                    if check_stage_ids:
                        for _check_stage_ids_rec in check_stage_ids:
                            _lead_rec.write({
                                'lead_status': 'Duplication',
                                'user_id': _check_stage_ids_rec.user_id.id,
                            })
                            if _check_stage_ids_rec.user_id:
                                # Send Notification
                                notification_ids = []
                                notification_ids.append((0, 0, {
                                    'res_partner_id': _check_stage_ids_rec.user_id.partner_id.id,
                                    'notification_status': 'exception'}))

                                _check_stage_ids_rec.message_post(
                                    body="You received duplicate lead notification",
                                    subject=_('Duplicate Lead'),
                                    message_type='comment',
                                    author_id=_check_stage_ids_rec.user_id.partner_id.id,
                                    partner_ids=_check_stage_ids_rec.user_id.partner_id.ids,
                                    subtype_id=self.env.ref('mail.mt_comment').id,
                                    notification_ids=notification_ids,
                                )

                    else:
                        _lead_rec.write({
                            'lead_status': 'Fresh',
                        })

                elif phone:
                    last_ten_phone = phone[-10:]
                    check_stage_ids = self.env['crm.lead'].search(
                        [('stage_id.check_duplicate', '=', True), ('type', '=', 'opportunity'),
                         ('stage_id', '!=', _stage_won.id),
                         ('phone', 'like', last_ten_phone)])
                    if check_stage_ids:
                        for _check_stage_ids_rec in check_stage_ids:
                            _lead_rec.write({
                                'lead_status': 'Duplication',
                                'user_id': check_stage_ids.user_id.id,
                            })
                            if check_stage_ids.user_id:
                                # Send Notification
                                notification_ids = []
                                notification_ids.append((0, 0, {
                                    'res_partner_id': check_stage_ids.user_id.partner_id.id,
                                    'notification_status': 'exception'}))

                                check_stage_ids.message_post(
                                    body="You received duplicate lead notification",
                                    subject=_('Duplicate Lead'),
                                    message_type='comment',
                                    author_id=check_stage_ids.user_id.partner_id.id,
                                    partner_ids=check_stage_ids.user_id.partner_id.ids,
                                    subtype_id=self.env.ref('mail.mt_comment').id,
                                    notification_ids=notification_ids,
                                )

                    else:
                        _lead_rec.write({
                            'lead_status': 'Fresh',
                        })

                else:
                    _lead_rec.write({
                        'lead_status': 'Fresh',
                    })


    def _find_smallest_lead_user(self):
        _user_ids = self.env['res.users'].search([('active', '=', True), ('sale_team_id', '!=', False)], order='id asc')
        _lead_obj=self.env['crm.lead']
        domain = [
            ('user_id', 'in', _user_ids.ids)
        ]
        _find_rec = _lead_obj.read_group(
            domain=domain,
            fields=['id', 'user_id'],
            groupby=['user_id'],
            lazy=False,
        )

        if _find_rec:
            _ret_value = 0
            _user_id = 0

            _tuple_record=[]
            _tuple_user=[]

            data_credit = defaultdict(int)
            for i in _find_rec:
                k=0
                for key, value in i.items():
                    k=k+1
                    if k==1:
                        _tuple_record.append(value)
                    if k==2:
                        _tuple_user.append(value[0])



            _ret_value = 0
            _index=0
            i=0
            for tp in _tuple_record:
                if _ret_value != 0:
                    if tp < _ret_value:
                        _ret_value=tp
                        _index=_tuple_record.index(tp)
                        i=i+1
                    else:
                        _ret_value=_ret_value
                        _index = _tuple_record.index(_ret_value)
                        i = i + 1
                else:
                    _ret_value = tp
                    _index=_tuple_record.index(tp)
                    i = i + 1

        _ret_user_id=_tuple_user[_index]
        return _ret_user_id


    def _cron_auto_lead_filtering(self):
        check_stage_ids = 0
        fresh_stage_ids = self.env['crm.stage'].search(
            [('fresh_lead', '=', True)])



        self._Lead_Seperation()

        _stage_won = self.env['crm.stage'].search([('is_won', '=', True)])

        _total_leads_count = self.env['crm.lead'].search_count([('type', '=', 'opportunity'),('stage_id', '!=', _stage_won.id)])
        _new_leads_count = self.env['crm.lead'].search_count([('type', '=', 'lead'), ('lead_status', '=', 'Fresh')])

        if _new_leads_count!=0:
            user_records = self.env['res.users'].search([('active', '=', True), ('sale_team_id', '!=', False)],
                                                        order='id asc')
            if user_records:
                _total_leads_tobe_assigned = self._combine_each_user_lead(user_records, _total_leads_count)
                for record in user_records:
                    _user_Leads_count = self.env['crm.lead'].search_count(
                        [('user_id', '=', record.id), ('type', '=', 'opportunity')])
                    if _total_leads_count != 0:
                        _lead_per = ((_user_Leads_count) / (_total_leads_count)) * 100
                    else:
                        _lead_per = 0

                    _lead_tobe_assigned_per = 100 - _lead_per
                    _one_user_lead = (_lead_tobe_assigned_per / _total_leads_tobe_assigned) * _new_leads_count
                    _one_user_lead_temp = _one_user_lead
                    _user_id_for_assign = record.id
                    if _one_user_lead < 1:
                        _value = self._find_smallest_lead_user()
                        _user_id_for_assign = _value
                        _one_user_lead = _new_leads_count
                    else:
                        _user_id_for_assign = record.id

                    lead_all = self.env['crm.lead'].search([('type', '=', 'lead'), ('lead_status', '=', 'Fresh')],
                                                           limit=_one_user_lead,
                                                           order='id asc')
                    if lead_all:
                        for lead in lead_all:
                            lead.write({
                                'stage_id': fresh_stage_ids.id,
                                'user_id': _user_id_for_assign
                            })
                            self.env['crm.lead2opportunity.partner'].create({
                                'name': 'convert',
                                'user_id': _user_id_for_assign,
                                'team_id': lead.team_id.id,
                                'lead_id': lead.id,
                                'action': 'nothing',
                                'partner_id': lead.user_id.partner_id.id,
                                'duplicated_lead_ids': [[6, False, [lead.id]]],
                            })
                            self._convert_opportunity_demo(lead)

                    if _one_user_lead_temp < 1:
                        return


    def _convert_opportunity_demo(self,lead):
        customer = self.env['res.partner'].browse(lead.partner_id.id)
        vals = lead._convert_opportunity_data(customer, lead.team_id.id)
        lead.write(vals)



class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lead_status = fields.Char(store='True', string="Lead Status")



















