from flask import Blueprint, jsonify, request

from app.utils.validators import validate_vehicle_data


vehicle_bp = Blueprint(
    "vehicles",
    __name__,
    url_prefix="/api/vehicles"
)


def create_vehicle_routes(service):

    @vehicle_bp.get("")
    def list_vehicles():
        search = request.args.get("search")

        vehicles = service.list(search)

        return jsonify(vehicles)

    @vehicle_bp.get("/<int:vehicle_id>")
    def get_vehicle(vehicle_id):
        vehicle = service.get_by_id(vehicle_id)

        if not vehicle:
            return jsonify({
                "error": "Veículo não encontrado."
            }), 404

        return jsonify(vehicle)

    @vehicle_bp.post("")
    def create_vehicle():
        data = request.get_json() or {}

        vehicle, error = service.create(data)

        if error:
            return jsonify({
                "error": error
            }), 400

        return jsonify(vehicle), 201

    @vehicle_bp.put("/<int:vehicle_id>")
    def update_vehicle(vehicle_id):
        data = request.get_json() or {}

        vehicle, error = service.update(
            vehicle_id,
            data
        )

        if error:
            status = 404 if error == "Veículo não encontrado." else 400

            return jsonify({
                "error": error
            }), status

        return jsonify(vehicle)

    @vehicle_bp.delete("/<int:vehicle_id>")
    def delete_vehicle(vehicle_id):
        success, error = service.delete(vehicle_id)

        if not success:
            return jsonify({
                "error": error
            }), 404

        return jsonify({
            "message": "Veículo excluído com sucesso."
        })

    @vehicle_bp.patch("/<int:vehicle_id>/mileage")
    def update_mileage(vehicle_id):
        data = request.get_json() or {}

        vehicle, error = service.update_mileage(
            vehicle_id,
            data.get("mileage")
        )

        if error:
            status = 404 if error == "Veículo não encontrado." else 400

            return jsonify({
                "error": error
            }), status

        return jsonify(vehicle)

    return vehicle_bp