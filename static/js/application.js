const elements = document.getElementsByClassName('application-bar');

Array.from(elements).forEach(element => {
    element.addEventListener('click', () => {
        Array.from(elements).forEach(element => {
            element.classList.remove('application-bar-selected');
        });

        element.classList.add('application-bar-selected');
    });
});