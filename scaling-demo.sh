#!/bin/bash

# 🚀 Scaling Demonstration Script
# Shows how to scale the face recognition system

echo "🔧 Face Recognition System - Scaling Demonstration"
echo "=================================================="
echo ""

# Stop current services
echo "📋 Preparing for scaling demonstration..."
docker-compose down -q

# Create a temporary docker-compose for scaling demo
cat > docker-compose.scale-demo.yml << 'EOF'
services:
  face-recognition-app-1:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5001:5000"
    volumes:
      - known_faces_data:/app/backend/known_faces
      - attendance_data:/app/api
      - ./backend/resorces:/app/backend/resorces:ro
    environment:
      - FLASK_ENV=production
      - FLASK_APP=api/app.py
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    networks:
      - face-recognition-network

  face-recognition-app-2:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5002:5000"
    volumes:
      - known_faces_data:/app/backend/known_faces
      - attendance_data:/app/api
      - ./backend/resorces:/app/backend/resorces:ro
    environment:
      - FLASK_ENV=production
      - FLASK_APP=api/app.py
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    networks:
      - face-recognition-network

  face-recognition-app-3:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5003:5000"
    volumes:
      - known_faces_data:/app/backend/known_faces
      - attendance_data:/app/api
      - ./backend/resorces:/app/backend/resorces:ro
    environment:
      - FLASK_ENV=production
      - FLASK_APP=api/app.py
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    networks:
      - face-recognition-network

  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./scaling-nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - face-recognition-app-1
      - face-recognition-app-2
      - face-recognition-app-3
    restart: unless-stopped
    networks:
      - face-recognition-network

volumes:
  known_faces_data:
  attendance_data:

networks:
  face-recognition-network:
EOF

# Create nginx config for load balancing
cat > scaling-nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream face_recognition_backend {
        server face-recognition-app-1:5000;
        server face-recognition-app-2:5000;
        server face-recognition-app-3:5000;
    }

    server {
        listen 80;
        
        location / {
            proxy_pass http://face_recognition_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
EOF

echo "🚀 Starting 3 face recognition instances with load balancer..."
docker-compose -f docker-compose.scale-demo.yml up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 15

echo ""
echo "📊 Scaled deployment status:"
docker-compose -f docker-compose.scale-demo.yml ps

echo ""
echo "🌐 Access points:"
echo "  • Load Balanced: http://localhost (nginx distributes traffic)"
echo "  • Instance 1: http://localhost:5001"
echo "  • Instance 2: http://localhost:5002"  
echo "  • Instance 3: http://localhost:5003"

echo ""
echo "🔍 Testing load balancer distribution:"
for i in {1..6}; do
    echo -n "Request $i: "
    curl -s http://localhost/health | grep -o '"status":"[^"]*"' || echo "Connection failed"
    sleep 1
done

echo ""
echo "✅ Scaling demonstration complete!"
echo ""
echo "To return to normal deployment:"
echo "  docker-compose -f docker-compose.scale-demo.yml down"
echo "  docker-compose --profile monitoring up -d"
echo ""

read -p "Press Enter to return to normal deployment..."

# Cleanup
docker-compose -f docker-compose.scale-demo.yml down
rm -f docker-compose.scale-demo.yml scaling-nginx.conf

# Restart normal deployment
docker-compose --profile monitoring up -d

echo "🎯 Returned to normal monitoring deployment!"
