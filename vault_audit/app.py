from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from modules.parser.parser import parse_container_file
from modules.auditor.auditor import VaultAuditor
from modules.export.exporter import export_audit_results
from modules.database.db_manager import DatabaseManager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['EXPORT_FOLDER'] = os.path.join(os.path.dirname(__file__), 'exports')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

db_manager = DatabaseManager(os.path.join(os.path.dirname(__file__), 'vault_audit.db'))

container_data = None
auditor = None
last_audit_result = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global container_data, auditor

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Only .xlsx files are allowed'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        container_data = parse_container_file(filepath)
        auditor = VaultAuditor(container_data)

        response_data = {
            'success': True,
            'location': container_data.location_name,
            'created_at': container_data.parameters.created_at,
            'created_by': container_data.parameters.created_by,
            'carrier': container_data.parameters.carrier,
            'carrier_location': container_data.parameters.carrier_location,
            'total_valid_labels': len(container_data.valid_labels),
            'valid_labels': sorted(list(container_data.valid_labels))
        }

        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audit', methods=['POST'])
def audit():
    global auditor, last_audit_result

    if not auditor:
        return jsonify({'error': 'Please upload a container file first'}), 400

    data = request.json
    scanned_labels = data.get('scanned_labels', [])

    result = auditor.audit(scanned_labels)
    summary = auditor.get_summary(result)

    last_audit_result = result

    # Record import to database (only when Complete Audit is pressed)
    import_stats = None
    try:
        import_stats = db_manager.record_import(
            import_date=container_data.parameters.created_at_date,
            carrier_location=container_data.parameters.carrier_location,
            valid_labels=list(container_data.valid_labels)
        )
    except Exception as import_error:
        print(f"Error recording import: {import_error}")

    # Record scanned labels to database
    bag_records = {}
    for label in scanned_labels:
        if label.strip():
            try:
                record = db_manager.record_scan(label.strip(), container_data.parameters.carrier_location)
                bag_records[label.strip()] = record
            except Exception as e:
                print(f"Error recording scan for {label}: {e}")

    # Get location tracking stats
    location_stats = db_manager.get_location_stats(container_data.parameters.carrier_location)

    return jsonify({
        'summary': summary,
        'matched_labels': sorted(list(result.matched_labels)),
        'unmatched_labels': sorted(list(result.unmatched_labels)),
        'expected_not_scanned': sorted(list(result.expected_not_scanned)),
        'bag_records': bag_records,
        'location_stats': location_stats,
        'import_stats': import_stats
    })

@app.route('/export', methods=['GET'])
def export():
    global last_audit_result, container_data

    if not last_audit_result:
        return jsonify({'error': 'No audit results to export'}), 400

    if not container_data:
        return jsonify({'error': 'No container data available'}), 400

    try:
        # Get location stats for export
        location_stats = db_manager.get_location_stats(container_data.parameters.carrier_location)

        # Get ALL labels that are >=3 days old (import-based tracking)
        labels_over_3_days = db_manager.get_labels_over_3_days(container_data.parameters.carrier_location)

        # Get import duration stats for export (replaces scan-based duration)
        import_durations = db_manager.get_import_duration_stats(
            label_ids=list(container_data.valid_labels),
            carrier_location=container_data.parameters.carrier_location
        )

        container_info = {
            'location': container_data.location_name,
            'carrier': container_data.parameters.carrier,
            'created_at': container_data.parameters.created_at,
            'created_by': container_data.parameters.created_by,
            'location_stats': location_stats
        }

        filepath = export_audit_results(
            last_audit_result,
            container_info,
            app.config['EXPORT_FOLDER'],
            import_durations,  # Pass import durations instead of bag durations
            labels_over_3_days  # Pass labels that are >=3 days old
        )

        return send_file(
            filepath,
            as_attachment=True,
            download_name=os.path.basename(filepath)
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bags/<label_id>', methods=['GET'])
def get_bag(label_id):
    try:
        bag = db_manager.get_bag_by_label(label_id)
        if bag:
            return jsonify(bag)
        return jsonify({'error': 'Bag not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bags', methods=['GET'])
def get_all_bags():
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        bags = db_manager.get_all_bags(limit=limit, offset=offset)
        return jsonify({'bags': bags, 'count': len(bags)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bags/location/<location>', methods=['GET'])
def get_bags_by_location(location):
    try:
        bags = db_manager.get_bags_by_location(location)
        return jsonify({'bags': bags, 'count': len(bags), 'location': location})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bags/<label_id>', methods=['DELETE'])
def delete_bag(label_id):
    try:
        success = db_manager.delete_bag(label_id)
        if success:
            return jsonify({'success': True, 'message': f'Bag {label_id} deleted'})
        return jsonify({'error': 'Bag not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Support Railway and other cloud platforms with PORT env variable
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)