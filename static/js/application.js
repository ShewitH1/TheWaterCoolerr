const elements = document.getElementsByClassName('application-bar');

// make sure the script is being loaded
console.log('Application script loaded!');

Array.from(elements).forEach(element => {
    element.addEventListener('click', () => {
        console.log('Element clicked!');
        Array.from(elements).forEach(element => {
            element.classList.remove('application-bar-selected');
        });

        element.classList.add('application-bar-selected');
    });
});