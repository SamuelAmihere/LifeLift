#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Hospitals """
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models.incident import Incident
from models.system_user import Patient
from datetime import date, datetime


ignore_keys = ['id', 'created_at', 'updated_at']


@app_views.route('/patients', methods=['GET'])
@swag_from('documentation/patients/get_patient.yml', methods=['GET'])
def get_patients():
    """Get all patients"""
    objs = storage.all(Patient).values()
    pat = []
    i = 0
    for obj in objs:
        incident = storage.get_one_by(Incident, id=obj.incident_id)
        if incident:
            i += 1
            obj.reason = incident.incident_description
            obj.latitude = incident.latitude
            obj.longitude = incident.longitude
            obj.No = i
            diff = datetime.utcnow() - obj.created_at
            sec = diff.total_seconds()
            minutes = sec / 60
            hours = minutes / 60
            days = hours / 24

            time = ""
            if days > 1:
                time = "{} day{} ago".format(int(days), "s" if int(days) > 1 else "")
            elif hours > 1:
                time = "{} hour{} ago".format(int(hours), "s" if int(hours) > 1 else "")
            elif minutes > 1:
                time = "{} minute{} ago".format(int(minutes), "s" if int(minutes) > 1 else "")
            else:
                time = "{} second{} ago".format(int(sec), "s" if int(sec) > 1 else "")

            obj.time = time
            pat.append(obj.to_dict())
    return jsonify(pat)