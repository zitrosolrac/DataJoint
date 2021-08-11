import datajoint as dj

dj.config['database.host'] = 'tutorial-db.datajoint.io'
dj.config['database.user'] = 'carlosortiz9204'
dj.config['database.password'] = 'Houst0n!'

dj.conn()

schema = dj.schema('carlosortiz9204_challenge')

schema.spawn_missing_classes()

# please uncomment these as you see fit to clear custom entered data from tables

#ExperimentSetup.drop()

#Subject.drop()

#Session.drop()

print(Session())

