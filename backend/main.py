from flask import Flask, request, jsonify
from flask_cors import CORS
from psrqpy import QueryATNF
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "ColDToNs API is running"})

@app.route('/api/menu-config', methods=['GET'])
def get_menu_config():
    """Return the menu configuration for the frontend"""
    menu_config = {
        "database": {
            "title": "Database Tools",
            "tools": [
                {
                    "id": "adtn-catalog",
                    "name": "ADTN Catalog",
                    "icon": "fas fa-database",
                    "description": "Access the ADTN neutron star catalog"
                },
                {
                    "id": "data-import",
                    "name": "Data Import",
                    "icon": "fas fa-upload",
                    "description": "Import neutron star data from various sources"
                },
                {
                    "id": "data-export",
                    "name": "Data Export",
                    "icon": "fas fa-download",
                    "description": "Export processed data in various formats"
                },
                {
                    "id": "data-browser",
                    "name": "Data Browser",
                    "icon": "fas fa-table",
                    "description": "Browse and search through neutron star datasets"
                }
            ]
        },
        "analysis": {
            "title": "Analysis Tools",
            "tools": [
                {
                    "id": "statistical-analysis",
                    "name": "Statistical Analysis",
                    "icon": "fas fa-chart-bar",
                    "description": "Perform statistical analysis on neutron star data"
                },
                {
                    "id": "period-analysis",
                    "name": "Period Analysis",
                    "icon": "fas fa-wave-square",
                    "description": "Analyze pulsar periods and timing"
                }
            ]
        },
        "visualization": {
            "title": "Visualization Tools",
            "tools": [
                {
                    "id": "plot-generator",
                    "name": "Plot Generator",
                    "icon": "fas fa-chart-line",
                    "description": "Create various plots and charts"
                },
                {
                    "id": "sky-map",
                    "name": "Sky Map",
                    "icon": "fas fa-globe",
                    "description": "Visualize neutron star positions on sky map"
                }
            ]
        },
        "modeling": {
            "title": "Modeling Tools",
            "tools": [
                {
                    "id": "eos-modeling",
                    "name": "EoS Modeling",
                    "icon": "fas fa-atom",
                    "description": "Model equations of state for neutron star matter"
                }
            ]
        },
        "simulation": {
            "title": "Simulation Tools",
            "tools": [
                {
                    "id": "merger-simulation",
                    "name": "Merger Simulation",
                    "icon": "fas fa-expand-arrows-alt",
                    "description": "Simulate neutron star mergers"
                }
            ]
        },
        "collaboration": {
            "title": "Collaboration Tools",
            "tools": [
                {
                    "id": "project-sharing",
                    "name": "Project Sharing",
                    "icon": "fas fa-share",
                    "description": "Share projects and collaborate with others"
                }
            ]
        },
        "help": {
            "title": "Help & Documentation",
            "tools": [
                {
                    "id": "documentation",
                    "name": "Documentation",
                    "icon": "fas fa-book",
                    "description": "Access comprehensive documentation"
                },
                {
                    "id": "tutorials",
                    "name": "Tutorials",
                    "icon": "fas fa-graduation-cap",
                    "description": "Interactive tutorials and guides"
                }
            ]
        }
    }
    return jsonify(menu_config)

@app.route('/api/atnf-parameters', methods=['GET'])
def get_atnf_parameters():
    """Return ATNF parameter list"""
    atnf_params = [
        "JNAME", "RAJ", "DECJ", "P0", "DM", "F0", "F1", "GL", "GB",
        "S400", "S1400", "W50", "W10", "BINARY", "DIST", "AGE", "EDOT"
    ]
    return jsonify(atnf_params)

# Tool-specific API endpoints
@app.route('/api/tools/adtn-catalog/data', methods=['POST'])
def adtn_catalog_data():
    query = QueryATNF(params=request.json.get('parameters', []),psrs=request.json.get('pulsarNames', []))
    return jsonify(query.data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)