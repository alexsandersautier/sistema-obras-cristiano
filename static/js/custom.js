const currentYear = new Date().getFullYear();
const currentMonth = new Date().getMonth();

const year = document.getElementById('yearSelect');
const month = document.getElementById('monthSelect');
const currentBuilding = document.getElementById('buildingSelect');
const currentTeam = document.getElementById('teamSelect');

document.getElementById('tableTitle').innerText = `Obra: ${currentBuilding.value} - Equipe: ${currentTeam.value}`

const logoLink = document.getElementById('jazzy-logo');
logoLink.setAttribute('href', '/admin/building/building/');

const footer = document.querySelector('.main-footer');
footer.innerHTML = `<strong>© ${currentYear} Sistema desenvolvido por Alexsander Sautier</strong>`;

const filters = document.getElementById('formData');

filters.addEventListener('submit', (event) => {
    event.preventDefault();

    const params = new URLSearchParams({
        year: year.value,
        month: month.value,
        building: currentBuilding.value,
        team: currentTeam.value,
    });

    window.location.href = window.location.pathname + '?' + params.toString();
});

year.addEventListener('change', () => filters.requestSubmit());
month.addEventListener('change', () => filters.requestSubmit());
currentBuilding.addEventListener('change', () => filters.requestSubmit());
currentTeam.addEventListener('change', () => filters.requestSubmit());