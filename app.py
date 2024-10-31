from flask import Flask
from flask_graphql import GraphQLView
from database import db_session, init_db, connection_url
from schema import schema
app = Flask(__name__)

app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = connection_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



with app.app_context():
    init_db()


    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ))

# break the connection if the application is down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# for run the application:
# run in terminal:
# docker compose up --build
# for shot down:
# docker compose down