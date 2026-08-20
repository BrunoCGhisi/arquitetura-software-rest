class BrandService:

    def __init__(self, repository):
        self.repository = repository

    def list(self, search=None):
        data = self.repository.read()
        brands = data["brands"]

        if search:
            search = search.lower()

            brands = [
                brand
                for brand in brands
                if search in brand["name"].lower()
            ]

        return brands

    def get_by_id(self, brand_id):
        data = self.repository.read()

        for brand in data["brands"]:
            if brand["id"] == brand_id:
                return brand

        return None

    def create(self, brand_data):
        data = self.repository.read()

        new_id = self._next_id(data["brands"])

        brand = {
            "id": new_id,
            "name": brand_data["name"].strip(),
            "active": brand_data.get("active", True)
        }

        data["brands"].append(brand)

        self.repository.write(data)

        return brand

    def update(self, brand_id, brand_data):
        data = self.repository.read()

        for brand in data["brands"]:
            if brand["id"] == brand_id:

                if "name" in brand_data:
                    brand["name"] = brand_data["name"].strip()

                if "active" in brand_data:
                    brand["active"] = bool(brand_data["active"])

                self.repository.write(data)

                return brand

        return None

    def delete(self, brand_id):
        data = self.repository.read()

        vehicle_using_brand = any(
            vehicle["brand_id"] == brand_id
            for vehicle in data["vehicles"]
        )

        if vehicle_using_brand:
            return False, "Não é possível excluir uma marca utilizada por um veículo."

        original_length = len(data["brands"])

        data["brands"] = [
            brand
            for brand in data["brands"]
            if brand["id"] != brand_id
        ]

        if len(data["brands"]) == original_length:
            return False, "Marca não encontrada."

        self.repository.write(data)

        return True, None

    def _next_id(self, items):
        if not items:
            return 1

        return max(item["id"] for item in items) + 1