from flask import Blueprint, jsonify, request

from app.utils.validators import validate_brand_data


brand_bp = Blueprint("brands", __name__, url_prefix="/api/brands")


def create_brand_routes(service):

    @brand_bp.get("")
    def list_brands():
        search = request.args.get("search")

        brands = service.list(search)

        return jsonify(brands)

    @brand_bp.get("/<int:brand_id>")
    def get_brand(brand_id):
        brand = service.get_by_id(brand_id)

        if not brand:
            return jsonify({
                "error": "Marca não encontrada."
            }), 404

        return jsonify(brand)

    @brand_bp.post("")
    def create_brand():
        data = request.get_json() or {}

        valid, error = validate_brand_data(data)

        if not valid:
            return jsonify({
                "error": error
            }), 400

        brand = service.create(data)

        return jsonify(brand), 201

    @brand_bp.put("/<int:brand_id>")
    def update_brand(brand_id):
        data = request.get_json() or {}

        valid, error = validate_brand_data(data)

        if not valid:
            return jsonify({
                "error": error
            }), 400

        brand = service.update(brand_id, data)

        if not brand:
            return jsonify({
                "error": "Marca não encontrada."
            }), 404

        return jsonify(brand)

    @brand_bp.delete("/<int:brand_id>")
    def delete_brand(brand_id):
        success, error = service.delete(brand_id)

        if not success:
            return jsonify({
                "error": error
            }), 400

        return jsonify({
            "message": "Marca excluída com sucesso."
        })

    return brand_bp