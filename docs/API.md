# API Contracts (MVP)
`POST /api/patients/` — create patient  
`GET /api/patients?query=` — search patients  
`POST /api/orders/` — create order for patient  
`GET /api/orders/:id` — fetch order with items

All endpoints: JSON, consistent error envelope `{error: {code, message, details}}`.
