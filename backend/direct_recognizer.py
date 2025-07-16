"""
Direct Dlib Face Recognition Implementation
Simple and efficient face detection and registration
"""

import dlib
import cv2
import numpy as np
import os
import logging
from PIL import Image
import io
import base64
from datetime import datetime

logger = logging.getLogger(__name__)

class DirectDlibRecognizer:
    def __init__(self, models_dir, known_faces_dir):
        """Initialize the direct dlib recognizer"""
        self.models_dir = models_dir
        self.known_faces_dir = known_faces_dir
        
        # Load dlib models
        predictor_path = os.path.join(models_dir, "shape_predictor_68_face_landmarks.dat")
        face_rec_model_path = os.path.join(models_dir, "dlib_face_recognition_resnet_model_v1.dat")
        
        if not os.path.exists(predictor_path):
            raise FileNotFoundError(f"Shape predictor not found: {predictor_path}")
        if not os.path.exists(face_rec_model_path):
            raise FileNotFoundError(f"Face recognition model not found: {face_rec_model_path}")
            
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)
        self.face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
        
        logger.info("Direct Dlib models loaded successfully")
        
        # Load known faces
        self.known_encodings = {}
        self.load_known_faces()
        
    def get_face_encoding(self, image):
        """Get face encoding from image using dlib"""
        try:
            # Ensure image is in the right format
            if len(image.shape) == 3 and image.shape[2] == 3:
                # RGB image - convert to grayscale for detection
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
                
            # Detect faces
            faces = self.detector(gray, 1)
            
            if len(faces) == 0:
                return None
                
            # Use the first detected face
            face = faces[0]
            
            # Get facial landmarks
            landmarks = self.predictor(gray, face)
            
            # Get face encoding
            face_encoding = self.face_rec_model.compute_face_descriptor(image, landmarks)
            
            return np.array(face_encoding)
            
        except Exception as e:
            logger.error(f"Error getting face encoding: {e}")
            return None
    
    def load_known_faces(self):
        """Load all known faces from directory"""
        self.known_encodings = {}
        
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir, exist_ok=True)
            logger.info("Created known_faces directory")
            return
        
        total_encodings = 0
        
        for person_name in os.listdir(self.known_faces_dir):
            person_dir = os.path.join(self.known_faces_dir, person_name)
            
            if not os.path.isdir(person_dir):
                continue
                
            person_encodings = []
            
            for filename in os.listdir(person_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(person_dir, filename)
                    
                    try:
                        # Load image
                        image = cv2.imread(img_path)
                        if image is None:
                            logger.warning(f"Could not load image: {img_path}")
                            continue
                            
                        # Convert BGR to RGB
                        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                        # Get encoding
                        encoding = self.get_face_encoding(image_rgb)
                        
                        if encoding is not None:
                            person_encodings.append(encoding)
                            total_encodings += 1
                        else:
                            logger.warning(f"No face detected in {img_path}")
                            
                    except Exception as e:
                        logger.error(f"Error processing {img_path}: {e}")
            
            if person_encodings:
                self.known_encodings[person_name] = person_encodings
                logger.info(f"Loaded {len(person_encodings)} encodings for {person_name}")
        
        logger.info(f"Total known faces loaded: {len(self.known_encodings)} people with {total_encodings} encodings")
    
    def recognize_face(self, image, tolerance=0.6):
        """Recognize face in image"""
        try:
            # Get encoding for unknown face
            unknown_encoding = self.get_face_encoding(image)
            
            if unknown_encoding is None:
                return {
                    "face_detected": False,
                    "name": None,
                    "confidence": 0.0,
                    "registration_required": False
                }
            
            # Check against known faces
            best_match = None
            best_distance = float('inf')
            
            for name, encodings in self.known_encodings.items():
                for known_encoding in encodings:
                    # Calculate distance
                    distance = np.linalg.norm(known_encoding - unknown_encoding)
                    
                    if distance < tolerance and distance < best_distance:
                        best_distance = distance
                        best_match = name
            
            if best_match:
                confidence = max(0.0, 1.0 - (best_distance / tolerance))
                return {
                    "face_detected": True,
                    "name": best_match,
                    "confidence": confidence,
                    "distance": best_distance,
                    "registration_required": False
                }
            else:
                # Unknown face - registration required
                return {
                    "face_detected": True,
                    "name": None,
                    "confidence": 0.0,
                    "registration_required": True,
                    "message": "Unknown face detected"
                }
                
        except Exception as e:
            logger.error(f"Error in face recognition: {e}")
            return {
                "face_detected": False,
                "name": None,
                "confidence": 0.0,
                "error": str(e),
                "registration_required": False
            }
    
    def register_person_direct(self, person_name, images):
        """Register a person directly using dlib approach"""
        try:
            # Clean person name
            import re
            person_name = re.sub(r'[<>:"/\\|?*]', '', person_name).strip()
            
            if not person_name:
                return {"success": False, "error": "Invalid person name"}
            
            # Create person directory
            person_dir = os.path.join(self.known_faces_dir, person_name)
            
            if os.path.exists(person_dir):
                return {"success": False, "error": f"Person '{person_name}' already exists"}
            
            os.makedirs(person_dir, exist_ok=True)
            
            # Process and save images
            saved_count = 0
            valid_faces = 0
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for i, image_data in enumerate(images):
                try:
                    # Decode image
                    if isinstance(image_data, str):
                        if image_data.startswith("data:image"):
                            image_data = image_data.split(",")[1]
                        image_bytes = base64.b64decode(image_data)
                        image_pil = Image.open(io.BytesIO(image_bytes))
                        image_array = np.array(image_pil.convert('RGB'))
                    else:
                        continue
                    
                    # Check if face is detected
                    encoding = self.get_face_encoding(image_array)
                    
                    if encoding is not None:
                        # Save image
                        filename = f"{person_name}_{timestamp}_{i+1:02d}.jpg"
                        img_path = os.path.join(person_dir, filename)
                        
                        # Convert RGB to BGR for cv2
                        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                        cv2.imwrite(img_path, image_bgr)
                        
                        saved_count += 1
                        valid_faces += 1
                        
                        logger.info(f"Saved valid face image: {filename}")
                    else:
                        logger.warning(f"No face detected in image {i+1}")
                        
                except Exception as e:
                    logger.error(f"Error processing image {i+1}: {e}")
                    continue
            
            if valid_faces == 0:
                # Remove empty directory
                import shutil
                shutil.rmtree(person_dir)
                return {
                    "success": False, 
                    "error": "No valid faces detected in any image"
                }
            
            # Reload known faces to include new person
            self.load_known_faces()
            
            return {
                "success": True,
                "message": f"Person '{person_name}' registered successfully",
                "person_name": person_name,
                "total_images": len(images),
                "valid_faces": valid_faces,
                "face_detection_rate": f"{(valid_faces/len(images)*100):.1f}%"
            }
            
        except Exception as e:
            logger.error(f"Error registering person: {e}")
            return {"success": False, "error": str(e)}


def create_direct_recognizer(models_dir, known_faces_dir):
    """Create and return a direct dlib recognizer instance"""
    try:
        recognizer = DirectDlibRecognizer(models_dir, known_faces_dir)
        return recognizer
    except Exception as e:
        logger.error(f"Failed to create direct recognizer: {e}")
        return None
