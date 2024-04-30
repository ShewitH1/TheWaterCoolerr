var editPageData = document.getElementById("profileDataDiv");

var profileType = editPageData.getAttribute("data-profile-type");

var profileID = editPageData.getAttribute("data-profile-id")


function updateWorkExperience(expUUID, title, cmpy_name, sector, descr, start, end, check, requestType) {
    if (requestType == "saveAll") {
        var job_title = title.value;
        if (job_title == "") {deleteWorkExperience(expUUID); return;}
        var company_name = cmpy_name.value;
        if (company_name == "") {deleteWorkExperience(expUUID); return;} 
        var job_sector = sector.value
        var start_date = start.value;
        var end_date = end.value;
        var description = descr.value;
        var waterCooler = check.checked;
    } 
    var job_title = title.value;
    var company_name = cmpy_name.value;
    var job_sector = sector.value
    var start_date = start.value;
    var end_date = end.value;
    var description = descr.value;
    var waterCooler = check.checked;

    var workExperienceData = {
        work_experience_id : expUUID,
        job_title : job_title,
        company_name : company_name,
        job_sector : job_sector,
        start_date : start_date,
        end_date : end_date,
        description : description,
        waterCooler : waterCooler
    };

    var experienceDataRequest = JSON.stringify(workExperienceData);
    fetch('/updateWorkExperience', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: experienceDataRequest
    })
    .then(response => {
        if (!response.ok)
        {
            throw new Error("Response Error in Work Experience Update");
        }
        return response.json();
    })
    .then(response => {
        var alertDiv = document.querySelector(`#workExpForm${expUUID} #alert-div`);
        console.log(response);
        if (response.response == 'success')
        {
            alertDiv.innerHTML=`
            <div class="alert alert-success" role="alert">
            Successfully Updated Work Experience!
            </div>`
        } else if (response.response == "failure-title") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, work experience needs a title
            </div>`
        } else if (response.response == "failure-name") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, work experience needs a company or workplace name
            </div>`
        } else if (response.response == "failure-start") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, work experience needs a valid start date
            </div>`
        } else if (response.response == "failure-date") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, work experience start date cannot be greater than current date
            </div>`
        } else if (response.response == "failure-greater-date") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, work experience start date cannot be greater than current date
            </div>`
        } else if (response.response == "failure-greater-date-end") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, work experience end date cannot be greater than current date
            </div>`
        }
        timeAlert(alertDiv)
    })
}

function updateEducationExperience(expUUID, inst, level, area, start, end, requestType) {
    if (requestType == "saveAll")
    {
        var institution_name = inst.value;
        if (institution_name == "") {deleteEducationExperience(expUUID); return;}
        var education_level = level.value;
        if (education_level == "") {deleteEducationExperience(expUUID); return;}
        var study_area = area.value;
        if (study_area == "") {deleteEducationExperience(expUUID); return;}
        var start_date = start.value;
        var end_date = end.value;
    }
    var institution_name = inst.value;
    var education_level = level.value;
    var study_area = area.value;
    var start_date = start.value;
    var end_date = end.value;

    var educationExperienceData = {
        education_experience_id : expUUID,
        institution_name : institution_name,
        education_level : education_level,
        study_area : study_area,
        start_date : start_date,
        end_date : end_date
    };

    var experienceDataRequest = JSON.stringify(educationExperienceData);
    fetch('/updateEducationExperience', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: experienceDataRequest
    })
    .then(response => {
        if (!response.ok)
        {
            throw new Error("Response Error in Education Experience Update");
        }
        return response.json();
    })
    .then(response => {
        var alertDiv = document.querySelector(`#eduExpForm${expUUID} #alert-div`);
        if (response.response == 'success')
        {
            alertDiv.innerHTML=`
            <div class="alert alert-success" role="alert">
            Successfully Updated Education Experience!
            </div>`
        } else if (response.response == "failure-inst") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, education experience needs an institution name
            </div>`
        } else if (response.response == "failure-level") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, education experience needs a level of education
            </div>`
        } else if (response.response == "failure-area") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, education experience needs an area of study
            </div>`
        } else if (response.response == "failure-start") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, education experience needs a valid start date
            </div>`
        } else if (response.response == "failure-date") {
                alertDiv.innerHTML=`
                <div class="alert alert-danger" role="alert">
                Failed to update, education experience start date cannot be greater than current date
                </div>`
        } else if (response.response == "failure-greater-date") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, education experience start date cannot be greater than current date
            </div>`
        } else if (response.response == "failure-greater-date-end") {
            alertDiv.innerHTML=`
            <div class="alert alert-danger" role="alert">
            Failed to update, education experience end date cannot be greater than current date
            </div>`
        }
        timeAlert(alertDiv)
    })
}

function timeAlert(alertDiv)
{
    var counter = 0;

    var intervalID = setInterval(function() {
        counter += 3;
        clearInterval(intervalID);
        alertDiv.innerHTML = "";
    }, 3000);
}

function deleteWorkExperience(expUUID) {
    var workExperienceDelete = {
        work_experience_id : expUUID,
    };

    var workExperienceDeleteRequest = JSON.stringify(workExperienceDelete);
    fetch('/deleteWorkExperience', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: workExperienceDeleteRequest
    })
    .then(response => {
        if (!response.ok)
        {
            throw new Error("Response Error in Deletion")
        }
        return response.json();
    })
    .then(response => {
        if (response.response == 'success')
        {
            var formID = "workExpForm" + expUUID;
            var deleteForm = document.getElementById(formID);
            if (deleteForm)
            {
                deleteForm.parentNode.removeChild(deleteForm);
            }
        }
    })
}

function deleteEducationExperience(expUUID) {
    var educationExperienceDelete = {
        education_experience_id : expUUID,
    };

    var educationExperienceDeleteRequest = JSON.stringify(educationExperienceDelete);
    fetch('/deleteEducationExperience', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: educationExperienceDeleteRequest
    })
    .then(response => {
        if (!response.ok)
        {
            throw new Error("Response Error in Deletion")
        }
        return response.json();
    })
    .then(response => {
        if (response.response == 'success')
        {
            var formID = "eduExpForm" + expUUID;
            var deleteForm = document.getElementById(formID);
            if (deleteForm)
            {
                deleteForm.parentNode.removeChild(deleteForm);
            }
        }
    })
}

function saveAll() {
    if (profileType == "user")
    {
        //var profileID = editPageData.getAttribute("data-profile-id");
        var profileData = new FormData();
        profileData.append('type', profileType);
        profileData.append('profile_id', profileID);
        profileData.append('firstname', document.getElementById('firstnameField').value)
        profileData.append('lastname', document.getElementById('lastnameField').value)
        profileData.append('profile_bio', document.getElementById('bioField').value)
        var profile = document.getElementById('profileUpload')
        if (profile) {
            if (profile.files.length > 0) {
                profileData.append('profile_picture', profile.files[0]);
            }
        }
        var banner = document.getElementById('bannerUpload')
        if (banner) {
            if (banner.files.length > 0) {
                profileData.append('profile_banner', banner.files[0]);
            }
        }

        var workForms = document.querySelectorAll('[id^="workExpForm"]');
        var workFormArr = Array.from(workForms);
        workFormArr.forEach(form => {
            var formTitle = form.getAttribute('id');
            var expID = formTitle.replace('workExpForm', '');
            var title = form.querySelector('#titleField');
            var company = form.querySelector('#companyField');
            var sector = form.querySelector('#sectorSelect');
            var description = form.querySelector('#descField');
            var start_date = form.querySelector('#startDate');
            var end_date = form.querySelector('#endDate');
            var watercooler = form.querySelector('#waterCoolerCheck');
            updateWorkExperience(expID, title, company, sector, description, start_date, end_date, watercooler, "saveAll");
        })

        var eduForms = document.querySelectorAll('[id^="eduExpForm"]');
        var eduFormArr = Array.from(eduForms);
        eduFormArr.forEach(form => {
            var formTitle = form.getAttribute('id');
            var expID = formTitle.replace('eduExpForm', '');
            var institution = form.querySelector('#institutionField');
            var education_level = form.querySelector('#educationSelect');
            var study_area = form.querySelector('#areaField');
            var start_date = form.querySelector('#startDate');
            var end_date = form.querySelector('#endDate');
            updateEducationExperience(expID, institution, education_level, study_area, start_date, end_date, "saveAll");
        })
        
        fetch('/updateProfile', {
            method: 'POST',
            body: profileData
        })
        .then(response => {
            if (!response.ok)
            {
                throw new Error("Failure in main profile Update")
            }
            return response.json();
        })
        .then(response => {
            if ('redirect' in response) {
                window.location.href = response.redirect;
            }
        })
    }
    if (profileType == "company")
    {
        //var profileID = editPageData.getAttribute("data-profile-id");
        var profileData = new FormData();
        profileData.append('type', profileType);
        profileData.append('profile_id', profileID);
        profileData.append('name', document.getElementById('nameField').value);
        console.log(document.getElementById('aboutField').value);
        profileData.append('company_bio', document.getElementById('aboutField').value);
        var profile = document.getElementById('profileUpload');
        if (profile) {
            if (profile.files.length > 0) {
                profileData.append('company_image', profile.files[0]);
            }
        }
        var banner = document.getElementById('profileBanner');
        if (banner) {
            if (banner.files.length > 0) {
                profileData.append('company_banner', banner.files[0]);
            }
        }
        var aboutIMG1 = document.getElementById('aboutIMG1');
        if (aboutIMG1) {
            if (aboutIMG1.files.length > 0) {
                profileData.append('about_img_1', aboutIMG1.files[0]);
            }
        }
        var aboutIMG2 = document.getElementById('aboutIMG1');
        if (aboutIMG2) {
            if (aboutIMG2.files.length > 0) {
                profileData.append('about_img_1', aboutIMG2.files[0]);
            }
        }
        var aboutIMG3 = document.getElementById('aboutIMG1');
        if (aboutIMG3) {
            if (aboutIMG3.files.length > 0) {
                profileData.append('about_img_1', aboutIMG3.files[0]);
            }
        }
        fetch('/updateProfile', {
            method: 'POST',
            body: profileData
        })
        .then(response => {
            if (!response.ok)
            {
                throw new Error("Failure in company profile update")
            }
            return response.json();
        })
        .then(response => {
            console.log(response.message);
            if ('redirect' in response) {
                window.location.href = response.redirect;
            }
        })
    }
}


if (profileType == "user")
{
    //var profileID = editPageData.getAttribute("data-profile-id");
    var profileIDRequestData = {
        profile_id : profileID
    }
    var profileIDRequest = JSON.stringify(profileIDRequestData);

    document.getElementById("addWorkButton").addEventListener("click", function() {
        fetch('/addWorkExperience', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: profileIDRequest
        })
        .then(response => {
            if (!response.ok)
            {
                throw new Error("Response Error!");
            }
            return response.json();
        })
        .then(response => {
            if ('workExpID' in response)
            {
                var workExpID = response.workExpID;
                var jobSectorTypes = response.sectors;
                var workExpContainer = document.getElementById("workplaceExperienceContainer");
                var currentDate = new Date();
                var formattedDate = currentDate.toISOString().split('T')[0];
                workExpContainer.innerHTML+=`
                <form id="workExpForm${workExpID}" class="mx-3">
                    <div id="alert-div"></div>
                    <div class="row my-2">
                        <div class="col-4">
                            <label for="titleField" class="field-label">Job Title:</label>
                            <input class="form-control" id="titleField" type="text" placeholder="">
                        </div>
                        <div class="col-4">
                            <label for="companyField" class="field-label">Company Name:</label>
                            <input class="form-control" id="companyField" type="text" placeholder="">
                        </div>
                        <div class="col-4">
                            <label for="sectorSelect" class="field-label">Job Sector (Optional)</label>
                            <select class="form-select" id="sectorSelect" aria-label="Default select example">
                                <option selected>Job Sectors</option>
                            </select>
                        </div>
                    </div>
                    <div class="row my-2">
                        <div class="col">
                            <label for="descField" class="field-label">Enter Brief Job Description:</label>
                            <textarea class="form-control" id="descField" type="text" placeholder=""></textarea>
                        </div>
                    </div>
                    <div class="row my-2">
                        <div class="col-6">
                            <label for="startDate" class="field-label">Position Start Date:</label>
                            <input type="date" class="form-control" id="startDate" name="startDate" max=${formattedDate} min="1940-00-00">
                        </div>
                        <div class="col-6">
                            <label for="endDate" class="field-label">Position End Date (if applicable):</label>
                            <input type="date" class="form-control" id="endDate" name="endDate" max=${formattedDate} min="1940-00-00">
                        </div>
                    </div>
                    <div class="row my-2">
                        <div class="col">
                            <input class="form-check-input" type="checkbox" value="" id="waterCoolerCheck">
                            <label for="waterCoolerCheck" class="form-check-label field-label">Position Through TheWaterCooler?</label>
                        </div>
                    </div>
                    <div>
                        <button type="button" id="save${workExpID}Button" class="btn btn-success mt-2 mb-2" onclick="updateWorkExperience('${workExpID}', titleField, companyField, sectorSelect, descField, startDate, endDate, waterCoolerCheck, 'singleUpdate')">Save Experience</button>
                        <button type="button" id="delete${workExpID}Button" class="btn btn-danger mt-2 mb-2" onclick="deleteWorkExperience('${workExpID}')">Delete</button>
                    </div>
                </form>
            `;
            var selectBox = document.querySelector(`#workExpForm${workExpID} #sectorSelect`);
            jobSectorTypes.forEach(sector => {
                selectBox.innerHTML += `
                <option value="${sector}">${sector}</option>
                `;
            });
            }
        });
    })

    document.getElementById("addEducationButton").addEventListener("click", function() {
        fetch('/addEducationExperience', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: profileIDRequest
        })
        .then(response => {
            if (!response.ok)
            {
                throw new Error("Response Error!");
            }
            return response.json();
        })
        .then(response => { 
            if ('eduExpID' in response)
            {
                var eduExpID = response.eduExpID;
                var educationTypes = response.levels;
                var eduExpContainer = document.getElementById("educationExperienceContainer");
                var currentDate = new Date();
                var formattedDate = currentDate.toISOString().split('T')[0];
                eduExpContainer.innerHTML+=`
                <form id="eduExpForm${eduExpID}" class="mx-3">
                    <div id="alert-div"></div>
                    <div class="row my-2">
                        <div class="col-4">
                            <label for="institutionField" class="field-label">Institution Name:</label>
                            <input class="form-control" id="institutionField" type="text" placeholder="">
                        </div>
                        <div class="col-4">
                            <label for="educationSelect" class="field-label">Education Level:</label>
                            <select class="form-select" id="educationSelect" aria-label="Default select example">
                                <option selected>Education Levels</option>
                            </select>
                        </div>
                        <div class="col-4">
                            <label for="areaField" class="field-label">Area of Study:</label>
                            <input class="form-control" id="areaField" type="text" placeholder="">
                        </div>
                    </div>
                    <div class="row my-2">
                        <div class="col-6">
                            <label for="startDate" class="field-label">Position Start Date:</label>
                            <input type="date" class="form-control" id="startDate" name="startDate" max=${formattedDate} min="1940-00-00">
                        </div>
                        <div class="col-6">
                            <label for="endDate" class="field-label">Position End Date (if applicable):</label>
                            <input type="date" class="form-control" id="endDate" name="endDate" max=${formattedDate} min="1940-00-00">
                        </div>
                    </div>
                    <div>
                        <button type="button" id="save${eduExpID}Button" class="btn btn-success mt-2 mb-2" onclick="updateEducationExperience('${eduExpID}', institutionField, educationSelect, areaField, startDate, endDate)">Save Experience</button>
                        <button type="button" id="delete${eduExpID}Button" class="btn btn-danger mt-2 mb-2" onclick="deleteEducationExperience('${eduExpID}')">Delete</button>
                    </div>
                </form>
            `;
            var selectBox = document.querySelector(`#eduExpForm${eduExpID} #educationSelect`);
            educationTypes.forEach(sector => {
                selectBox.innerHTML += `
                <option value="${sector}">${sector}</option>
                `;
            });
            }
        })
    })
}






