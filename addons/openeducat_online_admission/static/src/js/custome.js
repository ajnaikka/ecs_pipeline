odoo.define('openeducat_online_admission.student_registration', function (require) {
    "use strict";
    var core = require('web.core');
    var Dialog = require("web.Dialog");
    var session = require('web.session');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var websiteRootData = require('website.root');
    var utils = require('web.utils');
    var field_utils = require('web.field_utils');
    var _t = core._t;
    var qweb = core.qweb;
    const time = require('web.time');

    var StudentRegister = Widget.extend({
        events:{'change #self_application': '_onchangedropdown',
                'change .admission_form_date': '_onchangebirthdate'},

        xmlDependencies: ['/openeducat_online_admission/static/src/xml/custome.xml'],
        init: function(){
            this._super.apply(this,arguments);
        },
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then( function(){
                $("#birthdate").attr('placeholder', time.getLangDateFormat());
                $( "#birthdate" ).datepicker('destroy');
                $( ".admission_form_date" ).each( function(){
                    self._initDateTimePicker($(this));
                });
            });

        },
        _formatDate: function(){
            var dateFormat = time.getLangDateFormat();
            var formatArr = ['Y','M','D'];
            for(var idx in formatArr){
                var chr =  formatArr[idx];
                var count = [...dateFormat].filter(x => x === chr).length;
                if(count > 2){
                    dateFormat = dateFormat.replace( `${chr.repeat(count)}`, `${chr.repeat(2)}` );
                }
            }
            dateFormat = dateFormat.toLowerCase()
            return dateFormat;
        },

        _initDateTimePicker: function ($dateGroup) {
            var self = this;
            var datetimepickerFormat = time.getLangDateFormat();
            $dateGroup.datetimepicker({
                format : datetimepickerFormat,
                minDate: 0,
                useCurrent: false,
                maxDate: moment(new Date()),
                viewDate: false,
                icons: {
                    time: 'fa fa-clock-o',
                    date: 'fa fa-calendar',
                    next: 'fa fa-chevron-right',
                    previous: 'fa fa-chevron-left',
                    up: 'fa fa-chevron-up',
                    down: 'fa fa-chevron-down',
                },
                locale : moment.locale(),
                allowInputToggle: true,
            });
            $dateGroup.on('change.datetimepicker', function(ev){
                self._onchangebirthdate(ev);
            })
        },

        _onchangedropdown: function(ev){
            var application = $(ev.currentTarget).val();
            ajax.jsonRpc('/get/application_data', 'call',
                {
                'application': application,
                }).then(function (data) {
                if (data['student_id'])
                {
                var student_data = qweb.render('GetStudentData',
                {
                    students: data['student_id'][0],
                    country: data['country_id']
                });
                $('.students').html(student_data);
                $('.country').html(student_data);
                }
                else if (data['country'])
                {
                  var others_data = qweb.render('GetOthersData',
                {
                    others: data['country'],
                });
                $('.others').html(others_data);
                }

            });
        },

        _onchangebirthdate: function(ev){
            var birth_date = $("input[name='birth_date']").val();
            var register_id = $("select[name='register_id']").val();
            var momentDate = field_utils.parse.date(birth_date);
            var formattedDate = momentDate ? momentDate.toJSON() : '';
            if(register_id){
                ajax.jsonRpc('/check/birthdate', 'call',
                    {
                    'birthdate': formattedDate,
                    'register': register_id,
                    }).then(function (data) {
                    if (data['birthdate'])
                    {
                      alert('Not Eligible for Admission minimum required age is :'+ data['age']);
                      var birth_date = $("input[name='birth_date']").val('');
                    }
                    });
            }
            else{
                alert('Please Select a Course');
                var birth_date = $("input[name='birth_date']").val('');
            }
        }
    });

    websiteRootData.websiteRootRegistry.add(StudentRegister, '.js_get_data');

    return StudentRegister;
}); 
