import os
import random
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

# 1. Define global instances
mongo = PyMongo()
# Initialize metrics without app first to avoid circular import issues
metrics = PrometheusMetrics(app=None)

# Define the metric once globally
stock_gauge = metrics.info('stock_value', 'Simulated Stock Value')

def create_app():
    """Application factory function."""
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder='../templates'
    )

    # 2. Configuration
    # We use os.getenv to support Docker/K8s, but default to localhost for local testing
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/smart_office")
    app.config["SECRET_KEY"] = "dev"

    # 3. Initialize Extensions
    mongo.init_app(app)
    # Enable CORS for all domains to fix frontend connection issues
    CORS(app)
    # Initialize Prometheus
    metrics.init_app(app)

    # 4. Stock API Route (Required for DevOps/Grafana demo)
    @app.route('/api/stock')
    def get_stock():
        val = random.randint(50, 150)
        stock_gauge.set(val)
        return jsonify({"current_stock": val})

    # 5. Health Check Route
    @app.route('/health')
    def health_check():
        try:
            # Quick ping to check DB connection
            mongo.db.command('ping')
            return jsonify(status="healthy", db="connected"), 200
        except Exception as e:
            return jsonify(status="unhealthy", error=str(e)), 500

    # 6. Import & Register Blueprints
    from .blueprints.main import main_bp
    from .blueprints.control import control_bp
    from .blueprints.energy import energy_bp
    from .blueprints.parking import parking_bp
    from .blueprints.meeting_rooms import meeting_bp
    from .blueprints.wellness import wellness_bp
    from .blueprints.automation_rules import automation_rules_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(control_bp)
    app.register_blueprint(energy_bp)
    app.register_blueprint(parking_bp)
    app.register_blueprint(meeting_bp)
    app.register_blueprint(wellness_bp)
    app.register_blueprint(automation_rules_bp)

    return app