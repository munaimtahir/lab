#!/bin/bash
# Deployment Verification Script for VPS 172.235.33.181
# This script validates that all services are properly configured and running

set -e

echo "=========================================="
echo "Al Shifa LIMS - Deployment Verification"
echo "VPS: 172.235.33.181"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ERRORS=0
WARNINGS=0

# Function to print success
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print error
error() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

# Function to print warning
warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "1. Checking Prerequisites..."
echo "----------------------------"

# Check Docker
if command_exists docker; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
    success "Docker installed (version $DOCKER_VERSION)"
else
    error "Docker is not installed"
fi

# Check Docker Compose
if command_exists docker-compose || docker compose version >/dev/null 2>&1; then
    if command_exists docker-compose; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f4 | cut -d',' -f1)
    else
        COMPOSE_VERSION=$(docker compose version --short)
    fi
    success "Docker Compose installed (version $COMPOSE_VERSION)"
else
    error "Docker Compose is not installed"
fi

# Check Git
if command_exists git; then
    success "Git installed"
else
    warning "Git is not installed (needed for updates)"
fi

echo ""
echo "2. Checking Configuration Files..."
echo "-----------------------------------"

# Check if backend/.env exists
if [ -f "backend/.env" ]; then
    success "backend/.env exists"
    
    # Check critical environment variables
    if grep -q "DJANGO_SECRET_KEY=REPLACE-WITH-SECURE-SECRET-KEY-BEFORE-DEPLOYMENT" backend/.env; then
        error "DJANGO_SECRET_KEY is still set to default placeholder value!"
    else
        success "DJANGO_SECRET_KEY has been changed"
    fi
    
    if grep -q "POSTGRES_PASSWORD=REPLACE-WITH-SECURE-DATABASE-PASSWORD" backend/.env; then
        error "POSTGRES_PASSWORD is still set to default placeholder value!"
    else
        success "POSTGRES_PASSWORD has been changed"
    fi
    
    if grep -q "DEBUG=True" backend/.env; then
        warning "DEBUG is set to True (should be False for production)"
    else
        success "DEBUG is set to False"
    fi
    
    if grep -q "172.235.33.181" backend/.env; then
        success "VPS IP configured in backend/.env"
    else
        warning "VPS IP not found in backend/.env"
    fi
else
    error "backend/.env does not exist (copy from backend/.env.example)"
fi

# Check Docker files
if [ -f "backend/Dockerfile" ]; then
    success "backend/Dockerfile exists"
else
    error "backend/Dockerfile is missing"
fi

if [ -f "nginx/Dockerfile" ]; then
    success "nginx/Dockerfile exists"
else
    error "nginx/Dockerfile is missing"
fi

if [ -f "docker-compose.yml" ]; then
    success "docker-compose.yml exists"
else
    error "docker-compose.yml is missing"
fi

if [ -f "nginx/nginx.conf" ]; then
    success "nginx/nginx.conf exists"
    
    # Check if VPS IP is in nginx config
    if grep -q "172.235.33.181" nginx/nginx.conf; then
        success "VPS IP configured in nginx.conf"
    else
        warning "VPS IP not found in nginx.conf"
    fi
else
    error "nginx/nginx.conf is missing"
fi

echo ""
echo "3. Checking Docker Services..."
echo "-------------------------------"

# Check if services are running
if docker compose ps >/dev/null 2>&1 || docker-compose ps >/dev/null 2>&1; then
    # Use docker compose or docker-compose depending on what's available
    if command_exists docker-compose; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi
    
    # Check each service
    for service in backend db redis nginx; do
        if $COMPOSE_CMD ps | grep -q "$service.*Up"; then
            success "$service is running"
        else
            error "$service is not running"
        fi
    done
else
    warning "No Docker services running (run 'docker compose up -d' first)"
fi

echo ""
echo "4. Testing Service Health..."
echo "-----------------------------"

# Wait a moment for services to be ready
sleep 2

# Test backend health endpoint (internal)
if docker compose ps backend 2>/dev/null | grep -q "Up"; then
    if docker compose exec -T backend curl -sf http://localhost:8000/api/health/ >/dev/null 2>&1; then
        success "Backend health check passed (internal)"
    else
        error "Backend health check failed (internal)"
    fi
fi

# Test nginx serving (internal)
if docker compose ps nginx 2>/dev/null | grep -q "Up"; then
    if docker compose exec -T nginx wget --quiet --tries=1 --spider http://localhost/ 2>/dev/null; then
        success "Nginx is serving content (internal)"
    else
        error "Nginx is not serving content (internal)"
    fi
fi

# Test external access (requires host network access)
if command_exists curl; then
    echo ""
    echo "5. Testing External Access..."
    echo "------------------------------"
    
    # Test frontend
    if curl -sf http://172.235.33.181/ >/dev/null 2>&1; then
        success "Frontend accessible at http://172.235.33.181/"
    else
        warning "Frontend not accessible from this host (may require network routing)"
    fi
    
    # Test backend API
    if curl -sf http://172.235.33.181/api/health/ >/dev/null 2>&1; then
        success "Backend API accessible at http://172.235.33.181/api/health/"
        
        # Show health response
        HEALTH_RESPONSE=$(curl -s http://172.235.33.181/api/health/)
        echo "   Health response: $HEALTH_RESPONSE"
    else
        warning "Backend API not accessible from this host (may require network routing)"
    fi
fi

echo ""
echo "6. Checking Logs for Errors..."
echo "--------------------------------"

# Check for common errors in logs
if docker compose ps >/dev/null 2>&1; then
    # Check backend logs for DisallowedHost errors
    if docker compose logs backend 2>/dev/null | grep -q "DisallowedHost"; then
        error "DisallowedHost errors found in backend logs"
    else
        success "No DisallowedHost errors in backend logs"
    fi
    
    # Check backend logs for CORS errors
    if docker compose logs backend 2>/dev/null | grep -qi "cors.*error\|origin.*blocked"; then
        warning "Possible CORS errors found in backend logs"
    else
        success "No CORS errors in backend logs"
    fi
    
    # Check nginx logs for errors (excluding 404s)
    NGINX_ERRORS=$(docker compose logs nginx 2>/dev/null | grep -i "error" | grep -iv "404" | wc -l)
    if [ "$NGINX_ERRORS" -gt 0 ]; then
        warning "Errors found in nginx logs (check with: docker compose logs nginx)"
    else
        success "No critical errors in nginx logs"
    fi
fi

echo ""
echo "7. Checking Network Configuration..."
echo "--------------------------------------"

# Check if ports are listening
if command_exists netstat || command_exists ss; then
    if netstat -tuln 2>/dev/null | grep -q ":80 " || ss -tuln 2>/dev/null | grep -q ":80 "; then
        success "Port 80 is listening"
    else
        error "Port 80 is not listening"
    fi
    
    if netstat -tuln 2>/dev/null | grep -q ":443 " || ss -tuln 2>/dev/null | grep -q ":443 "; then
        success "Port 443 is listening (HTTPS ready)"
    else
        warning "Port 443 is not listening (HTTPS not configured)"
    fi
else
    warning "Cannot check port status (netstat/ss not available)"
fi

# Check firewall status (if ufw is available)
if command_exists ufw; then
    if ufw status | grep -q "80.*ALLOW"; then
        success "Firewall allows port 80"
    else
        warning "Firewall may block port 80 (check with: sudo ufw status)"
    fi
fi

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Deployment is ready.${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Deployment is running but has $WARNINGS warning(s).${NC}"
    exit 0
else
    echo -e "${RED}✗ Deployment has $ERRORS error(s) and $WARNINGS warning(s).${NC}"
    echo ""
    echo "Please fix the errors and run this script again."
    echo "For detailed logs, use: docker compose logs -f"
    exit 1
fi
