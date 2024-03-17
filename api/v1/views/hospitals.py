#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Hospitals """
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models.alert import Alert
from models.company import Company
from models.contact import Contact

from models.hosp_operator import Hospital
from models.location import Address
from models.system_user import HospitalStaff
from models.utils.create_table import CreateCompany
from util.create_table import CreateUser

ignore_keys = ['id', 'created_at', 'updated_at']


@app_views.route('/hospitals', methods=['GET'])
@swag_from('documentation/hospital/get_hospital.yml', methods=['GET'])
def get_hospitals():
    """Get all hospitals"""
    results = []
    data_hospitals = storage.all(Hospital)
    for obj in data_hospitals.values():
        comp = storage.get_one_by(Company, id=obj.company_id)
        obj.name = comp.name
        # fetch the company contact
        print("2. =====================")
        
        contact = storage.get_one_by(Contact, address_id=comp.address_id)
        if contact is None:
            
            # print(comp.address_id)
            obj.contact = '+2330000000000'
        else:
            obj.contact = contact.phone_number
        results.append(obj.to_dict())
    
    return jsonify(results)



@app_views.route('/hospital/<hospital_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/hospital/get_hospital_id.yml', methods=['GET'])
def get_hospital(hospital_id=None):
    """Get a hospital by id"""
    print("1. =====================")
    print(f"hospital_id: {hospital_id}")
    obj = storage.get_one_by(Hospital, id=hospital_id)
    if obj is None:
        abort(404)
    comp = storage.get_one_by(Company, id=obj.company_id)
    obj.name = comp.name
    return jsonify(obj.to_dict())

# @app_views.route('/hospital', methods=['POST'], strict_slashes=False)
# @swag_from('documentation/hospital/post_hospital.yml', methods=['POST'])
# def post_hospital():
#     """Create a new hospital"""
#     if not request.json:
#         abort(400, 'Not a JSON')
#     if 'name' not in request.json:
#         abort(400, 'Missing name')
#     if 'address_id' not in request.json:
#         abort(400, 'Missing address_id')
#     if 'company_id' not in request.json:
#         abort(400, 'Missing company_id')
#     data = request.get_json()
#     new_hospital = CreateCompany().create(Hospital, 'hospital', data)
#     return make_response(jsonify(new_hospital), 201)

# @app_views.route('/hospital/<hospital_id>', methods=['PUT'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/put_hospital_id.yml', methods=['PUT'])
# def put_hospital(hospital_id=None):
#     """Update a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     if not request.json:
#         abort(400, 'Not a JSON')
#     data = request.get_json()
#     for key, value in data.items():
#         setattr(obj, key, value)
#     obj.save()
#     return make_response(jsonify(obj.to_dict()), 200)

# @app_views.route('/hospital/<hospital_id>', methods=['DELETE'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/delete_hospital_id.yml', methods=['DELETE'])
# def delete_hospital(hospital_id=None):
#     """Delete a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     storage.delete(obj)
#     storage.save()
#     return make_response(jsonify({}), 200)

# #Get hospital status
# @app_views.route('/hospital/<hospital_id>/status', methods=['GET'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/get_hospital_id_status.yml', methods=['GET'])
# def get_hospital_status(hospital_id=None):
#     """Get hospital's status"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     comp = storage.get_one_by(Company, id=obj.company_id)
#     if comp is None:
#         abort(404)
#     return jsonify(comp.status)

# # update hospital status
# @app_views.route('/hospital/<hospital_id>/status', methods=['PUT'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/put_hospital_id_status.yml', methods=['PUT'])
# def put_hospital_status(hospital_id=None):
#     """Update hospital's status"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     if not request.json:
#         abort(400, 'Not a JSON')
#     data = request.get_json()
#     comp = storage.get_one_by(Company, id=obj.company_id)
#     if comp is None:
#         abort(404)
#     comp.status = data['status']
#     comp.save()
#     return make_response(jsonify(comp.to_dict()), 200)

# @app_views.route('/hospital/<hospital_id>/contacts', methods=['GET'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/get_hospital_id_contacts.yml', methods=['GET'])
# def get_hospital_contacts(hospital_id=None):
#     """Get hospital's contacts"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     comp = storage.get_one_by(Company, id=obj.company_id)
#     if comp is None:
#         abort(404)
#     address = storage.get_one_by(Address, id=comp.address_id)
#     if address is None:
#         abort(404)
#     contact = storage.get_one_by(Contact, id=address.contact_id)
#     cont = list({
#         'email': contact.email,
#         'phone': contact.phone_number,
#         'address': address.to_dict()
#     })
#     return jsonify(cont)

# @app_views.route('/hospital/<hospital_id>/contacts', methods=['PUT'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/put_hospital_id_contacts.yml', methods=['PUT'])
# def put_hospital_contacts(hospital_id=None):
#     """Update hospital's contacts"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     if not request.json:
#         abort(400, 'Not a JSON')
#     data = request.get_json()
#     comp = storage.get_one_by(Company, id=obj.company_id)
#     if comp is None:
#         abort(404)
#     address = storage.get_one_by(Address, id=comp.address_id)
#     if address is None:
#         abort(404)
#     contact = storage.get_one_by(Contact, id=address.contact_id)
#     if contact is None:
#         abort(404)
#     for key, value in data.items():
#         setattr(contact, key, value)
#     contact.save()
#     return make_response(jsonify(contact.to_dict()), 200)

# @app_views.route('/hospital/<hospital_id>/alerts', methods=['GET'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/get_hospital_id_alerts.yml', methods=['GET'])
# def get_hospital_alerts(hospital_id=None):
#     """Get all alerts for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     # check if there are alerts
#     if len(obj.alerts) == 0:
#         return make_response(jsonify({}), 200)
#     return jsonify([alert.to_dict() for alert in obj.alerts])

# @app_views.route('/hospital/<hospital_id>/alerts/<alert_id>', methods=['GET'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/get_hospital_id_alert_id.yml', methods=['GET'])
# def get_hospital_alert_id(hospital_id=None, alert_id=None):
#     """Get an alert for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     if alert_id not in [alert.id for alert in obj.alerts]:
#         abort(404)
#     alert = storage.get_one_by(Alert, id=alert_id)
#     if alert is None:
#         abort(404)
#     return jsonify(alert.to_dict())

# @app_views.route('/hospital/<hospital_id>/alerts', methods=['PUT'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/put_hospital_id_alerts.yml', methods=['PUT'])
# def put_hospital_alerts(hospital_id=None):
#     """Update all alerts for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     if not request.json:
#         abort(400, 'Not a JSON')
#     data = request.get_json()
#     for key, value in data.items():
#         if key not in ignore_keys:
#             setattr(obj, key, value)
#     obj.save()
#     return make_response(jsonify(obj.to_dict()), 200)

# @app_views.route('/hospital/<hospital_id>/alerts/<alert_id>', methods=['PUT'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/put_hospital_id_alert_id.yml', methods=['PUT'])
# def put_hospital_alert_id(hospital_id=None, alert_id=None):
#     """Update an alert for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     if alert_id in [alert.id for alert in obj.alerts]:
#         abort(404)
#     alert = storage.get_one_by(Alert, id=alert_id)
#     if alert is None:
#         abort(404)
#     if not request.json:
#         abort(400, 'Not a JSON')
#     data = request.get_json()
#     for key, value in data.items():
#         if key not in ignore_keys:
#             setattr(alert, key, value)

# @app_views.route('/hospital/<hospital_id>/alerts', methods=['DELETE'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/delete_hospital_id_alert.yml', methods=['DELETE'])
# def delete_hospital_alert(hospital_id=None):
#     """Delete all alerts for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     for alert in obj.alerts:
#         storage.delete(alert)
#     storage.save()
#     return make_response(jsonify({}), 200)

# @app_views.route('/hospital/<hospital_id>/alerts/<alert_id>', methods=['DELETE'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/delete_hospital_id_alert_id.yml', methods=['DELETE'])
# def delete_hospital_alert_id(hospital_id=None, alert_id=None):
#     """Delete an alert for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     if alert_id not in [alert.id for alert in obj.alerts]:
#         abort(404)
#     alert = storage.get_one_by(Alert, id=alert_id)
#     if alert is None:
#         abort(404)
#     storage.delete(alert)
#     storage.save()
#     return make_response(jsonify({}), 200)


# @app_views.route('/hospital/<hospital_id>/location', methods=['GET'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/get_hospital_id_location.yml', methods=['GET'])
# def get_hospital_location(hospital_id=None):
#     """Get hospital's location"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     return jsonify([location.to_dict() for location in obj.locations])

# @app_views.route('/hospital/<hospital_id>/staff', methods=['GET'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/get_hospital_id_staff.yml', methods=['GET'])
# def get_hospital_staff(hospital_id=None):
#     """Get all staff for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     return jsonify([staff.to_dict() for staff in obj.staff])


# @app_views.route('/hospital/<hospital_id>/<staff_id>', methods=['POST'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/post_hospital_id_staff_id.yml', methods=['POST'])
# def post_hospital_staff(hospital_id=None, staff_id=None):
#     """Create a new staff for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)

#     if 'staff_id' not in request.get_json():
#         abort(400, description="Missing user_id")

#     data = request.get_json()
    
#     data['hospital_id'] = hospital_id
#     staff_user = CreateUser()
#     staff = staff_user.create_user(data)
#     return make_response(jsonify(staff), 201)

# @app_views.route('/hospital/<hospital_id>/staff/<staff_id>', methods=['PUT'],
#                     strict_slashes=False)
# @swag_from('documentation/hospital/put_hospital_id_staff_id.yml', methods=['PUT'])
# def put_hospital_staff(hospital_id=None, staff_id=None):
#     """Update a staff for a hospital"""
#     obj = storage.get_one_by(Hospital, id=hospital_id)
#     if obj is None:
#         abort(404)
#     staff = storage.get_one_by(HospitalStaff, id=staff_id)
#     if staff is None:
#         abort(404)
    
#     if not request.json or 'staff_id' not in request.json:
#         abort(400, 'Not a JSON')
#     data = request.get_json()
#     for key, value in data.items():
#         if key not in ignore_keys:
#             setattr(staff, key, value)
#     staff.save()
#     return make_response(jsonify(staff.to_dict()), 200)