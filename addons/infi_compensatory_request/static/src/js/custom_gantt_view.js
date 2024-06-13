odoo.define('infi_compensatory_request.custom_gantt_view', ['web.core', 'web_gantt.GanttView', 'web_gantt.GanttRenderer'], function (require) {
    "use strict";

    var GanttView = require('web_gantt.GanttView');
    var GanttRenderer = require('web_gantt.GanttRenderer');

    var CustomGanttRenderer = GanttRenderer.extend({
        _render: function () {
            this._super.apply(this, arguments);
            // Add custom logic to change the color of Gantt bars
            // based on the value of the shift_type field
            this.$('.o_gantt_row').each(function () {
                var shiftType = $(this).data('record').shift_id[1];
                if (shiftType === 'Morning') {
                    $(this).css('background-color', 'red');
                }
            });
        },
    });

    var CustomGanttView = GanttView.extend({
        config: _.extend({}, GanttView.prototype.config, {
            Renderer: CustomGanttRenderer,
        }),
    });

    core.view_registry.add('custom_gantt_view', CustomGanttView);

    return CustomGanttView;
});
