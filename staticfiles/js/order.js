document.addEventListener("DOMContentLoaded", function () {
    const buildingSelect = document.querySelector("#id_building");
    if (buildingSelect) {
        $(buildingSelect).on("select2:select", function (e) {
            const buildingId = this.value;
            if (!buildingId) return;

            fetch(`/get-services/${buildingId}/`)
                .then((response) => response.json())
                .then((services) => {
                    const selects = document.querySelectorAll("select[id$='-service_price']");
                    selects.forEach((select) => {
                        select.innerHTML = "";
                        const emptyOption = document.createElement("option");
                        emptyOption.value = "";
                        emptyOption.textContent = "---------";
                        select.appendChild(emptyOption);

                        services.forEach((service) => {
                            const option = document.createElement("option");
                            option.value = service.id;
                            option.textContent = service.text;
                            select.appendChild(option);
                        });
                    });
                });
        });
    }
});
