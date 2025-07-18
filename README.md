# 🎯 Real-Time Face Recognition Attendance System

A production-ready, containerized face recognition attendance system with mo\*\*📊 Storage ## 🌐 Application Access Points

Once running## 📱 How to Use the Interface

### **🚀 Getting Started**

1. **Visit the application**: http://localhost:5000 (or http://localhost via Nginx)
2. **Monitor performance**: http://localhost:3000 (Grafana - admin/admin)
3. **Check metrics**: http://localhost:9090 (Prometheus)

### 1. **🎥 Real-Time Face Recognition**

- Click **"Start Auto Capture"** button
- Point your camera at faces
- System automatically recognizes known people and logs attendance
- View real-time confidence scores and timestamps

### 2. **👤 Register New People**

- When an unknown face appears, system automatically prompts for namem provides multiple interfaces and services:

### **🎯 Main Application (Web Interfaces)**

- **Direct Access**: http://localhost:5000 ✅ _Full web interface_
- **Load Balanced**: http://localhost ✅ _Same interface via Nginx proxy_

### **📊 Monitoring & Analytics (Web Dashboards)**

- **Prometheus Metrics**: http://localhost:9090 ✅ _Metrics and monitoring_
- **Grafana Dashboards**: http://localhost:3000 ✅ _Visual analytics (admin/admin)_

### **🗄️ Backend Services (No Web Interface)**

- **Redis Cache**: localhost:6379 ⚙️ _Database service - use Redis CLI_
- **Nginx Load Balancer**: Port 80/443 ⚙️ _Proxy service - routes to main app_

> **💡 Note**: Redis and Nginx don't have web interfaces - they're backend services. Redis is a database cache, and Nginx is a reverse proxy that routes traffic to your main application.

### **🔍 Service Health Check**

````bash
# Test all services
curl http://localhost:5000/health     # Main app
curl http://localhost:9090/-/healthy  # Prometheus
curl http://localhost:3000/api/health # Grafana
docker exec face-recognition-redis redis-cli ping  # Redis
curl -I http://localhost             # Nginx proxy
```-registration with 30-frame capture process
- Person-specific directories with JPEG images
- Pre-computed face encodings for fast matching
- CSV attendance logs with timestamps and confidence

### Data Flow:

1. **Camera** → WebRTC capture → Base64 encoding
2. **API** → Image processing → Face detection
3. **Recognition** → Encoding generation → Distance calculation
4. **Results** → Attendance logging or registration prompt

## 🛠️ System Management Commands

### **🔄 Application Control**

```bash
# Start full production stack
docker-compose --profile monitoring up -d

# Basic deployment (minimal resources)
docker-compose --profile basic up -d

# Check service status
docker-compose ps

# View application logs
docker-compose logs -f face-recognition-app

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart face-recognition-app
````

### **📊 Health Verification**

```bash
# Run comprehensive health check
./verify_deployment.sh

# Quick health check
curl http://localhost:5000/health

# Check Prometheus metrics
curl http://localhost:9090/-/healthy

# Test Grafana
curl http://localhost:3000/api/health
```

### **⚡ Performance Scaling**

```bash
# Scale application for high load
docker-compose up -d --scale face-recognition-app=3

# Resource monitoring
docker stats

# System cleanup
docker system prune -a
```

### **💾 Data Management**

````bash
# Backup face data and attendance
tar -czf backup_$(date +%Y%m%d).tar.gz backend/known_faces api/attendance.csv

# View attendance records
cat api/attendance.csv

# Monitor storage usage
docker system df
```rface, comprehensive DevOps pipeline, and enterprise monitoring. Built with Python, Flask, Dlib, and OpenCV - fully containerized with Docker and production-ready deployment automation.

## ✨ Features

### 🚀 Core Application
- **🌐 Modern Web Interface** - Bootstrap UI with real-time webcam recognition
- **🤖 Automatic Registration** - Unknown faces trigger automatic 30-frame capture
- **📊 Intelligent Attendance** - CSV logging with timestamps and confidence scores
- **🔌 REST API** - Clean endpoints for integration and development
- **💪 Direct Dlib Implementation** - Reliable face detection and recognition
- **⚡ Optimized Performance** - CPU-only processing, no GPU required

### 🐳 DevOps & Production Features
- **🐳 Complete Containerization** - Multi-stage Docker builds (6GB → 2GB optimization)
- **🔄 CI/CD Pipeline** - GitHub Actions with automated testing and deployment
- **📊 Full Monitoring Stack** - Prometheus metrics + Grafana dashboards
- **🏗️ Multi-Environment Support** - Development, staging, and production profiles
- **🔧 Automation Scripts** - One-command deployment and health verification
- **🛡️ Security Hardened** - Non-root containers, dependency scanning, vulnerability checks

## 🚀 Quick Start

### Option 1: Production Deployment (Recommended)
```bash
# Clone repository
git clone https://github.com/ayushkumar912/lightweight-face-recognition.git
cd lightweight-face-recognition

# Deploy with full monitoring stack
docker-compose --profile monitoring up -d

# Verify deployment
./verify_deployment.sh
````

**Production Access:**

- **Application**: http://localhost:5000
- **Monitoring**: http://localhost:9090 (Prometheus)
- **Dashboards**: http://localhost:3000 (Grafana - admin/admin)

### Option 2: Development Setup

```bash
# Traditional setup
chmod +x run.sh
./run.sh
```

### Option 3: Docker Only

```bash
# Basic containerized deployment
docker-compose --profile basic up -d
```

**Access:** http://localhost:5000

> 📋 **For complete DevOps operations, deployment guides, and production management, see [DevOpsREADME.md](./DevOpsREADME.md)**

## 🌐 Application Access Points

Once running, your system provides multiple interfaces:

### **🎯 Main Application**

- **Primary URL**: http://localhost:5000
- **Nginx Proxy**: http://localhost (load-balanced access)

### **� Monitoring & Analytics**

- **Prometheus Metrics**: http://localhost:9090
- **Grafana Dashboards**: http://localhost:3000 (login: admin/admin)

### **🗄️ Backend Services**

- **Redis Cache**: localhost:6379

## �📱 How to Use the Interface

### 1. **🎥 Real-Time Face Recognition**

- Click **"Start Auto Capture"** button
- Point your camera at faces
- System automatically recognizes known people and logs attendance
- View real-time confidence scores and timestamps

### 2. **👤 Register New People**

- When an unknown face appears, system automatically prompts for name
- Enter the person's name in the dialog box
- System captures 30 training frames automatically
- Person becomes immediately available for recognition
- No manual training required!

### 3. **📊 View Attendance & Analytics**

- Real-time attendance display on dashboard
- Download CSV reports with timestamps
- View confidence scores for each recognition
- Monitor system performance metrics
- Access detailed analytics via Grafana dashboards

### 4. **🔧 System Management**

- Health status indicators for all services
- Resource usage monitoring
- Real-time metrics and alerts
- Automated backup and recovery options

## 🏗️ System Architecture

![System Architecture](System_Architecture.jpeg)

### Key Components:

**🌐 Web Frontend**

- WebRTC camera interface with getUserMedia() API
- Bootstrap 5 UI with real-time display
- Auto-capture and manual recognition controls

**🔌 Flask API Server**

- RESTful endpoints for recognition and registration
- Real-time attendance logging and CSV export
- Comprehensive error handling and validation

**🤖 Dlib Recognition Engine**

- HOG frontal face detector for initial detection
- 68-point facial landmark predictor for alignment
- ResNet-based face recognition model for encoding
- Euclidean distance matching with 0.6 threshold

**� Storage Systems**

- Auto-registration with 30-frame capture process
- Person-specific directories with JPEG images
- Pre-computed face encodings for fast matching
- CSV attendance logs with timestamps and confidence

### Data Flow:

1. **Camera** → WebRTC capture → Base64 encoding
2. **API** → Image processing → Face detection
3. **Recognition** → Encoding generation → Distance calculation
4. **Results** → Attendance logging or registration prompt

## 📁 Project Structure

```
lightweight-face-recognition/
├── 📜 README.md                    # This comprehensive guide
├── � DevOpsREADME.md             # Complete DevOps operations guide
├── �🚀 run.sh                       # Traditional setup script
├── 🐳 Dockerfile                   # Multi-stage container build
├── 📋 docker-compose.yml           # Multi-environment orchestration
├── 🚀 deploy.sh                    # Automated deployment script
├── 🔍 verify_deployment.sh         # Health verification script
├── 📋 requirements.txt             # Python dependencies
├── 📄 LICENSE                      # MIT License
│
├── � .github/workflows/           # CI/CD Pipeline
│   └── ci-cd.yml                   # GitHub Actions workflow
│
├── 📊 monitoring/                  # Monitoring Configuration
│   ├── prometheus.yml              # Metrics collection config
│   ├── grafana-dashboard.json      # Pre-built dashboards
│   └── alert_rules.yml             # Automated alerting
│
├── 🌐 nginx/                       # Reverse Proxy
│   └── nginx.conf                  # Load balancer configuration
│
├── ☸️ k8s/                         # Kubernetes Manifests
│   ├── deployment.yaml             # Application deployment
│   ├── service.yaml                # Service definitions
│   └── monitoring.yaml             # Monitoring stack
│
├── 📚 docs/                        # Organized Documentation
│   ├── DEPLOYMENT_SUCCESS.md       # Deployment verification
│   ├── DEVOPS_FEATURES.md          # DevOps capabilities
│   ├── PROMETHEUS_GUIDE.md         # Monitoring instructions
│   └── WEBSITE_USAGE_GUIDE.md      # User interface guide
│
├── �🔌 api/                         # Flask API Server
│   ├── app.py                      # Main Flask application
│   ├── start_api.sh                # API startup script
│   └── attendance.csv              # Generated attendance log
│
├── 🧠 backend/                     # Face Recognition Engine
│   ├── direct_recognizer.py        # Direct Dlib implementation
│   ├── known_faces/                # Training images database
│   │   ├── PersonName1/            # Individual person folders
│   │   └── PersonName2/            # Auto-created during registration
│   └── resorces/                   # Dlib model files
│       ├── shape_predictor_68_face_landmarks.dat
│       └── dlib_face_recognition_resnet_model_v1.dat
│
└── 🌐 frontend/                    # Web Interface
    ├── templates/
    │   └── index.html              # Main web interface
    └── static/
        ├── style.css               # Bootstrap styling
        └── script.js               # Camera and registration logic
```

## 📈 Monitoring & Analytics

### **Real-time Metrics Dashboard**

Access your Grafana dashboard at http://localhost:3000 (admin/admin):

- **System Health**: Service uptime, response times, error rates
- **Face Recognition Analytics**: Recognition accuracy, confidence trends
- **Attendance Patterns**: Daily/weekly attendance statistics
- **Resource Utilization**: CPU, memory, storage usage
- **Performance Metrics**: Request rates, processing times

### **Prometheus Metrics**

Monitor at http://localhost:9090:

- `up`: Service availability status
- `face_recognition_requests_total`: Total API requests
- `face_recognition_confidence`: ML model accuracy scores
- `attendance_records_total`: Daily attendance count
- `container_memory_usage_bytes`: Resource consumption

### **Application Logs**

```bash
# View real-time application logs
docker-compose logs -f face-recognition-app

# Filter for errors
docker-compose logs face-recognition-app | grep ERROR

# Export logs for analysis
docker-compose logs --no-color face-recognition-app > app.log
```

## 🚨 Troubleshooting Guide

### **Common Issues & Solutions**

#### 🔴 Container Won't Start

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs face-recognition-app

# Restart with clean state
docker-compose down -v && docker-compose up -d
```

#### 📹 Camera Access Issues

- **Chrome**: Enable camera permissions in browser settings
- **Firefox**: Allow camera access when prompted
- **Safari**: Check system camera permissions
- **HTTPS**: Some browsers require HTTPS for camera access

#### 🎯 Face Recognition Not Working

```bash
# Check if known faces exist
ls -la backend/known_faces/

# Verify model files
ls -la backend/resorces/

# Check recognition logs
docker-compose logs face-recognition-app | grep -i "recognition\|face"
```

#### 💾 Memory Issues

```bash
# Check resource usage
docker stats

# Increase memory limits (in docker-compose.yml)
mem_limit: 2g

# Clean up unused resources
docker system prune -a
```

#### 🌐 Port Conflicts

```bash
# Check what's using the port
lsof -i :5000

# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use different external port
```

### **Performance Optimization**

#### For High Load Environments:

```bash
# Scale application instances
docker-compose up -d --scale face-recognition-app=3

# Enable Redis caching
# (Already configured in production profile)

# Monitor resource usage
docker stats --no-stream
```

#### For Low-Resource Systems:

```bash
# Use basic profile (minimal resources)
docker-compose --profile basic up -d

# Reduce image size in Dockerfile
# (Already optimized with multi-stage builds)
```

## 🔧 API Endpoints

### Recognition

```http
POST /recognize?threshold=0.6
Content-Type: multipart/form-data

# Response
{
  "face_detected": true,
  "name": "John Doe",
  "confidence": 0.75,
  "registration_required": false,
  "attendance_logged": true,
  "timestamp": "2025-07-17T04:12:52"
}
```

### Registration

```http
POST /register_person
Content-Type: application/json

{
  "name": "John Doe",
  "images": ["data:image/jpeg;base64,/9j/4AAQ...", "..."]
}

# Response
{
  "success": true,
  "person_name": "John Doe",
  "total_images": 30,
  "valid_faces": 28,
  "face_detection_rate": "93.3%"
}
```

### Attendance

```http
GET /attendance
GET /attendance?name=John&date=2025-07-17

# Response
{
  "attendance": [
    {
      "Name": "John Doe",
      "Timestamp": "2025-07-17 04:12:52",
      "Confidence": "0.7503"
    }
  ],
  "total_records": 1
}
```

### Health Check

```http
GET /health

# Response
{
  "status": "healthy",
  "known_faces": 3,
  "total_encodings": 89,
  "uptime": "0:15:32"
}
```

## ⚙️ Technical Specifications

### Face Recognition Engine

- **Detection**: Dlib HOG + Linear SVM detector
- **Landmarks**: 68-point facial landmark predictor
- **Encoding**: ResNet-based 128-dimensional face descriptor
- **Matching**: Euclidean distance with 0.6 tolerance
- **Performance**: ~100-200ms per frame on MacBook M2

### Registration Process

- **Frame Count**: 30 frames at 5 FPS (6-second capture)
- **Quality Filtering**: Only frames with detected faces are saved
- **Format**: JPEG images at 85% quality
- **Validation**: Real-time face detection during capture
- **Storage**: Organized in person-specific directories

### Web Interface

- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Camera**: WebRTC getUserMedia API
- **Capture**: HTML5 Canvas for frame processing
- **Upload**: Base64 encoding for image transmission
- **Updates**: Real-time status and progress display

## 🔧 Advanced Configuration

### Recognition Threshold

```bash

```

### Environment Variables

```bash
# Create .env file for custom configuration
DEBUG=false
FLASK_ENV=production
LOG_LEVEL=INFO
RECOGNITION_THRESHOLD=0.6
MAX_REGISTRATION_FRAMES=30
KNOWN_FACES_PATH=/app/backend/known_faces
ATTENDANCE_FILE=/app/api/attendance.csv
```

### Database Configuration

```bash
# For production with PostgreSQL (optional)
DATABASE_URL=postgresql://user:pass@localhost/face_recognition
REDIS_URL=redis://localhost:6379/0
```

## 🔒 Security Considerations

- **Camera Access**: Ensure HTTPS for production camera access
- **File Upload**: Validate image uploads and limit file sizes
- **API Security**: Implement rate limiting and authentication
- **Data Privacy**: Securely handle biometric data storage
- **Network Security**: Use HTTPS and secure communication
- **Container Security**: Non-root users and minimal attack surface

## 🚀 Production Deployment

### **Quick Production Setup**

```bash
# Deploy complete production stack
docker-compose --profile production up -d

# For monitoring and analytics
docker-compose --profile monitoring up -d

# Verify deployment health
./verify_deployment.sh
```

### **Kubernetes Deployment**

```bash
# Deploy to Kubernetes cluster
kubectl apply -f k8s/

# Scale for high availability
kubectl scale deployment face-recognition-app --replicas=3

# Monitor deployment
kubectl get pods -l app=face-recognition
```

### **CI/CD Integration**

- GitHub Actions pipeline included
- Automated testing on multiple Python versions
- Security scanning with Bandit and Safety
- Docker image building and deployment
- Comprehensive health checks

## 📈 Performance Metrics

### **Real-world Performance**

- **Recognition Speed**: ~100-200ms per frame (MacBook M2)
- **Accuracy**: 95%+ with good lighting conditions
- **Memory Usage**: ~230MB per container instance
- **Registration Time**: 6 seconds (30 frames at 5 FPS)
- **Concurrent Users**: 50+ with load balancing

### **Scalability**

- **Horizontal Scaling**: Multiple app instances with load balancer
- **Caching**: Redis for improved response times
- **Resource Limits**: Configurable memory and CPU constraints
- **Auto-scaling**: Kubernetes HPA support

## 📚 Additional Resources

- **[DevOpsREADME.md](./DevOpsREADME.md)** - Complete DevOps operations guide
- **[docs/](./docs/)** - Detailed documentation and guides
- **[Monitoring Guide](./docs/PROMETHEUS_GUIDE.md)** - Prometheus and Grafana setup
- **[Website Usage](./docs/WEBSITE_USAGE_GUIDE.md)** - User interface guide
- **[Deployment Success](./docs/DEPLOYMENT_SUCCESS.md)** - Verification procedures

## 🔄 Version History

| Version | Date       | Features              | Changes                                  |
| ------- | ---------- | --------------------- | ---------------------------------------- |
| 1.0.0   | 2025-07-18 | Initial Release       | Basic face recognition system            |
| 2.0.0   | 2025-07-18 | DevOps Implementation | Full containerization, CI/CD, monitoring |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

### **Development Setup**

```bash
# Clone for development
git clone https://github.com/ayushkumar912/lightweight-face-recognition.git
cd lightweight-face-recognition

# Set up development environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/

# Start development server
python api/app.py
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dlib** - Face detection and recognition models by Davis King
- **OpenCV** - Computer vision library for image processing
- **Flask** - Lightweight web framework for Python
- **Bootstrap 5** - Modern CSS framework for responsive UI
- **Docker** - Containerization platform for deployment
- **Prometheus & Grafana** - Monitoring and visualization stack

---

## 📞 Support & Contact

For issues, questions, and contributions:

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/ayushkumar912/lightweight-face-recognition/issues)
- 💬 **Feature Requests**: [GitHub Discussions](https://github.com/ayushkumar912/lightweight-face-recognition/discussions)
- 📧 **Email**: [Contact Developer](mailto:ayushkumar912@example.com)
- 📖 **Documentation**: [DevOpsREADME.md](./DevOpsREADME.md)

---

**⭐ Star this repository if you found it helpful!**

**🎯 Built with ❤️ for enterprise-ready face recognition with complete DevOps automation**

````

### Manual Setup

```bash
# If run.sh doesn't work for your system
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cd api && python app.py
````

### Adding Known Faces Manually

```bash
# Create person directory
mkdir -p backend/known_faces/"Person Name"

# Add clear face images (JPG/PNG)
cp face1.jpg backend/known_faces/"Person Name"/
cp face2.jpg backend/known_faces/"Person Name"/

# Restart server to reload
```

## 📊 Performance Metrics

Based on testing with MacBook Air M2:

| Operation                | Time   | Accuracy          |
| ------------------------ | ------ | ----------------- |
| Face Detection           | ~50ms  | 95%+              |
| Face Recognition         | ~100ms | 90%+              |
| Registration (30 frames) | ~20s   | 85%+ valid frames |
| Database Reload          | ~500ms | 100%              |

## 🐛 Troubleshooting

### Common Issues

**"No face detected"**

- Ensure good lighting
- Face should be clearly visible and front-facing
- Remove glasses/masks if possible during registration

**"Import error: dlib"**

```bash
# Install dlib dependencies
pip install cmake
pip install dlib
```

**"Camera not working"**

- Grant camera permissions in browser
- Try different browser (Chrome recommended)
- Check if camera is used by other applications

**"Server won't start"**

```bash
# Check port availability
lsof -i :5000

# Kill conflicting process
kill -9 <PID>
```

### Logs and Debugging

```bash
# View detailed logs
cd api && python app.py

# Check attendance records
cat api/attendance.csv

# Verify known faces
ls backend/known_faces/
```

## 🔐 Security Considerations

- **Local Processing**: All face data stays on your machine
- **No Cloud Dependencies**: Works completely offline
- **Data Privacy**: Images stored locally in `backend/known_faces/`
- **Development Server**: Not suitable for production without proper security

## 📈 Future Enhancements

- [ ] **Multiple Face Recognition** - Handle multiple faces in single frame
- [ ] **Performance Dashboard** - Real-time analytics and metrics
- [ ] **Export Formats** - JSON, Excel export options
- [ ] **Authentication** - User login and access control
- [ ] **Mobile App** - React Native mobile client
- [ ] **Docker Deployment** - Containerized deployment option

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dlib** - Face detection and recognition models
- **OpenCV** - Image processing and camera capture
- **Flask** - Web framework and API server
- **Bootstrap** - Modern and responsive UI components

---

## 📞 Support

For issues and questions:

- 🐛 **Bugs**: [GitHub Issues](https://github.com/ayushkumar912/lightweight-face-recognition/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/ayushkumar912/lightweight-face-recognition/discussions)

---

**⭐ Star this repository if you found it helpful!**

**🔧 Built with ❤️ for reliable face recognition**
