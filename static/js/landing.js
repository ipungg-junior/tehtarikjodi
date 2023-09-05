const links = document.querySelectorAll('.nav a');
links.forEach(link => {
    link.addEventListener('click', function(e) {
        links.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});