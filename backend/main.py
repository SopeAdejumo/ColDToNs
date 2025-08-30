from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from psrqpy import QueryATNF
import os
import pandas as pd
import json
from io import BytesIO, StringIO
from astroquery.heasarc import Heasarc

# Create Flask app with static folder pointing to built frontend
app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app)  # Enable CORS for React frontend

# Global variable to cache HEASARC data
heasarc_data = None
heasarc_jnames = set()

def initialize_heasarc_data():
    """Initialize HEASARC data on startup"""
    global heasarc_data, heasarc_jnames
    try:
        print("Initializing HEASARC data...")
        heasarc = Heasarc()
        # Query the nicermastr catalog for all observations
        print("Querying HEASARC nicermastr catalog...")
        heasarc_data = heasarc.query_region(catalog="nicermastr", spatial='all-sky')
        
        if heasarc_data is not None and len(heasarc_data) > 0:
            # Extract unique JNAMEs from the HEASARC data
            # The column name might be different, let's check common variations
            possible_jname_columns = ['JNAME', 'jname', 'NAME', 'name', 'OBJECT', 'object']
            jname_column = None
            
            for col in possible_jname_columns:
                if col in heasarc_data.colnames:
                    jname_column = col
                    break
            
            if jname_column:
                heasarc_jnames = set(str(jname).strip() for jname in heasarc_data[jname_column] if jname)
                print(f"Found {len(heasarc_jnames)} unique JNAMEs in HEASARC database")
                print(f"Sample JNAMEs: {list(heasarc_jnames)[:5]}")
            else:
                print("Warning: Could not find JNAME column in HEASARC data")
                print(f"Available columns: {heasarc_data.colnames}")
        else:
            print("Warning: No HEASARC data retrieved")
            
    except Exception as e:
        print(f"Error initializing HEASARC data: {e}")
        heasarc_data = None
        heasarc_jnames = set()

# Initialize HEASARC data when the app starts
initialize_heasarc_data()

# Serve React App
@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    # Serve static files (CSS, JS, images, etc.)
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # For client-side routing, serve index.html for unknown routes
        return send_from_directory(app.static_folder, 'index.html')

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    global heasarc_data, heasarc_jnames
    heasarc_status = {
        "available": heasarc_data is not None,
        "jname_count": len(heasarc_jnames)
    }
    return jsonify({
        "status": "healthy", 
        "message": "ColDToNs API is running",
        "heasarc": heasarc_status
    })

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

@app.route('/api/heasarc-jnames', methods=['GET'])
def get_heasarc_jnames():
    """Return list of JNAMEs available in HEASARC database"""
    global heasarc_jnames
    return jsonify(list(heasarc_jnames))

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

@app.route('/api/tools/adtn-catalog/heasarc', methods=['POST'])
def adtn_catalog_heasarc():
    """
    Query HEASARC database for a specific pulsar JNAME
    Based on the usage pattern from nicer_test.py
    """
    try:
        jname = request.json.get('jname', '')
        
        if not jname:
            return jsonify({"error": "JNAME is required"}), 400
        
        global heasarc_data, heasarc_jnames
        
        # Check if JNAME exists in our cached data
        if jname not in heasarc_jnames:
            return jsonify({
                "error": f"JNAME {jname} not found in HEASARC database",
                "jname": jname,
                "available": False
            }), 404
        
        # If we have the data cached, filter it for this specific JNAME
        if heasarc_data is not None:
            # Find the correct JNAME column
            possible_jname_columns = ['JNAME', 'jname', 'NAME', 'name', 'OBJECT', 'object']
            jname_column = None
            
            for col in possible_jname_columns:
                if col in heasarc_data.colnames:
                    jname_column = col
                    break
            
            if jname_column:
                # Filter data for the specific JNAME
                mask = [str(row[jname_column]).strip() == jname for row in heasarc_data]
                filtered_data = heasarc_data[mask]
                
                if len(filtered_data) > 0:
                    # Convert to pandas DataFrame for easier JSON serialization
                    df = filtered_data.to_pandas()
                    
                    # Convert to records format
                    records = df.to_dict('records')
                    
                    return jsonify({
                        "jname": jname,
                        "available": True,
                        "count": len(records),
                        "data": records,
                        "columns": list(df.columns),
                        "message": f"Found {len(records)} HEASARC observations for {jname}"
                    })
                else:
                    return jsonify({
                        "error": f"No observations found for {jname} in HEASARC data",
                        "jname": jname,
                        "available": False
                    }), 404
            else:
                return jsonify({
                    "error": "Could not find JNAME column in HEASARC data",
                    "jname": jname,
                    "available": False
                }), 500
        else:
            return jsonify({
                "error": "HEASARC data not available",
                "jname": jname,
                "available": False
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)