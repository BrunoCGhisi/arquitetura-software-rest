from app.utils.validators import validate_vehicle_data


class VehicleService:

    def __init__(self, repository):
        self.repository = repository

    def list(self, search=None):
        data = self.repository.read()

        vehicles = data["vehicles"]

        if search:
            search = search.lower()

            vehicles = [
                vehicle
                for vehicle in vehicles
                if search in vehicle["plate"].lower()
                or search in vehicle["model"].lower()
            ]

        return self._add_brand_information(vehicles, data["brands"])

    def get_by_id(self, vehicle_id):
        data = self.repository.read()

        for vehicle in data["vehicles"]:
            if vehicle["id"] == vehicle_id:
                return self._add_brand_information(
                    [vehicle],
                    data["brands"]
                )[0]

        return None

    def create(self, vehicle_data):
        valid, error = validate_vehicle_data(vehicle_data)

        if not valid:
            return None, error

        data = self.repository.read()

        brand_id = int(vehicle_data["brand_id"])

        brand = next(
            (
                brand
                for brand in data["brands"]
                if brand["id"] == brand_id
            ),
            None
        )

        if not brand:
            return None, "Marca não encontrada."

        if not brand["active"]:
            return None, "Não é possível cadastrar veículo com marca inativa."

        new_id = self._next_id(data["vehicles"])

        vehicle = {
            "id": new_id,
            "plate": vehicle_data["plate"].strip().upper(),
            "model": vehicle_data["model"].strip(),
            "year": int(vehicle_data["year"]),
            "brand_id": brand_id,
            "mileage": int(vehicle_data.get("mileage", 0))
        }

        data["vehicles"].append(vehicle)

        self.repository.write(data)

        return vehicle, None

    def update(self, vehicle_id, vehicle_data):
        data = self.repository.read()

        vehicle = next(
            (
                vehicle
                for vehicle in data["vehicles"]
                if vehicle["id"] == vehicle_id
            ),
            None
        )

        if not vehicle:
            return None, "Veículo não encontrado."

        valid, error = validate_vehicle_data(vehicle_data)

        if not valid:
            return None, error

        brand_id = int(vehicle_data["brand_id"])

        brand = next(
            (
                brand
                for brand in data["brands"]
                if brand["id"] == brand_id
            ),
            None
        )

        if not brand:
            return None, "Marca não encontrada."

        if not brand["active"]:
            return None, "Não é possível utilizar uma marca inativa."

        vehicle["plate"] = vehicle_data["plate"].strip().upper()
        vehicle["model"] = vehicle_data["model"].strip()
        vehicle["year"] = int(vehicle_data["year"])
        vehicle["brand_id"] = brand_id

        self.repository.write(data)

        return vehicle, None

    def delete(self, vehicle_id):
        data = self.repository.read()

        original_length = len(data["vehicles"])

        data["vehicles"] = [
            vehicle
            for vehicle in data["vehicles"]
            if vehicle["id"] != vehicle_id
        ]

        if len(data["vehicles"]) == original_length:
            return False, "Veículo não encontrado."

        self.repository.write(data)

        return True, None

    def update_mileage(self, vehicle_id, new_mileage):
        data = self.repository.read()

        vehicle = next(
            (
                vehicle
                for vehicle in data["vehicles"]
                if vehicle["id"] == vehicle_id
            ),
            None
        )

        if not vehicle:
            return None, "Veículo não encontrado."

        try:
            new_mileage = int(new_mileage)
        except (ValueError, TypeError):
            return None, "Quilometragem inválida."

        if new_mileage < vehicle["mileage"]:
            return None, "A nova quilometragem não pode ser menor que a atual."

        vehicle["mileage"] = new_mileage

        self.repository.write(data)

        return vehicle, None

    def _add_brand_information(self, vehicles, brands):
        result = []

        for vehicle in vehicles:
            vehicle_copy = vehicle.copy()

            brand = next(
                (
                    brand
                    for brand in brands
                    if brand["id"] == vehicle["brand_id"]
                ),
                None
            )

            vehicle_copy["brand"] = brand

            result.append(vehicle_copy)

        return result

    def _next_id(self, items):
        if not items:
            return 1

        return max(item["id"] for item in items) + 1