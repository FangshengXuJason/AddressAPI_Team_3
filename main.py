from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)

database_name = "API"
mongodb_password = "Z4qLDcW4j"
DB_URI = "mongodb+srv://Team3:Z4qLDcW4j@cluster0.sebfg.mongodb.net/API?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)


class Address(db.Document): 
    addr_id = db.IntField()
    name= db.StringField()
    line1 = db.StringField()
    line2 = db.StringField()
    city = db.StringField()
    state = db.StringField()
    zipcode = db.IntField()
    country = db.StringField()

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


# populate a JSON file and return 201 if success
@app.route('/api/db_populate', methods=['POST'])
def db_populate(): 
    addr1 = Address(addr_id = 1,
                name="Jason Bourne",
                line1="1000 E Cherry",
                line2="APT 100" ,
                city="Seattle",
                state="WA",
                zipcode=98122,
                country="the United States"
                )
    addr1.save()
    return make_response("", 201)

# GET return the details of all books
@app.route('/api/address', methods=['GET'])
def api_books(): 
    if request.method == "GET": 
        result = []
        for addr in Address.objects: 
            result.append(addr)
        return make_response(jsonify(result), 200)
    pass

if __name__ == '__main__': 
    # app.run()
    app.run(debug=True)