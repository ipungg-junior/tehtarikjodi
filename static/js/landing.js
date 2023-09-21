const links = document.querySelectorAll('.nav a');
links.forEach(link => {
    link.addEventListener('click', function(e) {
        links.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

var elem = document.querySelector('.menu-slider');
var flkty = new Flickity( elem, {
  wrapAround: true,
});

document.addEventListener('DOMContentLoaded', function () {
  const burgerMenu = document.querySelector('.burger-menu');
  const burgerIcon = document.querySelector('.burger-icon');

  burgerIcon.addEventListener('click', function () {
    burgerMenu.classList.toggle('active');
  });
});

let prevScrollPos = window.scrollY;
const header = document.getElementById("main-header");

window.onscroll = function() {
    const currentScrollPos = window.scrollY;

    if (prevScrollPos > currentScrollPos) {
        header.style.top = "0";
    } else {
        header.style.top = `-${header.offsetHeight}em`;
    }

    prevScrollPos = currentScrollPos;
}