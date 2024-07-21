



const listButtons = document.querySelectorAll('li');

listButtons.forEach(item => {
    item.addEventListener('click', (event) => {
        const link = item.querySelector('a');
        if(link) {
            window.location.href = link.href;
        }

    });
    item.style.cursor = 'pointer';
});

