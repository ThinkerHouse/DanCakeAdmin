def get_updated_by(instance):
    updated_by = instance.updated_by
    if updated_by:
        return {
            'id': updated_by.id,
            'username': updated_by.username
        }
    return None

def get_created_by(instance):
    created_by = instance.created_by
    if created_by:
        return {
            'id': created_by.id,
            'username': created_by.username
        }
    return None

def get_approved_by(instance):
    approved_by = instance.approved_by
    if approved_by:
        return {
            'id': approved_by.id,
            'username': approved_by.username
        }
    return None

def get_production_plant(instance):
    production_plant = instance.production_plant
    if production_plant:
        return {
            'id': production_plant.id,
            'name': production_plant.name
        }
    return None

def get_unit(instance):
    unit = instance.unit
    if unit:
        return {
            'id': unit.id,
            'name': unit.name
        }
    return None

def get_product(instance):
    product = instance.product
    if product:
        return {
            'id': product.id,
            'name': product.name
        }
    return None