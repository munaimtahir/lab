# Add the IP to ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '172.235.33.181',       # VPS IP added
    '.yourdomain.com',      # existing domain(s)
]

# If using django-cors-headers:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://172.235.33.181",      # Add VPS IP (frontend origin)
    "https://yourdomain.com",
] 
# Or for older versions:
# CORS_ORIGIN_WHITELIST = ("http://172.235.33.181",)