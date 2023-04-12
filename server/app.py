from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )
api = Api(app)

class All_Apartments(Resource):
    def get(self):
        all_apartments = Apartment.query.all()
        apartment_dict = []
        for apartment in all_apartments:
            apartment_dict.append(apartment.to_dict())
        return make_response(apartment_dict,200)
    def post(self):
        data = request.get_json()
        new_apart = Apartment(
            number = data["number"]
        )
        db.session.add(new_apart)
        db.session.commit()
        return make_response(new_apart.to_dict(), 201)
api.add_resource(All_Apartments,"/apartment")

class All_Tenant(Resource):
    def get(self):
        all_tenant= Tenant.query.all()
        tenant_dict = []
        for tenant in all_tenant:
            tenant_dict.append(tenant.to_dict())
        return make_response(tenant_dict,200)
    def post(self):
        data = request.get_json()
        new_tenant = Tenant(
            name = data["name"],
            age = data["age"]
        )
        db.session.add(new_tenant)
        db.session.commit()
        return make_response(new_tenant.to_dict(), 201)
api.add_resource(All_Tenant,"/tenant")

class UD_Apartments(Resource):
    def patch(self,id):
        data = request.get_json()
        apartment_up = Apartment.query.filter(Apartment.id == id).first()
        for key in data.keys():
            setattr(apartment_up,key,data[key])
        db.session.add(apartment_up)
        db.session.commit()
        return make_response(apartment_up.to_dict(),203)
    def delete(self,id):
        apartment_del = Apartment.query.filter(Apartment.id == id).first()
        db.session.delete(apartment_del)
        db.session.commit()
        return make_response({},200)
api.add_resource(UD_Apartments,"/apartment/<id>")

class UD_Tenants(Resource):
    def patch(self,id):
        data = request.get_json()
        tenant_up = Tenant.query.filter(Tenant.id == id).first()
        for key in data.keys():
            setattr(tenant_up,key,data[key])
        db.session.add(tenant_up)
        db.session.commit()
        return make_response(tenant_up.to_dict(),203)
    def delete(self,id):
        tenant_del = Tenant.query.filter(Tenant.id == id).first()
        db.session.delete(tenant_del)
        db.session.commit()
        return make_response({},200)
api.add_resource(UD_Tenants,"/tenant/<id>")

class Make_Lease(Resource):
    def post(self):
        data = request.get_json()
        new_lease = Lease(
            rent = data["rent"],
            apartment_id = data["apartment_id"],
            tenant_id = data["tenant_id"]
        )
        db.session.add(new_lease)
        db.session.commit()
        return make_response(new_lease.to_dict(), 201)
api.add_resource(Make_Lease,"/lease")
class Delete_Lease(Resource):
    def delete(self,id):
        lease_del = Lease.query.filter(Lease.id == id).first()
        db.session.delete(lease_del)
        db.session.commit()
        return make_response({},200)
api.add_resource(Delete_Lease,"/lease/<id>")

if __name__ == '__main__':
    app.run( port = 3000, debug = True )