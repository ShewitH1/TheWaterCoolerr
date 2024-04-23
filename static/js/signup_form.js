document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("profileType").addEventListener('change', function() {
        var selectedValue = this.value;
        var formRender = document.getElementById("signupInfo");
        var submitButton = document.getElementById("submitButton");
    
        if (selectedValue === "user")
        {
            formRender.innerHTML = 
            `<div class="mt-2 mb-2">
            <label for="profileID">Create a unique profile id (16 char limit):</label>
            <input type="text" class="form-control" id="profileID" name="profileID" required>
            </div>
            <div class="mt-2 mb-2">
            <label for="email">Account email:</label>
            <input type="email" class="form-control" id="email" name="email" required>
            </div>
            <div class="mt-2 mb-2">
            <label for="passwordArea">Create a unique password:</label>
            <input type="password" class="form-control" id="passwordArea" name="password" required>
            </div>
            <div class="mt-2 mb-2">
            <label for="firstname">Enter your firstname:</label>
            <input type="text" class="form-control" id="firstname" name="firstname" required>
            </div>
            <div class="mt-2 mb-2">
            <label for="lastname">Enter your lastname:</label>
            <input type="text" class="form-control" id="lastname" name="lastname" required>
            </div>`;
            submitButton.style.display="block";
        } else if (selectedValue === "company") {
            formRender.innerHTML = 
            `<div class="mt-2 mb-2">
            <label for="companyID">Create a unique company id (16 char limit):</label>
            <input type="text" class="form-control" id="companyID" name="companyID" required>
            </div>
            <div class="mt-2 mb-2">
            <label for="companyLogin">Create a username or email to manage your business:</label>
            <input type="text" class="form-control" id="companyLogin" name="companyLogin" required>
            </div>
            <div class="mt-2 mb-2">
            <label for="passwordArea">Create a unique password:</label>
            <input type="password" class="form-control" id="passwordArea" name="password" required>
            </div>
            <div class="mt-2 mb-2">
            <label for="companyName">Enter your firstname:</label>
            <input type="text" class="form-control" id="companyName" name="companyName" required>
            </div>`;
            submitButton.style.display="block";
        } else {
            formRender.innerHTML = '';
            submitButton.style.display="none";
        }
    });
});

function signup(event) {
    event.preventDefault();
    var selectedValue;
    if (document.getElementById('profileType'))
        selectedValue = document.getElementById("profileType").value;
    var formRender = document.getElementById("signupInfo");

    console.log(selectedValue);
    var formData = new FormData();
    console.log('calling');
    if (selectedValue === 'user') {
            formData.append('payload_tag', 'basic');
            formData.append('profile_type', selectedValue);
            formData.append('profile_id', document.getElementById('profileID').value);
            formData.append('email', document.getElementById('email').value);
            formData.append('pass', document.getElementById('passwordArea').value)
            formData.append('firstname', document.getElementById('firstname').value);
            formData.append('lastname', document.getElementById('lastname').value);
    } else if (selectedValue === 'company') {
        formData.append('payload_tag', 'basic');
        formData.append('profile_type', selectedValue);
        formData.append('company_id', document.getElementById('companyID').value);
        formData.append('login', document.getElementById('companyLogin').value);
        formData.append('pass', document.getElementById('passwordArea').value);
        formData.append('company_name', document.getElementById('companyName').value);
    } else {
        var id = $('#extrasData').data('extras-id');
        var profileType = $('#extrasData').data('extras-profiletype');
        formData.append('payload_tag', 'extra');
        formData.append('id', id);
        formData.append('profileType', profileType);
        formData.append('profile_bio','');
        if (document.getElementById('profileBio')) {
            var bio = document.getElementById('profileBio');
            if (bio.value != "") {
                formData.set('profile_bio', bio.value)
            }
        }
        if (document.getElementById('profileUpload')) {
            var profile = document.getElementById('profileUpload');
            console.log(profile.files);
            if (profile.files.length > 0) {
                console.log('profile');
                formData.append('profile_picture', profile.files[0]);
            }
        }
        if (document.getElementById('bannerUpload')) {
            var banner = document.getElementById('bannerUpload');
            console.log(banner.files);
            if (banner.files.length > 0) {
                console.log('banner');
                formData.append('profile_banner', banner.files[0]);
            }
        }
    }

    console.log(formData);

    fetch('/signup', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok)
        {
            throw new Error("Response Error!");
        }
        return response.json();
    })
    .then(response => {
        if ('redirect' in response) {
            window.location.href = response.redirect;
        }
        const profileTypeContainer = document.getElementById('profileTypeContainer');
        profileTypeContainer.innerHTML = '';
        formRender.innerHTML='';
        const extrasContainer = document.getElementById('signupExtras');
        let id;
        let profileType;
        console.log(response);
        if ('user_id' in response) {
            id = response.user_id;
            profileType = 'user';
        } else if ('company_id' in response) {
            id = response.company_id;
            profileType = 'company';
        }
        extrasContainer.innerHTML =
        `<div id="extrasData" data-extras-id=${id} data-extras-profileType=${profileType}></div>
        <div class="mt-2 mb-2">
            <label for="profileBio">Enter a profile bio (Optional)</label>
            <textarea class="form-control" id="profileBio" name="newBio" rows="1"></textarea>
        </div>
        <div class="mt-2 mb-2">
            <label for="profileUpload">Upload profile picture, best fit will be 1:1 aspect ratio (square) (Optional)</label>
        </div>
        <div class="mt-2 mb-2">
            <input type="file" class="form-control-file" id="profileUpload" name="newProfile" accept="image/*">
        </div>
        <div class="mt-2 mb-2">
            <label for="bannerUpload">Upload profile banner, best fit will be 3:1 aspect ratio (Optional)</label>
        </div>
        <div class="mt-2 mb-2">
            <input type="file" class="form-control-file" id="bannerUpload" name="newBanner" accept="image/*">
        </div>`;
    })
    .catch(error => {
        console.error('Error tracking analytics event:', error);
    });
    // $.ajax({
    //     type: 'POST',
    //     url: '/signup',
    //     data: formData,
    //     contentType: false,
    //     cache: false,
    //     processData: false,
    //     success: function(response) {
    //         if ('redirect' in response)
    //         {
    //             window.location.href = response.redirect;
    //         }
    //         var profileTypeContainer = document.getElementById('profileTypeContainer');
    //         profileTypeContainer.innerHTML='';
    //         formRender.innerHTML='';
    //         var extrasContainer = document.getElementById('signupExtras');
    //         var id;
    //         var profileType;
    //         console.log(response)
    //         if ('user_id' in response)
    //         {
    //             id = response['user_id'];
    //             profileType = 'user';
    //         } else if ('company_id' in response)
    //         {
    //             id = response['company_id'];
    //             profileType = 'company'
    //         }
    //         extrasContainer.innerHTML =
    //         `<div id="extrasData" data-extras-id=${id} data-extras-profileType=${profileType}></div>
    //         <div class="mt-2 mb-2">
    //             <label for="profileBio">Enter a profile bio (Optional)</label>
    //             <textarea class="form-control" id="profileBio" name="newBio" rows="1"></textarea>
    //         </div>
    //         <div class="mt-2 mb-2">
    //             <label for="profileUpload">Upload profile picture, best fit will be 1:1 aspect ratio (square) (Optional)</label>
    //         </div>
    //         <div class="mt-2 mb-2">
    //             <input type="file" class="form-control-file" id="profileUpload" name="newProfile" accept="image/*">
    //         </div>
    //         <div class="mt-2 mb-2">
    //             <label for="bannerUpload">Upload profile banner, best fit will be 3:1 aspect ratio (Optional)</label>
    //         </div>
    //         <div class="mt-2 mb-2">
    //             <input type="file" class="form-control-file" id="bannerUpload" name="newBanner" accept="image/*">
    //         </div>`;
    //     },
    //     error: function(error) {
    //         console.error('Error tracking analytics event:', error);
    //     }
    // });
}