## 🌐 Face Recognition Website User Guide

### 📱 **Access Your Website**
**Main Interface:** http://localhost:5000
**Alternative:** http://localhost (via Nginx proxy)

---

### 🎯 **Step-by-Step Usage Instructions**

#### **Step 1: Open the Website**
```bash
# Open in your browser
open http://localhost:5000
# Or use the Simple Browser (already opened for you)
```

#### **Step 2: Allow Camera Access**
1. Click "Allow" when browser asks for camera permission
2. You should see your live camera feed in the video box
3. If camera doesn't work, check browser permissions

#### **Step 3: Use Face Recognition**

**🔄 Auto Capture Mode (Recommended):**
1. Click "Start Auto Capture" button (green)
2. System automatically scans for faces every 2 seconds
3. When a known face is detected, it shows:
   - Person's name
   - Confidence score (0-100%)
   - Timestamp of recognition
   - Attendance is automatically logged

**📷 Manual Capture Mode:**
1. Click "Manual Capture" button (blue)
2. Takes a single photo and analyzes it
3. Good for testing or single-shot recognition

#### **Step 4: View Results**
- **Recognition Results:** Shows name, confidence, and time
- **System Status:** Displays health and known faces count
- **Recent Attendance:** Live updates of attendance records

---

### 🎛️ **Website Features**

#### **📊 Dashboard Elements:**
1. **Live Camera Feed** - Real-time video stream
2. **Recognition Display** - Shows detected person info
3. **System Status** - Health monitoring
4. **Attendance Log** - Recent check-ins
5. **Control Buttons** - Start/stop and manual capture

#### **🔧 Technical Features:**
- **Real-time Processing** - Instant face detection
- **Automatic Logging** - Attendance saved to CSV
- **Confidence Scores** - ML model accuracy display
- **Responsive Design** - Works on mobile/desktop
- **Bootstrap UI** - Professional appearance

---

### 🧪 **Testing the Website**

#### **Test with Known Faces:**
Currently registered people:
- ✅ **Aryan** (30 face encodings)
- ✅ **Ayush Kumar** (30 face encodings) 
- ✅ **Narendra Modi** (9 face encodings)

#### **Expected Behavior:**
- **Known Person:** Shows name + high confidence (>70%)
- **Unknown Person:** Shows "Unknown" + lower confidence
- **No Face:** Shows "No face detected"
- **Poor Quality:** May show lower confidence scores

---

### 🔍 **Troubleshooting**

#### **Camera Issues:**
```bash
# Check camera permissions in browser
# Try different browsers (Chrome, Safari, Firefox)
# Restart the application if needed
docker-compose --profile monitoring restart face-recognition-app
```

#### **Recognition Issues:**
```bash
# Check system health
curl http://localhost:5000/health

# View application logs
docker-compose --profile monitoring logs face-recognition-app --tail 20

# Verify known faces loaded
# Should show 3 people with 69 total encodings
```

#### **Performance Issues:**
```bash
# Monitor system resources
docker stats face-recognition-app

# Check if all services running
docker-compose --profile monitoring ps
```

---

### 📱 **API Endpoints (Advanced)**

#### **Direct API Testing:**
```bash
# Health check
curl http://localhost:5000/health

# Get attendance records
curl http://localhost:5000/attendance

# Manual recognition (POST image)
curl -X POST -F "image=@photo.jpg" http://localhost:5000/recognize
```

---

### 🎯 **Pro Tips**

1. **Best Lighting:** Use good front lighting for better recognition
2. **Face Position:** Look directly at camera, not at angle
3. **Distance:** Stay 2-4 feet from camera for optimal results
4. **Multiple Faces:** System can detect multiple people simultaneously
5. **Confidence Threshold:** >70% is typically reliable recognition

---

### 🚀 **Next Steps**

1. **Add New People:** Add photos to `backend/known_faces/[name]/` folder
2. **Customize UI:** Modify `frontend/templates/index.html`
3. **View Analytics:** Check Grafana at http://localhost:3000
4. **Monitor System:** Use Prometheus at http://localhost:9090
5. **Scale System:** Add more camera endpoints or recognition nodes
