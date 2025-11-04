# Quick Reference Card - VPS Deployment

## 🌐 VPS Information
- **IP Address:** `172.235.33.181`
- **Access URL:** http://172.235.33.181/

## 🔑 Default Credentials (⚠️ CHANGE IN PRODUCTION!)

### Backend Users
```
Admin:        admin       / admin123        (Full access)
Reception:    reception   / reception123    (Patient & Orders)
Technologist: tech        / tech123         (Lab work)
Pathologist:  pathologist / path123         (Verification & Reports)
```

### Database
```
Host:     db (Docker service)
Port:     5432
Database: lims
User:     lims
Password: lims (dev) or CHANGE-ME (production)
```

## 🚀 Quick Deploy Commands

```bash
# 1. Clone and setup
git clone https://github.com/munaimtahir/lab.git && cd lab
cp backend/.env.example backend/.env

# 2. Generate secrets
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
openssl rand -base64 32

# 3. Update backend/.env with generated secrets

# 4. Deploy
docker compose build && docker compose up -d

# 5. Verify
./verify-deployment.sh
```

## 🔗 Access Points

| Service | URL |
|---------|-----|
| Frontend | http://172.235.33.181/ |
| API | http://172.235.33.181/api/ |
| Admin | http://172.235.33.181/admin/ |
| Health | http://172.235.33.181/api/health/ |

## ✅ VPS IP Location Check

- [x] `backend/core/settings.py` → ALLOWED_HOSTS
- [x] `backend/core/settings.py` → CORS_ALLOWED_ORIGINS
- [x] `backend/.env.example` → ALLOWED_HOSTS
- [x] `backend/.env.example` → CORS_ALLOWED_ORIGINS
- [x] `nginx/nginx.conf` → server_name
- [x] `docker-compose.yml` → environment defaults
- [x] `frontend/.env.example` → documented alternative
- [x] `verify-deployment.sh` → test scripts

## ⚠️ Security To-Do Before Production

1. [ ] Change DJANGO_SECRET_KEY in backend/.env
2. [ ] Change POSTGRES_PASSWORD in backend/.env
3. [ ] Set DEBUG=False in backend/.env
4. [ ] Change all user passwords after deployment
5. [ ] Configure firewall (allow 80, 443, 22)

## 📚 Full Documentation

- **Credentials:** VPS-IP-CREDENTIALS.md
- **Deployment:** README-DEPLOY.md
- **Summary:** DEPLOYMENT-SUMMARY.md
- **Verification:** Run `./verify-deployment.sh`

---
**Generated:** 2025-11-04 | **Status:** ✅ All VPS IP configurations verified
