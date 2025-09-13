const year = document.getElementById('yearSelect');
const month = document.getElementById('monthSelect');
const currentBuilding = document.getElementById('buildingSelect');
const currentTeam = document.getElementById('teamSelect');
const tableTitle = document.getElementById('tableTitle');
if (tableTitle) tableTitle.innerText = `Obra: ${currentBuilding.value} - Equipe: ${currentTeam.value}`

const logoLink = document.getElementById('jazzy-logo');
if (logoLink) {
    logoLink.setAttribute('href', '/admin/building/building/');
}

const footer = document.querySelector('.main-footer');
if (footer) {
    footer.innerHTML = `<strong>© ${new Date().getFullYear()} Sistema desenvolvido por Alexsander Sautier</strong>`;
}

const filters = document.getElementById('formData');

if (filters) {
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
}

if (year && month && currentBuilding && currentTeam) {
    year.addEventListener('change', () => filters.requestSubmit());
    month.addEventListener('change', () => filters.requestSubmit());
    currentBuilding.addEventListener('change', () => filters.requestSubmit());
    currentTeam.addEventListener('change', () => filters.requestSubmit());
}

document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector(".main-header");

    const button = document.createElement("button");
    button.innerHTML = '<i class="fa-solid fa-moon"></i>';
    button.className = "btn btn-sm btn-primary ml-2";
    button.style.marginLeft = "1rem";

    const body = document.body;
    const currentTheme = localStorage.getItem("jazzmin-theme") || "default";

    if (currentTheme === "darkly") {
        body.className = "theme-darkly dark-mode";
        button.innerHTML = '<i class="fa-solid fa-sun"></i>';
    } else {
        body.className = "theme-flatly";
        button.innerHTML = '<i class="fa-solid fa-moon"></i>';
    }

    button.addEventListener("click", () => {
        const newTheme = body.className.includes("darkly") ? "flatly" : "darkly";
        localStorage.setItem("jazzmin-theme", newTheme);
        location.reload();
    });

    if (header) {
        header.appendChild(button);
    }

    const loginBox = document.querySelector('.login-box')
    
    
    setInterval(() => {
        body.style.minHeight = '100vh';
        loginBox.style.margin = 'auto'
    },200)
});
