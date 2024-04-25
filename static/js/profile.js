document.addEventListener("DOMContentLoaded", function() {
    var editProfileButton = document.getElementById("editProfileButton")
    if (editProfileButton) {
    document.getElementById("editProfileButton").addEventListener("click", function() {
        var editProfileID = this.getAttribute("data-profile-id");
    
        var request = {
            profile_id : editProfileID
        };
    
        var requestJson = JSON.stringify(request);

        fetch('/editProfile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: requestJson
        })
        .then(response => {
            if (!response.ok)
            {
                throw new Error("Response Error!");
            }
            return response.json();
        })
        .then(response => {
            if ('html' in response) {
                // Replace the entire HTML content of the page with the received template HTML
                document.documentElement.innerHTML = response.html;
                // Dispatch a new DOMContentLoaded event to initialize any JavaScript
                var editScript = document.createElement("script");
                editScript.setAttribute("src", baseURL + 'js/profile_edit.js');
                document.head.append(editScript);
                document.dispatchEvent(new Event('DOMContentLoaded'));
            }
        });
    });
    } else {
        //console.log('fuck');
        // console.log(document.currentScript);
        // var currentScript = this.currentScript;
        // if (currentScript) {
        //     currentScript.parentNode.removeChild(currentScript);
        // }
    }
});