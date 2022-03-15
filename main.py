from flask import Flask, make_response, request, jsonify, request
from flask_mongoengine import MongoEngine, QuerySet

app = Flask(__name__)

database_name = "API"
mongodb_password = "Z4qLDcW4j" # BIG SECRET
DB_URI = "mongodb+srv://Team3:Z4qLDcW4j@cluster0.sebfg.mongodb.net/API?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)
print("connected to db")

# this is a custom query set
# it helps devs filter mongo data
class AddressQuerySet(QuerySet):
    def filter_name(self, name):
        print("name: {}".format(name))
        return self.filter(name__icontains=name)

    def filter_name_exact(self, name):
        print("name: {}".format(name))
        return self.filter(name=name)

    def filter_line1(self, line1):
        print("addr line 1: {}".format(line1))
        return self.filter(line1__icontains=line1)

    def filter_line2(self, line2):
        print("addr line 2: {}".format(line2))
        return self.filter(line2__icontains=line2)

    def filter_zipcode(self, zipcode):
        print("zip code: {}".format(zipcode))
        return self.filter(zipcode=zipcode)

    def filter_city(self, city):
        print("city: {}".format(city))
        return self.filter(city=city)

    def filter_state(self, state):
        print("state: {}".format(state))
        return self.filter(state=state)

# A mongodb schema for Address
# it is design to work for address from that 11 countries/region
class Address(db.Document):
    meta = {'queryset_class': AddressQuerySet}
    addr_id = db.IntField()
    name= db.StringField()
    line1 = db.StringField()
    line2 = db.StringField()
    city = db.StringField()
    state = db.StringField()
    zipcode = db.IntField()
    country = db.StringField()
    # see 2.5.6. Custom Query Set in mongo-engine official documentation

    def to_json(self):
        # converts this documents to JSON
        return {
            "addr_id": self.addr_id,
            "name": self.name,
            "line1": self.line1,
            "line2": self.line2,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "country": self.country
        }


# look up address with multiple params
@app.route('/api/lookup/test2', methods=['GET'])
def api_lookup_multi_param():
    # need state for sure
    state = request.args.get('state', default = None, type = str)
    if not state:
        return make_response("state not provided", 400)

    # need city for sure
    city = request.args.get('city', default = None, type = str)
    if not city:
        return make_response("city not provided", 400)

    # narrow down to city, state
    result = Address.objects.filter_state(state).filter_city(city)

    # optional param: name, line1, line2, zipcode
    # filter name
    name = request.args.get('name', default = None, type = str)
    if name:
        result = result.filter_name(name)

    # filter line 1
    line1 = request.args.get('line1', default = None, type = str)
    if line1:
        result = result.filter_line1(line1)

    # fileter line 2
    line2 = request.args.get('line2', default = None, type = str)
    if line2:
        result = result.filter_line2(line2)

    # filter zipcode
    zipcode = request.args.get('zipcode', default = None, type = int)
    if line2:
        result = result.filter_zipcode(zipcode)

    if result:
        return make_response(jsonify(result), 200)
    return make_response("address not found", 404)

# GET return the details of all addresses
@app.route('/api/address', methods=['GET'])
def api_addresses():
    if request.method == "GET":
        result = []
        for addr in Address.objects:
            result.append(addr)
        return make_response(jsonify(result), 200)
    pass


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)