#!/bin/bash

# 🚀 Face Recognition System Setup & Launch Script

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 Face Recognition System Setup & Launch${NC}"
echo "=============================================="
echo ""

# Check if we're in the correct directory
if [[ ! -f "README.md" ]] || [[ ! -d "api" ]] || [[ ! -d "backend" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    echo "Expected structure: README.md, api/, backend/, frontend/"
    exit 1
fi

echo -e "${BLUE}📁 Working Directory:${NC} $(pwd)"
echo ""

# Step 1: Check Python installation
echo -e "${BLUE}🐍 Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Step 2: Create virtual environment if it doesn't exist
echo -e "${BLUE}🔧 Setting up virtual environment...${NC}"
if [[ ! -d ".venv" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Step 3: Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Step 4: Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
if [[ -f "requirements.txt" ]]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi
echo ""

# Step 5: Verify dlib models
echo -e "${BLUE}🤖 Checking dlib models...${NC}"
MODEL_DIR="backend/resorces"
SHAPE_PREDICTOR="$MODEL_DIR/shape_predictor_68_face_landmarks.dat"
FACE_RECOGNITION_MODEL="$MODEL_DIR/dlib_face_recognition_resnet_model_v1.dat"

if [[ ! -f "$SHAPE_PREDICTOR" ]]; then
    echo -e "${RED}❌ Missing: $SHAPE_PREDICTOR${NC}"
    echo "Please download the dlib models and place them in backend/resorces/"
    exit 1
fi

if [[ ! -f "$FACE_RECOGNITION_MODEL" ]]; then
    echo -e "${RED}❌ Missing: $FACE_RECOGNITION_MODEL${NC}"
    echo "Please download the dlib models and place them in backend/resorces/"
    exit 1
fi

echo -e "${GREEN}✅ Dlib models found${NC}"
echo ""

# Step 6: Create necessary directories
echo -e "${BLUE}📂 Creating directories...${NC}"
mkdir -p backend/known_faces
mkdir -p api
echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# Step 7: Initialize attendance file
echo -e "${BLUE}📊 Setting up attendance tracking...${NC}"
if [[ ! -f "api/attendance.csv" ]]; then
    echo "Name,Timestamp,Confidence" > api/attendance.csv
    echo -e "${GREEN}✅ Attendance file initialized${NC}"
else
    echo -e "${GREEN}✅ Attendance file already exists${NC}"
fi
echo ""

# Step 8: Test imports
echo -e "${BLUE}🧪 Testing Python imports...${NC}"
python3 -c "
import dlib
import cv2
import numpy as np
import flask
print('✅ All required packages imported successfully')
" || {
    echo -e "${RED}❌ Import test failed. Please check your installation.${NC}"
    exit 1
}
echo ""

# Step 9: Start the application
echo -e "${BLUE}🌐 Starting Face Recognition API Server...${NC}"
echo ""
echo -e "  📍 API Server: ${GREEN}http://127.0.0.1:5000${NC}"
echo -e "  🔧 Health Check: ${GREEN}http://127.0.0.1:5000/health${NC}"
echo -e "  📊 Attendance: ${GREEN}http://127.0.0.1:5000/attendance${NC}"
echo ""
echo -e "${YELLOW}⚠️  Press Ctrl+C to stop the server${NC}"
echo ""

# Change to api directory and start the server
cd api
python app.py
