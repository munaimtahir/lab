# Data Model (Initial)
- Patient(id, mrn, full_name, father_name, dob, sex, phone, cnic, address, created_at, updated_at)
- Order(id, patient_id, order_no, priority, status, created_at)
- OrderItem(id, order_id, test_code, test_name, status)
- Sample(id, order_item_id, sample_type, barcode, collected_at, received_at, status)
- Result(id, order_item_id, value, unit, reference_range, flags, status, verified_by, verified_at, published_at)
- User(id, email, role, is_active, ...)

Statuses are defined as enums; transitions are validated by a state machine.
