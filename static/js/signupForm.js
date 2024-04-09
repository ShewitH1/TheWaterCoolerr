document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("profileType").addEventListener('change', function() {
        var selectedValue = this.value;
        var formRender = document.getElementById("signupInfo");
        var submitButton = document.getElementById("submitButton");
    
        if (selectedValue === "user")
        {
            formRender.innerHTML = 
            '<div class="mt-2 mb-2">' +
            '<label for="profileID">Create a unique profile id (16 char limit):</label>' +
            '<textarea class="form-control" id="profileID" name="profileID" rows="1" required></textarea>' +
            '</div>' +
            '<div class="mt-2 mb-2">' +
            '<label for="email">Account email:</label>' +
            '<textarea class="form-control" id="email" name="email" rows="1" required></textarea>' +
            '</div>' +
            '<div class="mt-2 mb-2">' +
            '<label for="passwordArea">Create a unique password:</label>' +
            '<textarea class="form-control" id="passwordArea" name="password" rows="1" required></textarea>' +
            '</div>' +
            '<div class="mt-2 mb-2">' +
            '<label for="firstname">Enter your firstname:</label>' +
            '<textarea class="form-control" id="firstname" name="firstname" rows="1" required></textarea>' +
            '</div>' +
            '<div class="mt-2 mb-2">' +
            '<label for="lastname">Enter your lastname:</label>' +
            '<textarea class="form-control" id="lastname" name="lastname" rows="1" required></textarea>' +
            '</div>';
            submitButton.style.display="block";
        } else if (selectedValue === "company") {
            formRender.innerHTML = 
            '<div class="mt-2 mb-2">' +
            '<label for="companyID">Create a unique company id (16 char limit):</label>' +
            '<textarea class="form-control" id="companyID" name="companyID" rows="1" required></textarea>' +
            '</div>' +
            '<div class="mt-2 mb-2">' +
            '<label for="companyLogin">Create a username or email to manage your business:</label>' +
            '<textarea class="form-control" id="companyLogin" name="companyLogin" rows="1" required></textarea>' +
            '</div>' +
            '<div class="mt-2 mb-2">' +
            '<label for="passwordArea">Create a unique password:</label>' +
            '<textarea class="form-control" id="passwordArea" name="password" rows="1" required></textarea>' +
            '</div>' +
            '<div class="mt-2 mb-2">' +
            '<label for="companyName">Enter your firstname:</label>' +
            '<textarea class="form-control" id="companyName" name="companyName" rows="1" required></textarea>' +
            '</div>'
            submitButton.style.display="block";
        } else {
            formRender.innerHTML = '';
            submitButton.style.display="none";
        }
    });
});