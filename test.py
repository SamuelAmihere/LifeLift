#! /usr/bin/env python3

from models.hospital.hosp_operator import HealthTopic, Hospital
from models.system_user import SystemUser
from models.patient import Patient
from models.location import Location
from models.ambulance.ambulance import Ambulance
from models.incident import Incident
from models.ambulance.ambu_operator import AmbulanceOwner, Driver
from models.location import Site, Address
import models

# create ambulances
amb1 = Ambulance(ambulance_type="Type 1")
amb1.save()
amb2 = Ambulance(ambulance_type="Type 2")
amb2.save()
# create drivers
driver1 = Driver(name="Driver 1", email="d1@gmail.com", phone="08012345678")
driver1.save()
driver2 = Driver(name="Driver 2", email="d2@yahoo.com", phone="08012345678")
driver2.save()

# create operator
op1 = AmbulanceOwner(name="Operator 1", email="mosesent@gmail.com",
                     phone="08012345678")

# Add ambulances and drivers to operator
op1.ambulances = ["0ddc6b59-465a-4b5b-970c-1a63cae880b8"]
op1.drivers = ["8ed3cd7e-6987-4a90-98d4-9e36b07b33fc", "58ef0fff-51ad-49f3-879e-41254825daac"]
op1.save()

# Add ambulances to site
if op1.assign_driver_to_ambulance("58ef0fff-51ad-49f3-879e-41254825daac", "0ddc6b59-465a-4b5b-970c-1a63cae880b8"):
    print(f"Driver added to")
op1.save()

# Create Address for sites
adds1 = Address(street="Street1", city="Lagos", state="Lagos", country="Nigeria")
adds1.save()
adds2 = Address(street="Street2", city="Lagos", state="Lagos", country="Nigeria")
adds2.save()


# create sites
site1 = Site(name="Site 1", address=adds1.id,
             latitude=6.5244, longitude=3.3792)
site1.save()

site2 = Site(name="Site 2", address=adds2.id,
             latitude=6.5244, longitude=3.3792)

# Create Address for hospitals
adds3 = Address(street="Street3", city="Amambra", state="Lagos", country="Nigeria")
adds4 = Address(street="Street3", city="Lagos", state="Lagos", country="Nigeria")
adds3.save()
adds4.save()

# Hospital
hosp1 = Hospital(name="Hospital 1", address=adds3.id,
                 phone="08012345678", email="hos1@g.com",
                 latitude=6.5244, longitude=3.3792)
hosp2 = Hospital(name="Hospital 2", address=adds4.id,
                 phone="08012345678", email="hosp2@co.com",
                 latitude=4.574, longitude=8.37892)

# create locations
loc1 = Location(latitude=6.5244, longitude=3.3792, radius=1000)

# add sites to location
loc1.active_sites = [site1.id, site2.id]
loc1.active_hospitals = [hosp1.id]

print(loc1.active_sites)

# create Hospital staff
staff1 = SystemUser(full_name="Staff 1", email="st1@yahoo.com",
                    phone="08012345678", hospital_id=hosp1.id,
                    role="Nurse")

staff2 = SystemUser(full_name="Staff 2", email="hdhd@yyy.co",
                    phone="08012345678", hospital_id=hosp2.id,
                    role="Nurse")


# Add staff to hospital
hosp1.staff = [staff1.id, staff2.id]

# create Health Topics
ms1 = """
This is our first message of the day on Corona Virus.
Please stay safe and adhere to all safety measures.
"""
ms2 = """
This is our second message of the day on Heart atttacks.
When you feel a sharp pain in your chest, please call 911.
"""
ms3 = """
This is our third message of the day on Malaria.
Please take your medication as prescribed by your doctor.
Don't forget to sleep under a treated mosquito net.
"""
ht1 = HealthTopic(topic="Topic 1", staff_id=staff1.id,
                   message=ms1)
ht2 = HealthTopic(topic="Topic 2", staff_id=staff1.id,
                     message=ms2)

# Add health topics to staff
staff1.health_topics = [ht1.id, ht2.id]


ht1.save()
ht2.save()

staff2.save()
staff1.save()

hosp1.save()
hosp2.save()