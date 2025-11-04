# VPS IP Verification & Credentials Documentation

## VPS IP Address: 172.235.33.181

This document verifies that the VPS IP has been added to all required configuration files and provides all credentials for the application.

---

## ✅ VPS IP Configuration Verification

### 1. Backend Django Settings (`backend/core/settings.py`)

**ALLOWED_HOSTS Configuration:**
```python
# Line 34-42
ALLOWED_HOSTS = (
    os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,172.235.33.181").split(",")
    if os.environ.get("ALLOWED_HOSTS")
    else [
        "localhost",
        "127.0.0.1",
        "172.235.33.181",  # ✅ VPS IP ADDED
    ]
)
```

**CORS_ALLOWED_ORIGINS Configuration:**
```python
# Line 207-213
_cors_origins = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://172.235.33.181,http://172.235.33.181:80",  # ✅ VPS IP ADDED
)
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in _cors_origins.split(",") if origin.strip()
]
```

**Status:** ✅ VPS IP configured in both ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS with environment variable fallback

---

### 2. Backend Environment Template (`backend/.env.example`)

```bash
# Line 4
ALLOWED_HOSTS=172.235.33.181,localhost,127.0.0.1  # ✅ VPS IP ADDED

# Line 7
CORS_ALLOWED_ORIGINS=http://172.235.33.181,http://172.235.33.181:80,http://localhost:5173,http://localhost:3000  # ✅ VPS IP ADDED
```

**Status:** ✅ VPS IP included in environment template for production deployment

---

### 3. Nginx Configuration (`nginx/nginx.conf`)

```nginx
# Line 32
server_name 172.235.33.181 localhost;  # ✅ VPS IP ADDED
```

**Status:** ✅ VPS IP configured as server_name in nginx

---

### 4. Docker Compose (`docker-compose.yml`)

```yaml
# Lines 43-44
environment:
  ALLOWED_HOSTS: ${ALLOWED_HOSTS:-172.235.33.181,localhost,127.0.0.1}  # ✅ VPS IP ADDED
  CORS_ALLOWED_ORIGINS: ${CORS_ALLOWED_ORIGINS:-http://172.235.33.181,http://172.235.33.181:80,http://localhost}  # ✅ VPS IP ADDED
```

**Status:** ✅ VPS IP configured in docker-compose environment defaults

---

### 5. Frontend Environment Template (`frontend/.env.example`)

```bash
# For production VPS deployment - use relative path since nginx proxies /api/ to backend
VITE_API_URL=/api

# For direct backend access (if not using nginx proxy)
# VITE_API_URL=http://172.235.33.181:8000  # ✅ VPS IP DOCUMENTED
```

**Status:** ✅ VPS IP documented as alternative configuration option

---

### 6. Verification Script (`verify-deployment.sh`)

```bash
# Multiple references to VPS IP for testing:
# Line 8: echo "VPS: 172.235.33.181"
# Lines checking VPS IP in configuration and testing endpoints
```

**Status:** ✅ VPS IP used in automated verification checks

---

## 🔑 Application Credentials

### Backend Superuser & User Credentials

The seed data command creates default users for testing and development. **⚠️ CHANGE THESE IN PRODUCTION!**

#### Superuser / Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@alshifa.com`
- **Role:** ADMIN (Full access to all features)
- **Permissions:** Full system access, user management, all CRUD operations

#### Reception User
- **Username:** `reception`
- **Password:** `reception123`
- **Email:** `reception@alshifa.com`
- **Role:** RECEPTION
- **Permissions:** Patient registration, order creation, report viewing

#### Technologist User
- **Username:** `tech`
- **Password:** `tech123`
- **Email:** `tech@alshifa.com`
- **Role:** TECHNOLOGIST
- **Permissions:** Sample receiving, result entry, worklist view

#### Pathologist User
- **Username:** `pathologist`
- **Password:** `path123`
- **Email:** `path@alshifa.com`
- **Role:** PATHOLOGIST
- **Permissions:** Result verification, result publishing, report generation

---

### Frontend Access

The frontend does not have separate credentials. Users log in through the frontend using the backend credentials listed above.

**Frontend URL:** `http://172.235.33.181/`

**Login Process:**
1. Navigate to `http://172.235.33.181/` or `http://172.235.33.181/login`
2. Enter username and password from the backend credentials
3. System will authenticate via JWT tokens
4. Access is role-based (see permissions above)

---

### Database Credentials

**Development/Seed Data:**
- **Host:** `db` (Docker service name)
- **Port:** `5432`
- **Database:** `lims`
- **Username:** `lims`
- **Password:** `lims` (for development)

**Production (from backend/.env.example):**
- **Host:** `db`
- **Port:** `5432`
- **Database:** `lims`
- **Username:** `lims`
- **Password:** `REPLACE-WITH-SECURE-DATABASE-PASSWORD` ⚠️ **MUST BE CHANGED**

---

### Django Configuration Secrets

**Django Secret Key:**
- **Current (development):** `django-insecure-ipmf8j^_92@tw&q8t9%f599m-yp)f%g*aeyl1d^5bwf#p+_v_^`
- **Production (backend/.env.example):** `REPLACE-WITH-SECURE-SECRET-KEY-BEFORE-DEPLOYMENT` ⚠️ **MUST BE CHANGED**

**Generate New Secret Key:**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

### Redis Configuration

- **URL:** `redis://redis:6379/0`
- **No authentication required** (internal Docker network only)

---

## 🔒 Security Recommendations

### ⚠️ CRITICAL - Before Production Deployment

1. **Change Django Secret Key**
   ```bash
   # Generate a new key
   python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   
   # Update in backend/.env
   DJANGO_SECRET_KEY=<generated-key>
   ```

2. **Change Database Password**
   ```bash
   # Generate a strong password
   openssl rand -base64 32
   
   # Update in backend/.env
   POSTGRES_PASSWORD=<generated-password>
   ```

3. **Change All Default User Passwords**
   - After deployment, login to Django admin at `http://172.235.33.181/admin/`
   - Navigate to Users
   - Change passwords for all users (admin, reception, tech, pathologist)
   - **OR** Delete seed users and create new ones with secure passwords

4. **Set DEBUG to False**
   ```bash
   # In backend/.env
   DEBUG=False
   ```

5. **Configure Firewall**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```

---

## 📋 Access Points Summary

| Service | URL | Credentials Required |
|---------|-----|---------------------|
| **Frontend** | http://172.235.33.181/ | Backend user credentials |
| **Backend API** | http://172.235.33.181/api/ | JWT token (from login) |
| **Health Check** | http://172.235.33.181/api/health/ | No auth required |
| **Django Admin** | http://172.235.33.181/admin/ | Superuser (admin/admin123) |
| **API Docs** | See docs/API.md | Various endpoints require auth |

---

## 🧪 Testing Credentials

After deployment, test the application with these credentials:

1. **Admin Testing:**
   - Login with `admin` / `admin123`
   - Full access to all features
   - Can manage users, view all data

2. **Reception Testing:**
   - Login with `reception` / `reception123`
   - Can register patients, create orders
   - Cannot access lab workflow

3. **Technologist Testing:**
   - Login with `tech` / `tech123`
   - Can receive samples, enter results
   - Cannot verify or publish results

4. **Pathologist Testing:**
   - Login with `pathologist` / `path123`
   - Can verify results, publish reports
   - Full lab workflow access

---

## 📝 Post-Deployment Checklist

- [ ] VPS IP verified in all configuration files ✅
- [ ] Backend superuser credentials documented ✅
- [ ] Frontend access method documented ✅
- [ ] Database credentials documented ✅
- [ ] Security recommendations provided ✅
- [ ] Change Django SECRET_KEY before production ⚠️
- [ ] Change POSTGRES_PASSWORD before production ⚠️
- [ ] Change default user passwords after deployment ⚠️
- [ ] Set DEBUG=False in production ⚠️
- [ ] Configure firewall on VPS ⚠️
- [ ] Test all access points after deployment ⚠️

---

## 📞 Support

For issues or questions:
- **Repository:** https://github.com/munaimtahir/lab
- **Owner:** @munaimtahir
- **Deployment Guide:** README-DEPLOY.md
- **Implementation Summary:** DEPLOYMENT-SUMMARY.md

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-04  
**VPS IP:** 172.235.33.181  
**Status:** ✅ Verified - All configurations include VPS IP
