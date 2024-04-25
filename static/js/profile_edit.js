function updateWorkExperience(expUUID, title, cmpy_name, sector, descr, start, end, check) {
    console.log('calling');
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
    console.log(experienceDataRequest);
    fetch('/updateWorkExperience', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: experienceDataRequest
    })
    .then(response => {
        console.log(response);
        if (!response.ok)
        {
            throw new Error("Response Error in Work Experience Update");
        }
        return response.json();
    })
    .then(response => {
        console.log(response.response);
        var alertDiv = document.querySelector(`#workExpForm${expUUID} #alert-div`);
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
        console.log(response.message);
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

console.log("test");
var editPageData = document.getElementById("profileDataDiv");

var profileType = editPageData.getAttribute("data-profile-type");

console.log(profileType);

if (profileType == "user")
{
    var profileID = editPageData.getAttribute("data-profile-id");
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
            console.log(response.message);
            if ('workExpID' in response)
            {
                var workExpID = response.workExpID;
                var jobSectorTypes = response.sectors;
                var workExpContainer = document.getElementById("workplaceExperienceContainer");
                var currentDate = new Date();
                var formattedDate = currentDate.toISOString().split('T')[0];
                console.log(formattedDate);
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
                        <button type="button" id="save${workExpID}Button" class="btn btn-success mt-2 mb-2" onclick="updateWorkExperience('${workExpID}', titleField, companyField, sectorSelect, descField, startDate, endDate, waterCoolerCheck)">Save Experience</button>
                        <button type="button" id="delete${workExpID}Button" class="btn btn-danger mt-2 mb-2" onclick="deleteWorkExperience('${workExpID}')">Delete</button>
                    </div>
                </form>
            `;
            var selectBox = document.querySelector(`#workExpForm${workExpID} #sectorSelect`);
            console.log(selectBox);
            jobSectorTypes.forEach(sector => {
                console.log(sector);
                selectBox.innerHTML += `
                <option value="${sector}">${sector}</option>
                `;
            });
            }
        });
    })

    document.getElementById("addEducationButton").addEventListener("click", function() {

    })
}

if (profileType == "company")
{

}






