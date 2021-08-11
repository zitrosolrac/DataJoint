from flask import Flask
from flask import jsonify
import datajoint as dj
from flask import request
import datetime

#the code below connects to a datajoint db 
#and creates a schema 

dj.config['database.host'] = 'tutorial-db.datajoint.io'
dj.config['database.user'] = 'carlosortiz9204'
password = input("Enter your password: ")
dj.config['database.password'] = password

dj.conn()

schema = dj.schema('carlosortiz9204_challenge')

# the code below creates tables using primary keys and composite keys as directed 

@schema
class Subject(dj.Manual):
    definition = """
    # Experimental animals
    subject_name         : varchar(255)                 # Unique name
    ---
    subject_dob          : date                         # date of birth
    subject_sex          : enum('M','F','unknown')      # sex
    """

@schema
class ExperimentSetup(dj.Manual):
    definition = """
    # Experimental animals
    experiment_setup     : int                # Unique id
    ---
   
    """

@schema
class Session(dj.Manual):
    definition = """
    # Experimental animals
    ->ExperimentSetup
    ->Subject
    session_date     : date                # Unique date
    ---
   
    """

#the code below populates the tables we created above with data from a file given to us called data.json 

data = [
    {
        "experiment_setup": 1
    },
    {
        "experiment_setup": 2
    },
    {
        "experiment_setup": 1
    },
    {
        "experiment_setup": 2
    },
    {
        "experiment_setup": 1
    }
]

ExperimentSetup.insert(data, skip_duplicates=True)

data = [
    {
        "subject_name": "K0 (chx10)",
        "subject_dob": "2008-03-02",
        "subject_sex": "M"
    },
    {
        "subject_name": "K0 (chx10)",
        "subject_dob": "2008-03-02",
        "subject_sex": "M"
    },
    {
        "subject_name": "K0 (chx20)",
        "subject_dob": "2008-03-10",
        "subject_sex": "F"
    },
    {
        "subject_name": "K0 (chx20)",
        "subject_dob": "2008-03-10",
        "subject_sex": "F"
    },
    {
        "subject_name": "M0 (chx10)",
        "subject_dob": "2008-03-25",
        "subject_sex": "F"
    }
]

Subject.insert(data, skip_duplicates=True)

data = [
    {
        "session_date": "2008-06-06",
        "experiment_setup": 1,
        "subject_name": "K0 (chx10)"
    },
    {
        "session_date": "2008-06-09",
        "experiment_setup": 2,
        "subject_name": "K0 (chx10)"
    },
    {
        "session_date": "2008-06-07",
        "experiment_setup": 1,
        "subject_name": "K0 (chx20)"
    },
    {
        "session_date": "2008-06-08",
        "experiment_setup": 2,
        "subject_name": "K0 (chx20)"
    },
    {
        "session_date": "2008-06-10",
        "experiment_setup": 1,
        "subject_name": "M0 (chx10)"
    }
]

Session.insert(data, skip_duplicates=True)

app = Flask(__name__)

#

@app.before_request
def before():
    print("This is executed BEFORE each request.")

#The code below are get request methods that are supplying data from respective data tables 
    
@app.route('/subject')
def hello():
    return jsonify(Subject().fetch(as_dict=True))

@app.route('/experimentsetup')
def experimentSetup():
    return jsonify(ExperimentSetup().fetch(as_dict=True))

@app.route('/session')
def experimentSession():
    return jsonify(Session().fetch(as_dict=True))

#The code below are post request methods that are receiving data and storing them in respective data tables

@app.route('/add_subject', methods=['POST'])
def postSub():
    data = request.get_json()
    print(data)
    name = data['name']
    dob = data['dob']
    sex = data['sex']
    

    Subject.insert1([name, dob, sex])

    return 'Done', 201

@app.route('/add_expSet', methods=['POST'])
def postExpSet():
    data = request.get_json()
    expSet = data['expSet']

    ExperimentSetup.insert([expSet])
    
    print(data)
    return 'Done', 201

@app.route('/add_session', methods=['POST'])
def postEntry():
    data = request.get_json()
    name = data['name']
    expSet = int(data['expSet'])
    sesDat = data['sesDat']

    Session.insert1([expSet, name, sesDat])
    
    print(data)
    return 'Done', 201

app.run(threaded=False)

#I made the threaded parameter false so the useEffect hooks could operate as intended 