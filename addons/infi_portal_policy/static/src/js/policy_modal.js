$(document).ready(function() {
    // Check if the current URL contains "my"
    if (window.location.href.indexOf("my") !== -1) {

      var policy_state = $('#policy_state').data('state');
      if (!policy_state){
         // Show the modal
      $('#policyModal').modal('show');
      var inputString = $('#policy_data').data('policy');
      // Replace single quotes with double quotes to make it valid JSON
      if(inputString){
           var jsonString = inputString.replace(/'/g, '"');
      }else{
       var jsonString = false;
      }


    // Parse the JSON string into an array of dictionaries
    if (jsonString){
    var policies = JSON.parse(jsonString);
    }
    else{
    var policies = false;
    }
      if(policies){
    // Output the array of dictionaries to console
       var currentIndex = 0;
       function displayPolicy(index) {
            var policy = policies[index];
            $('#policyModalTitle').text(policy.name);
            $('#policyModalBody').html(policy.description);

            // Append checkbox and submit button if it's the last policy
            if (index === policies.length - 1) {
                $('#policyModalBody').append('<div> </div>');
                $('#policyModalBody').append('<label style="padding-top: 33px;"><input type="checkbox" id="agreeCheckbox"> I agree</label>');
                $('#policyModalBody').append('<button type="button" class="btn btn-primary" style="display:none;" id="submitBtn">Submit</button>');
            }
        }

        function updateNextButtonVisibility() {
            if (currentIndex >= policies.length - 1) {
                $('#nextBtn').hide();
            } else {
                $('#nextBtn').show();
            }
        }

        displayPolicy(currentIndex);
        updateNextButtonVisibility();

        $('#nextBtn').click(function() {
            currentIndex++;
            displayPolicy(currentIndex);
            updateNextButtonVisibility();
        });

        $('#prevBtn').click(function() {
            if (currentIndex > 0) {
                currentIndex--;
                displayPolicy(currentIndex);
                $('#nextBtn').show();
            }
        });
        $('#policyModalBody').on('change', '#agreeCheckbox', function() {
            if ($(this).prop('checked')) {
                $('#submitBtn').css('display', 'block');
                console.log("yesssssss")
            } else {
                $('#submitBtn').css('display', 'none');
            }
        });

        // Button click event for the submit button
        $('#policyModalBody').on('click', '#submitBtn', function() {
            if ($('#agreeCheckbox').prop('checked')) {
                // Checkbox is checked, do something (e.g., submit form)
                console.log('Checkbox is checked. Submitting...');
            } else {
                // Checkbox is not checked
                console.log('Checkbox is not checked.');
            }
        });
        // Button click event for the submit button
        $('#policyModalBody').on('click', '#submitBtn', function() {
            if ($('#agreeCheckbox').prop('checked')) {
                // Checkbox is checked, do something (e.g., submit form)
                var checked = "agree";
                $.ajax({
                    type: "POST",
                    url: "/my/policy",
                    data: {
                        policies: checked,
                    },
                    contentType: "application/json",
                    success: function(response) {
                        // Handle successful response from the backend
                        console.log("Data submitted successfully:", response);
                        $('#policyModal').modal('hide');
                        // Redirect to the specified URL
                        window.location.href = "/my/employees/about_me";
                    },
                    error: function(xhr, status, error) {
                        // Handle error response from the backend
                        console.error("Error submitting data:", error);
                    }
                });
            } else {
                // Checkbox is not checked
                var checked = "not";
            }
        });

        }
      }

    }



  });