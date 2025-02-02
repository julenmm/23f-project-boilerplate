# Some set up for the application 

from flask import Flask
from flaskext.mysql import MySQL

# create a MySQL object that we will use in other parts of the API
db = MySQL()

def create_app():
    app = Flask(__name__)
    
    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'

    # these are for the DB object to be able to connect to MySQL. 
    app.config['MYSQL_DATABASE_USER'] = 'webapp'
    app.config['MYSQL_DATABASE_PASSWORD'] = open('/secrets/db_password.txt').readline().strip()
    app.config['MYSQL_DATABASE_HOST'] = 'db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'HotelFranchiseDB'  # Change this to your DB name

    # Initialize the database object with the settings above. 
    db.init_app(app)
    
    # Add the default route
    # Can be accessed from a web browser
    # http://ip_address:port/
    # Example: localhost:8001
    @app.route("/")
    def welcome():
        return "<h1>Welcome to the 3200 boilerplate app</h1>"

    # Import the various Blueprint Objects
    from src.front_desk_agent.front_desk_agent  import front_desk_agent
    from src.hotel_manager.hotel_manager import hotel_manager
    from src.housekeeping_supervisor.housekeeping_supervisor  import housekeeping_supervisor


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.register_blueprint(front_desk_agent,    url_prefix='/f')
    app.register_blueprint(hotel_manager,   url_prefix='/m')
    app.register_blueprint(housekeeping_supervisor,    url_prefix='/s')


    # Don't forget to return the app object
    return app