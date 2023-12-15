odoo.define('website_slides_subject.fullscreen', function (require) {
"use strict";

var core = require('web.core');
var QWeb = core.qweb;
var Fullscreen = require('@website_slides/js/slides_course_fullscreen_player')[Symbol.for("default")];
const {Markup} = require('web.utils');

Fullscreen.include({
    /**
     * Extend the _renderSlide method so that slides of category "subject"
     * are also taken into account and rendered correctly
     *
     * @private
     * @override
     */
    _renderSlide: function (){
        var def = this._super.apply(this, arguments);
        var $content = this.$('.o_wslides_fs_content');
        if (this.get('slide').category === "subject"){
            $content.html(QWeb.render('website.slides.fullscreen.flip_book',{widget: this}));
        }
        return Promise.all([def]);
    },

    _preprocessSlideData: function (slidesDataList) {
        slidesDataList.forEach(function (slideData, index) {
            // compute hasNext slide
            slideData.hasNext = index < slidesDataList.length-1;
            // compute embed url
            if (slideData.category === 'video' && slideData.videoSourceType !== 'vimeo') {
                slideData.embedCode = $(slideData.embedCode).attr('src') || ""; // embedCode contains an iframe tag, where src attribute is the url (youtube or embed document from odoo)
                var separator = slideData.embedCode.indexOf("?") !== -1 ? "&" : "?";
                var scheme = slideData.embedCode.indexOf('//') === 0 ? 'https:' : '';
                var params = { rel: 0, enablejsapi: 1, origin: window.location.origin };
                if (slideData.embedCode.indexOf("//drive.google.com") === -1) {
                    params.autoplay = 1;
                }
                slideData.embedUrl = slideData.embedCode ? scheme + slideData.embedCode + separator + $.param(params) : "";
            } else if (slideData.category === 'video' && slideData.videoSourceType === 'vimeo') {
                slideData.embedCode = Markup(slideData.embedCode);
            } else if (slideData.category === 'infographic') {
                slideData.embedUrl = _.str.sprintf('/web/image/slide.slide/%s/image_1024', slideData.id);
            } else if (slideData.category === 'document') {
                slideData.embedUrl = $(slideData.embedCode).attr('src');
            } else if (slideData.category === 'subject') {
//                const data = await this._rpc({
//                      model: 'slide.slide',
//                      method: 'browse',
//                      args: [slideData.id],
//                      kwargs: { },
//                });
//                slideData.embedUrl = $('<iframe src="https://heyzine.com/flip-book/ea25138512.html" width="100%" height="480" seamless="seamless" scrolling="no" frameborder="0" allowfullscreen="true"></iframe>').attr('src');
//                slideData.embedUrl = $(slideData.embedCode).attr('src');
            }
            // fill empty property to allow searching on it with _.filter(list, matcher)
            slideData.isQuiz = !!slideData.isQuiz;
            slideData.hasQuestion = !!slideData.hasQuestion;
            // technical settings for the Fullscreen to work
            var autoSetDone = false;
            if (!slideData.hasQuestion) {
                if (_.contains(['infographic', 'document', 'article', 'subject'], slideData.category)) {
                    autoSetDone = true;  // images, documents (local + external) and articles are marked as completed when opened
                } else if (slideData.category === 'video' && slideData.videoSourceType === 'google_drive') {
                    autoSetDone = true;  // google drive videos do not benefit from the YouTube integration and are marked as completed when opened
                }
            }
            slideData._autoSetDone = autoSetDone;
        });
        return slidesDataList;
    },
});
});
