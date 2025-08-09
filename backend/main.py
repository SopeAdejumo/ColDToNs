from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from psrqpy import QueryATNF
import os
import pandas as pd
import json
from io import BytesIO, StringIO

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
    pulsar_names = request.json.get('pulsarNames', [])
    parameters = request.json.get('parameters', [])
    
    # If no pulsar names provided, query the entire catalog
    if not pulsar_names or (len(pulsar_names) == 1 and pulsar_names[0] == ''):
        query = QueryATNF(params=parameters)
    else:
        query = QueryATNF(params=parameters, psrs=pulsar_names)
    
    return jsonify(query.pandas.to_dict('records'))

@app.route('/api/tools/adtn-catalog/download', methods=['POST'])
def adtn_catalog_download():
    try:
        data = request.json.get('data', [])
        parameters = request.json.get('parameters', [])
        file_format = request.json.get('format', 'csv').lower()
        
        if not data:
            return jsonify({"error": "No data to download"}), 400
        
        # Convert data to pandas DataFrame
        df = pd.DataFrame(data)
        
        # Reorder columns to match the parameters order if specified
        if parameters:
            # Only include columns that exist in the DataFrame
            available_params = [param for param in parameters if param in df.columns]
            if available_params:
                df = df[available_params]
        
        # Generate file based on format
        if file_format == 'csv':
            output = StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            
            # Convert StringIO to BytesIO for send_file
            bytes_output = BytesIO()
            bytes_output.write(output.getvalue().encode('utf-8'))
            bytes_output.seek(0)
            
            return send_file(
                bytes_output,
                mimetype='text/csv',
                as_attachment=True,
                download_name='atnf_catalog.csv'
            )
            
        elif file_format == 'json':
            output = BytesIO()
            json_data = df.to_dict('records')
            output.write(json.dumps(json_data, indent=2).encode('utf-8'))
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/json',
                as_attachment=True,
                download_name='atnf_catalog.json'
            )
            
        elif file_format == 'xlsx':
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='ATNF Catalog', index=False)
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='atnf_catalog.xlsx'
            )
            
        else:
            return jsonify({"error": f"Unsupported format: {file_format}"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)