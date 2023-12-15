odoo.define('openeducat_online_admission.tour', function (require) {
'use strict';

var tour = require("web_tour.tour");

tour.register('admission_registration_test', {
    test: true,
    url: '/student/registration/info/1',
},
    [
        {
            content: "select Sumita S Dani",
            extra_trigger: "#registration_name",
            trigger: "span:contains(Sumita S Dani)",
        },

    ]
);

});
