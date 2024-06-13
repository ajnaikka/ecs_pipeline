/** @odoo-module */

import { ActivityMenu } from "@hr_attendance/components/attendance_menu/attendance_menu";
import { patch } from "@web/core/utils/patch";

patch(ActivityMenu.prototype, {
        async captureImage1() {

            var video = document.getElementById('cameraFeed');
                    var canvas = document.createElement('canvas');
                    var context = canvas.getContext('2d');

                    // Request access to the camera
                    navigator.mediaDevices.getUserMedia({ video: true })
                        .then(function (stream) {
                            video.srcObject = stream;
                            video.play();
                            video.style.display = 'block'; // Display the video element

                            // Capture image when "Take Snap" button is clicked
                            document.querySelector('.modal-footer button').addEventListener('click', function () {
                                canvas.width = video.videoWidth;
                                canvas.height = video.videoHeight;
                                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                                var imageData = canvas.toDataURL('image/jpeg');
                                console.log("capturedImagePreview",imageData);
                                // Display captured image
                                var preview = document.getElementById('capturedImagePreview');
                                preview.src = imageData;
                                preview.style.display = 'block';

                                var formData = new FormData();
                                formData.append('image_data', imageData);
                                formData.append('csrf_token', odoo.csrf_token);
                                $.ajax({
                                    url: '/hr_attendance/upload_imageds',
                                    type: 'POST',
                                    data: formData,

                                    processData: false,
                                    contentType: false,
                                    success: function(response) {
                                        console.log('Image uploaded successfully.');

                                    },
                                    error: function(xhr, status, error) {
                                        console.error('Failed to upload image:', error);
                                    }
                                });

                                // Stop video stream
                                stream.getTracks().forEach(track => track.stop());
                            });
                        })
                        .catch(function (err) {
                            console.error('Error accessing camera:', err);
                        });
    },
    async captureImageout() {

                    var video = document.getElementById('checkoutCameraFeed');
                        var canvas = document.createElement('canvas');
                        var context = canvas.getContext('2d');

                        // Request access to the camera
                        navigator.mediaDevices.getUserMedia({ video: true })
                            .then(function (stream) {
                                video.srcObject = stream;
                                video.play();
                                video.style.display = 'block'; // Display the video element
                                console.log("it is working here");

                                // Capture image when "Take Snap" button is clicked
                                document.querySelector('#checkoutmodeltoggle .modal-footer button').addEventListener('click', function () {
                                    console.log("it enters in ");

                                    canvas.width = video.videoWidth;
                                    canvas.height = video.videoHeight;
                                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                                    var imageDataout = canvas.toDataURL('image/jpeg');
                                    console.log("checkoutCapturedImagePreview", imageDataout);

                                    // Display captured image
                                    var preview = document.getElementById('checkoutCapturedImagePreview');
                                    preview.src = imageDataout;
                                    preview.style.display = 'block';  // Ensure the image is displayed

                                    var formData = new FormData();
                                    formData.append('image_out', imageDataout);
                                    formData.append('csrf_token', odoo.csrf_token);
                                    $.ajax({
                                        url: '/hr_attendance/upload_image',
                                        type: 'POST',
                                        data: formData,
                                        processData: false,
                                        contentType: false,
                                        success: function(response) {
                                            console.log('Image uploaded successfully for check-out.');
                                        },
                                        error: function(xhr, status, error) {
                                            console.error('Failed to upload image for check-out:', error);
                                        }
                                    });

                                    // Stop video stream
                                    stream.getTracks().forEach(track => track.stop());
                                });
                            })
                            .catch(function (err) {
                                console.error('Error accessing camera for check-out:', err);
                            });
    },





});




























































//
//
///** @odoo-module */
//
//import { ActivityMenu } from "@mail/core/web/activity_menu";
//import { patch } from "@web/core/utils/patch";
//import { Component, App, xml } from "@odoo/owl";
//
//patch(ActivityMenu.prototype, {
//    async captureImage() {
//        var video = document.createElement('video');
//        var canvas = document.createElement('canvas');
//        var context = canvas.getContext('2d');
//
//        try {
//            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//            video.srcObject = stream;
//            video.play();
//        } catch (err) {
//            console.error('Error accessing camera:', err);
//        }
//
//        video.addEventListener('loadedmetadata', () => {
//            canvas.width = video.videoWidth;
//            canvas.height = video.videoHeight;
//            context.drawImage(video, 0, 0, canvas.width, canvas.height);
//            var imageData = canvas.toDataURL('image/jpeg');
//
//            var preview = document.getElementById('capturedImagePreview');
//            preview.src = imageData;
//            preview.style.display = 'block';
//            console.log("Image captured", imageData);
//
//            var formData = new FormData();
//            formData.append('image_data', imageData);
//            formData.append('csrf_token', odoo.csrf_token);
//            $.ajax({
//                url: '/hr_attendance/upload_image',
//                type: 'POST',
//                data: formData,
//
//                processData: false,
//                contentType: false,
//                success: function(response) {
//                    console.log('Image uploaded successfully.');
//
//                },
//                error: function(xhr, status, error) {
//                    console.error('Failed to upload image:', error);
//                }
//            });
//
//            // Stop video stream
//            video.srcObject.getVideoTracks().forEach(track => track.stop());
//        });
//    },
//});
