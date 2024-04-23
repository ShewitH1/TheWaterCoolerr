document.addEventListener("DOMContentLoaded", function() {
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
            console.log(response);
            if ('html' in response) {
                // Replace the entire HTML content of the page with the received template HTML
                document.documentElement.innerHTML = response.html;

                // Dispatch a new DOMContentLoaded event to initialize any JavaScript
                document.dispatchEvent(new Event('DOMContentLoaded'));
            }
        });
    });
});