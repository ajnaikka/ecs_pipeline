odoo.define('infi_portal_attendance_correction.attendance_form', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.attendanceForm = publicWidget.Widget.extend({
        selector: '#employee_list_attendance_form',

        events: {
            'click .btn-group .btn': '_onClickButton',
        },

        _onClickButton: function (ev) {
            var option = $(ev.currentTarget).data('option');
            // Perform actions based on the clicked option
            if (option === 'option1') {
                // Do something for option 1
            } else if (option === 'option2') {
                alert("Hello");
            } else if (option === 'option3') {
                // Do something for option 3
            }
        },
    });

    return publicWidget.registry.attendanceForm;
});
