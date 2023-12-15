/** @odoo-module */

//import { ExpenseDocumentUpload, ExpenseDocumentDropZone } from '../mixins/document_upload';

import { registry } from '@web/core/registry';
import { patch } from '@web/core/utils/patch';
import { useService } from '@web/core/utils/hooks';
import { listView } from "@web/views/list/list_view";

import { ListController } from "@web/views/list/list_controller";
import { ListRenderer } from "@web/views/list/list_renderer";

const { onWillStart } = owl;

export class LeadListController extends ListController {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.actionService = useService('action');
        this.rpc = useService("rpc");
        this.user = useService("user");

        onWillStart(async () => {
            this.isSalesManager = await this.user.hasGroup("sales_team.group_sale_manager");
        });
    }
    async checkDuplicateLeadClick() {
        const records = this.model.root.selection;
        const recordIds = records.map((a) => a.resId);
        const action = await this.orm.call('crm.lead', 'check_lead_duplication', [recordIds]);
        this.actionService.doAction(action);
    }

}
//patch(LeadListController.prototype, 'expense_list_controller_upload', ExpenseDocumentUpload);


registry.category('views').add('crm_duplicate_check_tree', {
    ...listView,
    buttonTemplate: 'lead_duplicate_checking.ListButtons',
    Controller: LeadListController,
});