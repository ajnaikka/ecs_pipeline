odoo.define('website_subsection_control.upload_modal', function (require) {
"use strict";

var core = require('web.core');
var _t = core._t;
var SlidesUpload = require('@website_slides/js/slides_upload')[Symbol.for("default")];

/**
 * Management of the new 'subsection' slide_category
 */
SlidesUpload.SlideUploadDialog.include({
    events: _.extend({}, SlidesUpload.SlideUploadDialog.prototype.events || {}, {
        'change input#subsection_id': '_onChangeSubsection'
    }),

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

   /**
    * Will automatically set the title of the slide to the title of the chosen subsection
    */
//    _onChangeCertification: function (ev) {
    _onChangeSubsection: function (ev) {
        const $inputElement = this.$("input#name");
        if (ev.added) {
            this.$('.o_error_no_subsection').addClass('d-none');
            this.$('#subsection_id').parent().find('.select2-container').removeClass('is-invalid');
            if (ev.added.text && !$inputElement.val().trim()) {
                $inputElement.val(ev.added.text);
            }
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Overridden to add the "subsection" slide category
     *
     * @override
     * @private
     */
    _setup: function () {
        this._super.apply(this, arguments);
        this.slide_category_data['subsection'] = {
            icon: 'fa fa-angle-double-right',
            label: _t('Subsection'),
            template: 'website.slide.upload.modal.subsection',
        };
    },
    /**
     * Overridden to add subsections management in select2
     *
     * @override
     * @private
     */
    _bindSelect2Dropdown: function () {
        this._super.apply(this, arguments);

        var self = this;
        this.$('#subsection_id').select2(this._select2Wrapper(_t('Subsection'), false,
            function () {
                return self._rpc({
                    route: '/slides_survey/subsection/search_read',
                    params: {
                        fields: ['title'],
                    }
                });
            }, 'title')
        );
    },
    /**
     * The select2 field makes the "required" input hidden on the interface.
     * We need to make the "subsection" field required so we override this method
     * to handle validation in a fully custom way.
     *
     * @override
     * @private
     */
    _formValidate: function () {
        var result = this._super.apply(this, arguments);

        var $subsectionInput = this.$('#subsection_id');
        if ($subsectionInput.length !== 0) {
            var $select2Container = $subsectionInput
                .parent()
                .find('.select2-container');
            var $errorContainer = $('.o_error_no_subsection');
            $select2Container.removeClass('is-invalid is-valid');
            if ($subsectionInput.is(':invalid')) {
                $select2Container.addClass('is-invalid');
                $errorContainer.removeClass('d-none');
            } else if ($subsectionInput.is(':valid')) {
                $select2Container.addClass('is-valid');
                $errorContainer.addClass('d-none');
            }
        }

        return result;
    },
    /**
     * Overridden to add the 'subsection' field into the submitted values
     *
     * @override
     * @private
     */
    _getSelect2DropdownValues: function () {
        var result = this._super.apply(this, arguments);

        var certificateValue = this.$('#subsection_id').select2('data');
        var survey = {};
        if (certificateValue) {
            if (certificateValue.create) {
                survey.id = false;
                survey.title = certificateValue.text;
            } else {
                survey.id = certificateValue.id;
            }
        }
        result['survey'] = survey;
        return result;
    },
});

});
