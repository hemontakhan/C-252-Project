# importing flask modules
from flask import Flask , request , render_template , jsonify

# importing firebase_admin module
import firebase_admin

# importing firestore.py module to create firestore client
from firebase_admin import firestore

# importing credentials.py module from firebase_admin folder
from firebase_admin import credentials

# creating authentication file
cred = credentials.Certificate(" ")

# connect this python script/app with firebase using the authentication credentials
firebase_admin.initialize_app(cred)

# creating firestore client
fb_db = firestore.client()

# creating flask object
app = Flask(__name__)

# first api : index page, only GET requests allowed at this API 
@app.route('/get-data',method=["GET"])
def index():
    try:
        # getting values from firebase document
         pot = fb_db.collection('Project 252').document('potentiometer values').get().to_dict()

        # convert it to python dictionary format

        # extracting value from dictionary
        val = pot['pot val']

        # rendering index.html template and pass the extracted value
        return render_template('index.html', value=val)
   except Exception as e:
      print(e)
      return jsonify({'status': 'failed'}) 



# second api : adding data , only POST request allowed at this API
@app.route('/add-data',method=["POST"])
def add():
    try:
        # getting potentiometer value from esp32
         pot_val = request.json.get('potentiometer')
        # sending potentiometer value on firebase
         fb_db.collection('Project 252').document('potentiometer values').set({'pot val': pot_val})
        # return status is json format
    except Exception as e:
        print(e)
        return jsonify({'status': 'failed'})
    



# start the server
if __name__  ==  "__main__":
    app.run(host = '0.0.0.0' , debug = True)

