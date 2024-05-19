ACTIVE_STATUS_CHOICES = (
    (0, 'Inactive'),
    (1, 'Active')
)

USER_TYPE_CHOICES = [
    ('vendor', 'Vendor'),
    ('administrator', 'Administrator'),
]

CHECKLIST_TYPE_CHOICE = [
    ('common', 'Common'),
    ('raw', 'Raw'),
    ('finish', 'Finish')
]

STORAGE_TYPE_CHOICE = [
    ('cold_storage', 'Cold Storage'),
    ('regular', 'Regular')
]

APPROVAL_STATUS_CHOICE = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

RECEIVED_ORDER_STATUS_CHOICE = [
    ('pending', 'Pending'),
    ('quarantine', 'Quarantine'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

PURPOSE_CHOICE = [
    ('regular', 'Regular'),
]

RETURN_TYPE_CHOICE = [
    ('material', 'Material'),
    ('order', 'Order'),
]

RETURN_STATUS_CHOICE = [
    ('pending', 'Pending'),
    ('returned', 'Returned'),
]
