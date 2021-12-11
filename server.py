from flask import Flask,Response,request
import pymongo
import json
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="Localhost",port=27017,serverSelectionTimeoutMS = 1000)
    db = mongo.company
    mongo.server_info()

except:
    print("Error- cannot conncet to the DB")


@app.route("/users",methods=["POST"])
@cross_origin()
def create_user():
    try:
        # user={"name":request.form["name"],"lastName":request.form["lastName"]}
        # dbResponse = db.users.insert_one(user)
        # # print(dbResponse.inserted_id)

        # return Response(
        #     response= json.dumps({"message":"user created","id": f"{dbResponse.inserted_id}"}),
        #     status=200,
        #     mimetype="application/json"
        # )
        user={"userName":request.json['userName'],"email":request.json["email"],"salary":request.json["salary"],"address":request.json["salary"]}
        dbResponse = db.users.insert_one(user)
        return Response(
            response= json.dumps({"message":"user created","id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)


@app.route("/users/<id>",methods=["PUT"])
def update_users(id):
    try:
        dbResponse = db.users.update_one(
            {"_id":ObjectId(id)},
            { "$set": { "name": request.form["name"] ,"lastName":request.form["lastName"]}}
        )
        for attr in dir(dbResponse):
            print(f"***{attr}***")
    
        return Response(
            response= json.dumps({"message":"user Updated"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"cannot user Updated"}),
            status=500,
            mimetype="application/json"
        )


@app.route("/users",methods=["GET"])
@cross_origin(origin="*")
def getUsers():
    try:
        data = list(db.users.find())
        for user in data :
            user["_id"] = str(user["_id"])        
        return Response(response= json.dumps(data),status=200,mimetype="application/json")

    except Exception as ex:
       return Response(
            response= json.dumps({"message":"Cannot get data"}),
            status=500,
            mimetype="application/json"
        )

@app.route("/users/<id>",methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1 :
            for attr in dir(dbResponse):
                print(f"***{attr}***")

            
            return Response(
            response= json.dumps({"message":"user Deleted"}),status=200,mimetype="application/json")
    
        return Response(
            response= json.dumps({"message":"user cannot Delete"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"cannot user delete"}),
            status=500,
            mimetype="application/json"
        )



if __name__ == "__main__":
    app.run(port=80,debug=True)