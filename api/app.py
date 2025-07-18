"""
Flask API for Real-time Face Recognition Attendance System
Optimized for macOS M2 Air with 8GB RAM
"""

import base64
import csv
import io
import logging
import os
import sys
import threading
from datetime import datetime

import cv2
import numpy as np
from flask import Flask, jsonify, render_template, request, send_from_directory
from PIL import Image

# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from direct_recognizer import create_direct_recognizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('face_recognition_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('face_recognition_request_duration_seconds', 'Request duration', ['method', 'endpoint'])
FACE_RECOGNITION_COUNT = Counter('face_recognitions_total', 'Total face recognitions', ['result'])
FACE_RECOGNITION_CONFIDENCE = Histogram('face_recognition_confidence', 'Face recognition confidence scores')
ATTENDANCE_COUNT = Counter('attendance_records_total', 'Total attendance records')
KNOWN_FACES_GAUGE = Gauge('known_faces_count', 'Number of known faces in system')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')

# Initialize Flask app with frontend paths
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app = Flask(
    __name__,
    template_folder=os.path.join(frontend_dir, "templates"),
    static_folder=os.path.join(frontend_dir, "static"),
)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max file size

# Prometheus middleware
@app.before_request
def before_request():
    request.start_time = time.time()
    ACTIVE_CONNECTIONS.inc()

@app.after_request
def after_request(response):
    request_duration = time.time() - request.start_time
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown'
    ).observe(request_duration)
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    
    ACTIVE_CONNECTIONS.dec()
    return response

# Global error handler to ensure JSON responses
@app.errorhandler(Exception)
def handle_exception(e):
    """Catch all unhandled exceptions and return JSON error"""
    logger.error(f"Unhandled exception: {e}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Return JSON error response
    return jsonify({
        "error": "Internal server error",
        "message": str(e),
        "type": type(e).__name__
    }), 500

@app.errorhandler(413)
def handle_file_too_large(e):
    """Handle file too large error"""
    return jsonify({
        "error": "File too large",
        "message": "The uploaded file exceeds the maximum size limit of 50MB"
    }), 413

@app.errorhandler(400)
def handle_bad_request(e):
    """Handle bad request error"""
    return jsonify({
        "error": "Bad request",
        "message": str(e)
    }), 400

# Global recognizer instance
recognizer = None
attendance_file = "attendance.csv"
attendance_lock = threading.Lock()


def init_recognizer():
    """Initialize the face recognizer with known faces."""
    global recognizer
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "..", "backend")
        models_dir = os.path.join(backend_dir, "resorces")
        known_faces_dir = os.path.join(backend_dir, "known_faces")

        recognizer = create_direct_recognizer(models_dir, known_faces_dir)
        logger.info("Face recognizer initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize recognizer: {e}")
        raise


def init_attendance_file():
    """Initialize attendance CSV file with headers if it doesn't exist."""
    if not os.path.exists(attendance_file):
        with open(attendance_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Timestamp", "Confidence"])
        logger.info(f"Created attendance file: {attendance_file}")


def log_attendance(name, confidence):
    """Log attendance to CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with attendance_lock:
        with open(attendance_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, timestamp, f"{confidence:.4f}"])

    logger.info(
        f"Logged attendance: {name} at {timestamp} (confidence: {confidence:.4f})"
    )


def decode_image(image_data):
    """Decode image from various formats (base64, file upload, etc.)"""
    try:
        if isinstance(image_data, str):
            # Handle data URL format (data:image/jpeg;base64,...)
            if image_data.startswith("data:image"):
                # Split and get base64 part
                try:
                    header, base64_data = image_data.split(",", 1)
                    logger.debug(f"Data URL header: {header}")
                except ValueError:
                    logger.error("Invalid data URL format")
                    return None
            else:
                base64_data = image_data
            
            # Decode base64
            try:
                # Remove any whitespace/newlines
                base64_data = base64_data.strip()
                image_bytes = base64.b64decode(base64_data)
                logger.debug(f"Decoded image size: {len(image_bytes)} bytes")
            except Exception as e:
                logger.error(f"Base64 decode error: {e}")
                return None
            
            # Create PIL Image from bytes
            try:
                image = Image.open(io.BytesIO(image_bytes))
                logger.debug(f"PIL Image created: {image.size}, mode: {image.mode}")
            except Exception as e:
                logger.error(f"PIL Image creation error: {e}")
                return None
                
        else:
            # Handle file upload
            image = Image.open(image_data)

        # Ensure RGB mode
        if image.mode != "RGB":
            logger.debug(f"Converting from {image.mode} to RGB")
            image = image.convert("RGB")

        # Convert to numpy array (required by dlib)
        image_array = np.array(image)
        logger.debug(f"NumPy array shape: {image_array.shape}, dtype: {image_array.dtype}")
        
        # Validate image dimensions
        if len(image_array.shape) != 3 or image_array.shape[2] != 3:
            logger.error(f"Invalid image shape: {image_array.shape}")
            return None
            
        return image_array

    except Exception as e:
        logger.error(f"Error decoding image: {e}")
        import traceback
        logger.debug(f"Traceback: {traceback.format_exc()}")
        return None


@app.route("/")
def index():
    """Serve the main attendance interface."""
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "recognizer_loaded": recognizer is not None,
            "known_faces": len(recognizer.known_encodings) if recognizer else 0,
            "attendance_file": os.path.exists(attendance_file),
        }
    )


@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    # Update known faces gauge
    if recognizer:
        KNOWN_FACES_GAUGE.set(len(recognizer.known_encodings))
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.route("/recognize", methods=["POST"])
def recognize_face():
    """Face recognition endpoint with automatic attendance logging."""
    try:
        if recognizer is None:
            return jsonify({"error": "Recognizer not initialized"}), 500

        image = None

        # Handle file upload
        if "image" in request.files:
            file = request.files["image"]
            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400
            image = decode_image(file)

        # Handle JSON with base64 image
        elif request.is_json:
            data = request.get_json()
            if "image" not in data:
                return jsonify({"error": "No image data provided"}), 400
            image = decode_image(data["image"])

        else:
            return jsonify({"error": "Invalid request format"}), 400

        if image is None:
            return jsonify({"error": "Failed to decode image"}), 400

        # Resize image for performance (macOS M2 optimization)
        height, width = image.shape[:2]
        if width > 640:
            scale = 640 / width
            new_width = 640
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))

        # Get recognition threshold
        threshold = float(request.args.get("threshold", 0.6))

        # Recognize face using direct dlib approach
        result = recognizer.recognize_face(image, tolerance=threshold)
        
        # Add timestamp and threshold info
        result["timestamp"] = datetime.now().isoformat()
        result["threshold"] = threshold

        # Update Prometheus metrics
        if result.get("face_detected"):
            if result.get("name"):
                FACE_RECOGNITION_COUNT.labels(result='recognized').inc()
                FACE_RECOGNITION_CONFIDENCE.observe(result.get("confidence", 0))
                ATTENDANCE_COUNT.inc()
            else:
                FACE_RECOGNITION_COUNT.labels(result='unknown').inc()
        else:
            FACE_RECOGNITION_COUNT.labels(result='no_face').inc()

        # Log attendance if person is recognized
        if result.get("face_detected") and result.get("name"):
            log_attendance(result["name"], result["confidence"])
            result["attendance_logged"] = True
        else:
            result["attendance_logged"] = False

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in recognize endpoint: {e}")
        return jsonify({"error": f"Recognition failed: {str(e)}"}), 500


@app.route("/known_faces", methods=["GET"])
def get_known_faces():
    """Get list of known faces."""
    try:
        if recognizer is None:
            return jsonify({"error": "Recognizer not initialized"}), 500

        faces = {
            name: len(encodings)
            for name, encodings in recognizer.known_encodings.items()
        }

        return jsonify(
            {
                "known_faces": faces,
                "total_people": len(faces),
                "total_encodings": sum(faces.values()),
            }
        )

    except Exception as e:
        logger.error(f"Error getting known faces: {e}")
        return jsonify({"error": f"Failed to get known faces: {str(e)}"}), 500


@app.route("/attendance", methods=["GET"])
def get_attendance():
    """Get attendance records."""
    try:
        if not os.path.exists(attendance_file):
            return jsonify({"attendance": [], "total_records": 0})

        records = []
        with open(attendance_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)

        # Get optional filters
        name_filter = request.args.get("name")
        date_filter = request.args.get("date")  # YYYY-MM-DD format

        if name_filter:
            records = [r for r in records if name_filter.lower() in r["Name"].lower()]

        if date_filter:
            records = [r for r in records if r["Timestamp"].startswith(date_filter)]

        return jsonify({"attendance": records, "total_records": len(records)})

    except Exception as e:
        logger.error(f"Error getting attendance: {e}")
        return jsonify({"error": f"Failed to get attendance: {str(e)}"}), 500


@app.route("/register_person", methods=["POST"])
def register_person():
    """Register a new person using direct dlib approach - simplified and reliable"""
    try:
        logger.info(f"Register person request received. Content-Type: {request.content_type}")
        logger.info(f"Request content length: {request.content_length}")
        
        if recognizer is None:
            return jsonify({"error": "Recognizer not initialized"}), 500

        if not request.is_json:
            logger.error(f"Invalid content type: {request.content_type}")
            return jsonify({"error": "JSON request required"}), 400

        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "No JSON data received"}), 400
            
        person_name = data.get("name")
        images_data = data.get("images", [])
        
        logger.info(f"Registration request for: {person_name}, {len(images_data)} images")
        
        if not person_name or not person_name.strip():
            logger.error("Person name is required")
            return jsonify({"error": "Person name is required"}), 400
            
        if not images_data:
            logger.error("At least one image is required")
            return jsonify({"error": "At least one image is required"}), 400

        # Use direct dlib registration
        result = recognizer.register_person_direct(person_name.strip(), images_data)
        
        if result["success"]:
            logger.info(f"Successfully registered: {person_name}")
            return jsonify(result), 200
        else:
            logger.error(f"Registration failed: {result.get('error')}")
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error registering person: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")

@app.route("/reload", methods=["POST"])
def reload_faces():
    """Reload known faces from the filesystem."""
    try:
        if recognizer is None:
            return jsonify({"error": "Recognizer not initialized"}), 500

        recognizer.load_known_faces()

        return jsonify(
            {
                "message": "Known faces reloaded successfully",
                "known_faces": len(recognizer.known_encodings),
            }
        )

    except Exception as e:
        logger.error(f"Error reloading faces: {e}")
        return jsonify({"error": f"Failed to reload faces: {str(e)}"}), 500


@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve static files."""
    return send_from_directory("static", filename)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Initialize systems
    init_recognizer()
    init_attendance_file()

    # Get configuration from environment
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    logger.info(f"Starting Face Recognition Attendance System on {host}:{port}")
    logger.info(f"Debug mode: {debug}")

    # Run Flask app
    app.run(host=host, port=port, debug=debug, threaded=True)
