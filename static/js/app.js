const vehicleForm = document.getElementById("vehicle-form");
const brandForm = document.getElementById("brand-form");


document.addEventListener("DOMContentLoaded", () => {
    loadBrands();
    loadVehicles();
});


vehicleForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const id = document.getElementById("vehicle-id").value;

    const vehicle = {
        plate: document.getElementById("plate").value,
        model: document.getElementById("model").value,
        year: document.getElementById("year").value,
        brand_id: document.getElementById("brand-id").value,
        mileage: document.getElementById("mileage").value
    };

    const url = id
        ? `/api/vehicles/${id}`
        : "/api/vehicles";

    const method = id ? "PUT" : "POST";

    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(vehicle)
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
        return;
    }

    alert("Veículo salvo com sucesso.");

    clearVehicleForm();
    loadVehicles();
});


brandForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const id = document.getElementById("brand-id").value;

    const brand = {
        name: document.getElementById("brand-name").value,
        active: document.getElementById("brand-active").checked
    };

    const url = id
        ? `/api/brands/${id}`
        : "/api/brands";

    const method = id ? "PUT" : "POST";

    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(brand)
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
        return;
    }

    alert("Marca salva com sucesso.");

    clearBrandForm();
    loadBrands();
});


async function loadBrands() {

    const response = await fetch("/api/brands");
    const brands = await response.json();

    const select = document.getElementById("brand-id");

    select.innerHTML = `
        <option value="">
            Selecione a marca
        </option>
    `;

    brands
        .filter(brand => brand.active)
        .forEach(brand => {

            select.innerHTML += `
                <option value="${brand.id}">
                    ${brand.name}
                </option>
            `;
        });

    renderBrands(brands);
}


function renderBrands(brands) {

    const table = document.getElementById("brands-table");

    table.innerHTML = "";

    brands.forEach(brand => {

        table.innerHTML += `
            <tr>

                <td>${brand.id}</td>

                <td>${brand.name}</td>

                <td>
                    ${brand.active ? "Ativa" : "Inativa"}
                </td>

                <td>

                    <button
                        onclick='editBrand(${JSON.stringify(brand)})'
                    >
                        Editar
                    </button>

                    <button
                        onclick="deleteBrand(${brand.id})"
                    >
                        Excluir
                    </button>

                </td>

            </tr>
        `;
    });
}


async function loadVehicles() {

    const search = document
        .getElementById("vehicle-search")
        .value;

    const response = await fetch(
        `/api/vehicles?search=${encodeURIComponent(search)}`
    );

    const vehicles = await response.json();

    renderVehicles(vehicles);
}


function renderVehicles(vehicles) {

    const table = document.getElementById("vehicles-table");

    table.innerHTML = "";

    vehicles.forEach(vehicle => {

        const brandName = vehicle.brand
            ? vehicle.brand.name
            : "Sem marca";

        table.innerHTML += `
            <tr>

                <td>${vehicle.id}</td>

                <td>${vehicle.plate}</td>

                <td>${vehicle.model}</td>

                <td>${vehicle.year}</td>

                <td>${brandName}</td>

                <td>${vehicle.mileage} km</td>

                <td>

                    <button
                        onclick='editVehicle(${JSON.stringify(vehicle)})'
                    >
                        Editar
                    </button>

                    <button
                        onclick="updateMileage(${vehicle.id})"
                    >
                        Atualizar KM
                    </button>

                    <button
                        onclick="deleteVehicle(${vehicle.id})"
                    >
                        Excluir
                    </button>

                </td>

            </tr>
        `;
    });
}


function editVehicle(vehicle) {

    document.getElementById("vehicle-id").value = vehicle.id;
    document.getElementById("plate").value = vehicle.plate;
    document.getElementById("model").value = vehicle.model;
    document.getElementById("year").value = vehicle.year;
    document.getElementById("brand-id").value = vehicle.brand_id;
    document.getElementById("mileage").value = vehicle.mileage;

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


async function deleteVehicle(id) {

    if (!confirm("Deseja excluir este veículo?")) {
        return;
    }

    const response = await fetch(
        `/api/vehicles/${id}`,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
        return;
    }

    loadVehicles();
}


async function updateMileage(id) {

    const mileage = prompt(
        "Informe a nova quilometragem:"
    );

    if (mileage === null) {
        return;
    }

    const response = await fetch(
        `/api/vehicles/${id}/mileage`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mileage: mileage
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
        return;
    }

    loadVehicles();
}


function editBrand(brand) {

    document.getElementById("brand-id").value = brand.id;
    document.getElementById("brand-name").value = brand.name;
    document.getElementById("brand-active").checked = brand.active;
}


async function deleteBrand(id) {

    if (!confirm("Deseja excluir esta marca?")) {
        return;
    }

    const response = await fetch(
        `/api/brands/${id}`,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
        return;
    }

    loadBrands();
}


function clearVehicleForm() {

    vehicleForm.reset();

    document.getElementById("vehicle-id").value = "";
    document.getElementById("mileage").value = 0;
}


function clearBrandForm() {

    brandForm.reset();

    document.getElementById("brand-id").value = "";
    document.getElementById("brand-active").checked = true;
}