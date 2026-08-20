def validate_vehicle_data(data):
    required_fields = [
        "plate",
        "model",
        "year",
        "brand_id"
    ]

    for field in required_fields:
        if field not in data:
            return False, f"O campo '{field}' é obrigatório."

    if not str(data["plate"]).strip():
        return False, "A placa é obrigatória."

    if not str(data["model"]).strip():
        return False, "O modelo é obrigatório."

    try:
        year = int(data["year"])

        if year < 1900:
            return False, "Ano do veículo inválido."

    except (ValueError, TypeError):
        return False, "Ano do veículo inválido."

    try:
        brand_id = int(data["brand_id"])
    except (ValueError, TypeError):
        return False, "Marca inválida."

    return True, None


def validate_brand_data(data):
    if "name" not in data:
        return False, "O nome da marca é obrigatório."

    if not str(data["name"]).strip():
        return False, "O nome da marca é obrigatório."

    return True, None