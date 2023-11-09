import os
from flask import Flask
from flask_cors import CORS
from forestadmin.datasource_sqlalchemy.datasource import SqlAlchemyDatasource
from forestadmin.flask_agent.agent import create_agent
from decouple import config


def initialize_forest_admin(app):
    """
    Initialize Forest Admin within a Flask application.

    Args:
        app (Flask): The Flask application to initialize Forest Admin for.

    Returns:
        None
    """
    # Define settings for the Forest Agent in Flask config
    app.config["FOREST_ENV_SECRET"] = os.environ.get("FOREST_ENV_SECRET")
    app.config["FOREST_AUTH_SECRET"] = os.environ.get("FOREST_AUTH_SECRET")

    # Create the Forest Agent
    agent = create_agent(app)

    # Set up CORS settings for Forest Admin
    CORS(
        app,
        resources={
            r"/forest/*": {"origins": r".*\.forestadmin\.com.*"},
        },
        supports_credentials=True,
    )

    # Retrieve database configuration from environment variables 
    # (similar to app.py)
    db_config = {
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'database': config('DB_NAME'),
    }

    # Construct the MySQL database URI using the app's database configuration
    db_uri = f'mysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}/{db_config["database"]}'

    # Register your data source to the agent using the updated database URI
    with app.app_context():
        agent.add_datasource(SqlAlchemyDatasource(db_uri=db_uri))

    # Finally, start the agent
    agent.start()


# Create your Flask app
app = Flask(__name)

# Initialize Forest Admin
initialize_forest_admin(app)
