/**
 * Real-time Face Recognition Attendance System - Frontend JavaScript
 * Handles webcam capture, automatic recognition, and UI updates
 */

class AttendanceSystem {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.isCapturing = false;
        this.captureInterval = null;
        this.threshold = 0.6;
        this.interval = 5; // seconds
        
        this.initializeElements();
        this.initializeCamera();
        this.checkSystemHealth();
        this.loadRecentAttendance();
        this.setupEventListeners();
    }

    initializeElements() {
        // Get DOM elements
        this.toggleBtn = document.getElementById('toggleCapture');
        this.manualBtn = document.getElementById('manualCapture');
        this.statusDiv = document.getElementById('status');
        this.resultDiv = document.getElementById('result');
        this.thresholdSlider = document.getElementById('threshold');
        this.intervalSlider = document.getElementById('captureInterval');
        this.thresholdValue = document.getElementById('thresholdValue');
        this.intervalValue = document.getElementById('intervalValue');
        this.systemStatus = document.getElementById('systemStatus');
        this.recentAttendance = document.getElementById('recentAttendance');
        this.refreshBtn = document.getElementById('refreshAttendance');
    }

    setupEventListeners() {
        // Toggle auto capture
        this.toggleBtn.addEventListener('click', () => {
            this.toggleAutoCapture();
        });

        // Manual capture
        this.manualBtn.addEventListener('click', () => {
            this.captureAndRecognize();
        });

        // Threshold slider
        this.thresholdSlider.addEventListener('input', (e) => {
            this.threshold = parseFloat(e.target.value);
            this.thresholdValue.textContent = this.threshold;
        });

        // Interval slider
        this.intervalSlider.addEventListener('input', (e) => {
            this.interval = parseInt(e.target.value);
            this.intervalValue.textContent = this.interval;
            
            // Restart auto capture if active
            if (this.isCapturing) {
                this.stopAutoCapture();
                this.startAutoCapture();
            }
        });

        // Refresh attendance
        this.refreshBtn.addEventListener('click', () => {
            this.loadRecentAttendance();
        });
    }

    async initializeCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    width: 640, 
                    height: 480,
                    facingMode: 'user'
                }
            });
            
            this.video.srcObject = stream;
            this.updateStatus('Camera initialized successfully', 'success');
            
            // Enable buttons once camera is ready
            this.video.addEventListener('loadeddata', () => {
                this.toggleBtn.disabled = false;
                this.manualBtn.disabled = false;
            });
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            this.updateStatus('Failed to access camera. Please check permissions.', 'danger');
        }
    }

    async checkSystemHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.updateSystemStatus(data);
            } else {
                throw new Error('System not healthy');
            }
        } catch (error) {
            console.error('Health check failed:', error);
            this.systemStatus.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle"></i>
                    System health check failed
                </div>
            `;
        }
    }

    updateSystemStatus(data) {
        this.systemStatus.innerHTML = `
            <div class="row text-center">
                <div class="col-6">
                    <div class="badge bg-success mb-2 w-100">Status</div>
                    <div class="h6">${data.status}</div>
                </div>
                <div class="col-6">
                    <div class="badge bg-info mb-2 w-100">Known Faces</div>
                    <div class="h6">${data.known_faces}</div>
                </div>
            </div>
            <div class="row text-center mt-2">
                <div class="col-6">
                    <div class="badge bg-primary mb-2 w-100">Recognizer</div>
                    <div class="h6">${data.recognizer_loaded ? '✓ Loaded' : '✗ Failed'}</div>
                </div>
                <div class="col-6">
                    <div class="badge bg-warning mb-2 w-100">Attendance</div>
                    <div class="h6">${data.attendance_file ? '✓ Ready' : '✗ Error'}</div>
                </div>
            </div>
        `;
    }

    async loadRecentAttendance() {
        try {
            const response = await fetch('/attendance');
            const data = await response.json();
            
            if (data.attendance.length === 0) {
                this.recentAttendance.innerHTML = '<p class="text-muted text-center">No attendance records yet</p>';
                return;
            }

            // Show last 5 records
            const recent = data.attendance.slice(-5).reverse();
            
            this.recentAttendance.innerHTML = recent.map(record => `
                <div class="border-bottom pb-2 mb-2">
                    <div class="fw-bold">${record.Name}</div>
                    <small class="text-muted">${new Date(record.Timestamp).toLocaleString()}</small>
                    <div class="badge bg-success ms-2">${(parseFloat(record.Confidence) * 100).toFixed(1)}%</div>
                </div>
            `).join('');
            
        } catch (error) {
            console.error('Failed to load attendance:', error);
            this.recentAttendance.innerHTML = '<p class="text-danger text-center">Failed to load attendance</p>';
        }
    }

    toggleAutoCapture() {
        if (this.isCapturing) {
            this.stopAutoCapture();
        } else {
            this.startAutoCapture();
        }
    }

    startAutoCapture() {
        this.isCapturing = true;
        this.toggleBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Auto Capture';
        this.toggleBtn.className = 'btn btn-danger btn-lg me-2';
        
        this.updateStatus(`Auto capture started (every ${this.interval}s)`, 'info');
        
        // Start immediate capture
        this.captureAndRecognize();
        
        // Set up interval
        this.captureInterval = setInterval(() => {
            this.captureAndRecognize();
        }, this.interval * 1000);
    }

    stopAutoCapture() {
        this.isCapturing = false;
        this.toggleBtn.innerHTML = '<i class="fas fa-play"></i> Start Auto Capture';
        this.toggleBtn.className = 'btn btn-success btn-lg me-2';
        
        if (this.captureInterval) {
            clearInterval(this.captureInterval);
            this.captureInterval = null;
        }
        
        this.updateStatus('Auto capture stopped', 'warning');
    }

    async captureAndRecognize() {
        try {
            // Draw video frame to canvas
            this.ctx.drawImage(this.video, 0, 0, 640, 480);
            
            // Convert to blob
            const blob = await new Promise(resolve => {
                this.canvas.toBlob(resolve, 'image/jpeg', 0.8);
            });
            
            // Send to API
            const formData = new FormData();
            formData.append('image', blob, 'capture.jpg');
            
            this.updateStatus('Processing image...', 'info');
            
            const response = await fetch(`/recognize?threshold=${this.threshold}`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.displayResult(result);
                
                // Refresh attendance if someone was recognized
                if (result.attendance_logged) {
                    setTimeout(() => this.loadRecentAttendance(), 1000);
                }
            } else {
                throw new Error(result.error || 'Recognition failed');
            }
            
        } catch (error) {
            console.error('Capture failed:', error);
            this.updateStatus(`Error: ${error.message}`, 'danger');
        }
    }

    displayResult(result) {
        if (result.registration_required) {
            // Unknown face or no face detected - start frame capture process
            this.startFrameCapture(result);
        } else if (result.face_detected && result.name) {
            // Known person recognized
            this.updateStatus(`✓ ${result.name} recognized`, 'success');
            
            this.resultDiv.style.display = 'block';
            this.resultDiv.className = 'mt-3';
            this.resultDiv.innerHTML = `
                <div class="alert alert-success" role="alert">
                    <h5 class="alert-heading">✅ Attendance Logged</h5>
                    <p class="mb-1"><strong>Name:</strong> ${result.name}</p>
                    <p class="mb-1"><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%</p>
                    <p class="mb-0"><strong>Time:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
                </div>
            `;
        } else {
            // Fallback for other cases
            this.updateStatus('Recognition completed', 'info');
            this.resultDiv.style.display = 'none';
        }
    }

    async startFrameCapture(recognitionResult) {
        // Stop auto capture if running
        const wasAutoCapturing = this.isCapturing;
        if (this.isCapturing) {
            this.stopAutoCapture();
        }

        // Show confirmation dialog first
        const shouldRegister = confirm(
            recognitionResult.registration_message + 
            "\n\nThis will capture 30 training images for better accuracy."
        );

        if (!shouldRegister) {
            // Resume auto capture if it was running
            if (wasAutoCapturing) {
                this.startAutoCapture();
            }
            return;
        }

        // Get person name
        const personName = prompt("Enter the person's name:");
        if (!personName || !personName.trim()) {
            // Resume auto capture if it was running
            if (wasAutoCapturing) {
                this.startAutoCapture();
            }
            return;
        }

        // Start frame capture process
        this.updateStatus('📸 Capturing training images... Please stay still', 'info');
        
        const capturedFrames = [];
        const totalFrames = 30;
        const captureInterval = 200; // 200ms between captures (5 fps)

        // Update UI to show progress
        this.resultDiv.style.display = 'block';
        this.resultDiv.className = 'mt-3';
        
        for (let i = 0; i < totalFrames; i++) {
            try {
                // Update progress
                this.resultDiv.innerHTML = `
                    <div class="alert alert-info" role="alert">
                        <h5 class="alert-heading">📸 Capturing Training Images</h5>
                        <div class="progress mb-2">
                            <div class="progress-bar progress-bar-striped progress-bar-animated" 
                                 style="width: ${((i + 1) / totalFrames * 100)}%">
                                ${i + 1}/${totalFrames}
                            </div>
                        </div>
                        <p class="mb-0">Please stay still and look at the camera</p>
                    </div>
                `;

                // Capture frame
                this.ctx.drawImage(this.video, 0, 0, 640, 480);
                const blob = await new Promise(resolve => {
                    this.canvas.toBlob(resolve, 'image/jpeg', 0.85);
                });

                if (!blob) {
                    console.warn(`Failed to create blob for frame ${i + 1}`);
                    continue;
                }

                // Convert to base64
                const base64 = await this.blobToBase64(blob);
                if (!base64 || base64.length < 100) {
                    console.warn(`Invalid base64 for frame ${i + 1}: ${base64 ? base64.length : 'null'} chars`);
                    continue;
                }

                capturedFrames.push(base64);
                console.log(`Frame ${i + 1} captured: ${base64.length} chars`);

                // Wait before next capture
                if (i < totalFrames - 1) {
                    await new Promise(resolve => setTimeout(resolve, captureInterval));
                }

            } catch (error) {
                console.error(`Error capturing frame ${i + 1}:`, error);
                // Continue with next frame instead of failing completely
            }
        }

        if (capturedFrames.length === 0) {
            throw new Error('No frames were captured successfully');
        }

        console.log(`Successfully captured ${capturedFrames.length}/${totalFrames} frames`);

        // Send registration request
        this.updateStatus('🔄 Processing images and registering person...', 'info');
        
        try {
            await this.registerPersonWithFrames(personName.trim(), capturedFrames);
        } catch (error) {
            console.error('Registration failed:', error);
            this.updateStatus(`❌ Registration failed: ${error.message}`, 'danger');
        }

        // Resume auto capture if it was running
        if (wasAutoCapturing) {
            setTimeout(() => {
                this.startAutoCapture();
            }, 3000); // Wait 3 seconds before resuming
        }
    }

    async blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    async registerPersonWithFrames(personName, frames) {
        const registerBtn = document.getElementById('manualCapture');
        const originalText = registerBtn.textContent;
        
        try {
            // Show loading state on manual capture button
            registerBtn.disabled = true;
            registerBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Registering...';
            
            // Validate frames before sending
            if (!frames || frames.length === 0) {
                throw new Error('No frames to register');
            }

            // Calculate total payload size
            const totalSize = JSON.stringify({name: personName, images: frames}).length;
            console.log(`Registration payload size: ${(totalSize / 1024 / 1024).toFixed(2)} MB`);

            if (totalSize > 50 * 1024 * 1024) { // 50MB limit
                throw new Error('Payload too large. Please try with fewer frames.');
            }
            
            // Prepare data for registration
            const registrationData = {
                name: personName,
                images: frames
            };
            
            console.log(`Sending registration for ${personName} with ${frames.length} images`);
            
            // Send registration request
            const response = await fetch('/register_person', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(registrationData)
            });
            
            // Get response text first to debug JSON parsing issues
            const responseText = await response.text();
            console.log('Registration response status:', response.status);
            console.log('Registration response headers:', response.headers.get('content-type'));
            console.log('Registration response text:', responseText);
            
            let result;
            try {
                result = JSON.parse(responseText);
            } catch (jsonError) {
                console.error('JSON parsing error:', jsonError);
                console.error('Response status:', response.status);
                console.error('Response content-type:', response.headers.get('content-type'));
                console.error('Response text (first 200 chars):', responseText.substring(0, 200));
                
                // Show user-friendly error
                throw new Error(`Server returned invalid response. Status: ${response.status}. Content: ${responseText.substring(0, 100)}...`);
            }
            
            if (response.ok && result.success) {
                // Registration successful
                this.updateStatus(`✅ ${personName} registered successfully!`, 'success');
                
                // Update system status to reflect new face count
                this.checkSystemHealth();
                
                // Show success message with details
                this.resultDiv.style.display = 'block';
                this.resultDiv.className = 'mt-3';
                this.resultDiv.innerHTML = `
                    <div class="alert alert-success" role="alert">
                        <h5 class="alert-heading">🎉 Registration Successful!</h5>
                        <p class="mb-1"><strong>Name:</strong> ${result.person_name}</p>
                        <p class="mb-1"><strong>Training Images:</strong> ${result.total_images}</p>
                        <p class="mb-1"><strong>Valid Faces:</strong> ${result.valid_faces}</p>
                        <p class="mb-0"><strong>Success Rate:</strong> ${result.face_detection_rate}</p>
                    </div>
                `;
                
                // Try recognition again after a short delay to verify registration
                setTimeout(() => {
                    this.captureAndRecognize();
                }, 2000);
                
            } else {
                // Registration failed
                throw new Error(result.error || result.warning || 'Unknown error');
            }
            
        } finally {
            // Restore button state
            registerBtn.disabled = false;
            registerBtn.textContent = originalText;
        }
    }

    updateStatus(message, type = 'info') {
        const alertClass = `alert-${type}`;
        this.statusDiv.innerHTML = `
            <div class="alert ${alertClass}" role="alert">
                <i class="fas fa-info-circle"></i>
                ${message}
            </div>
        `;
    }
}

// Global variable to store the attendance system instance
let attendanceSystem;

// Initialize the system when the page loads
document.addEventListener('DOMContentLoaded', () => {
    attendanceSystem = new AttendanceSystem();
});
