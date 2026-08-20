import os

from flask import Flask, render_template

from app.repositories.json_repository import JsonRepository
from app.services.brand_service import BrandService
from app.services.vehicle_service import VehicleService
from app.routes.brand_routes import create_brand_routes
from app.routes.vehicle_routes import create_vehicle_routes


def create_app():

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    database_path = os.path.join(
        base_dir,
        "data",
        "db.json"
    )

    repository = JsonRepository(database_path)

    brand_service = BrandService(repository)
    vehicle_service = VehicleService(repository)

    app.register_blueprint(
        create_brand_routes(brand_service)
    )

    app.register_blueprint(
        create_vehicle_routes(vehicle_service)
    )

    @app.get("/")
    def index():
        return render_template("index.html")

    return app