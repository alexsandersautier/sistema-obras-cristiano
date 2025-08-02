const logoLink = document.getElementById('jazzy-logo');
logoLink.setAttribute('href', '/admin/building/building/');

const footer = document.querySelector('.main-footer')
footer.innerHTML = `© ${new Date().getFullYear()} Sistema desenvolvido por Alexsander Sautier`