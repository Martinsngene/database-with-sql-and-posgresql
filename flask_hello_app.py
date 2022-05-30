from flask import Flask, sys, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Getting the object from flask to create our app
app = Flask(__name__)

#Configuring our app and pointing it to our database with resources to login
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/todoapp'

# Setting Track Modifications False to clear deprecation error
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating a database instance for our app to interact with the database
db = SQLAlchemy(app)

# Using Flask Migrate for database migrations
migrate = Migrate(app, db)

# Creating a person class with the db.Model method for SQLAlchemy to help map it to a table in the database

class Todos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default=False)

# This is useful for debugging as it returns info on what you query the database for
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


# This method makes the table mapped with the above class to actually be created in the database
# db.create_all()



@app.route('/todos/create', methods=['POST'])
def create_todo():   
   body={}
   error = False
   try: 
       description =  request.get_json()['description']
       todo = Todos(description=description)
       body['description'] = todo.description
       db.session.add(todo)
       db.session.commit()
   except:        
        error = True
        db.session.rollback()
        print(sys.exc_info())
   finally:
        db.session.close()           
        if  error == True:
            abort(400)
        else:            
            return jsonify(body)

@app.route('/')
def index():
    return 'Hello World!'

#This code goes at the bottom of your flask Python file(this is actually your server)
# This is a second option to start your server
# if __name__ == '__main__':
    # app.debug = True // This helps restart the server each time there is a change
    # app.run(host='0.0.0.0', port=3000)