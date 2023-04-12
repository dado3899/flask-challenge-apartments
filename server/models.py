from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Apartment(db.Model,SerializerMixin):
    __tablename__ = 'apartments'
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.Integer)
    leases = db.relationship("Lease", backref = "apartment")
    serialize_rules = ("-leases.apartment",)

class Tenant(db.Model,SerializerMixin):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer)
    leases = db.relationship("Lease", backref = "tenant")
    serialize_rules = ("-leases.tenant",)

    @validates('age')
    def age_validate(self, key, age):
        print(type(age))
        if age >= 18:
            return age
        else:
            raise Exception("Not correct age")

class Lease(db.Model,SerializerMixin):
    __tablename__ = 'leases'
    id = db.Column(db.Integer, primary_key = True)
    rent = db.Column(db.Integer)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    serialize_rules= ("-tenant.leases","-apartment.leases")