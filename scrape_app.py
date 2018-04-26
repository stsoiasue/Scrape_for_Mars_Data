# import dependencies
import scrape_mars
from flask import Flask, render_template, redirect
from pymongo import MongoClient
import creds

# Create a Flask app
app = Flask(__name__)

# index route
@app.route("/")
def index():
    # Connect to MongoDB
    db_user = creds.db_user
    db_pass = creds.db_pass
    uri = f"mongodb://{db_user}:{db_pass}@ds257579.mlab.com:57579/marsdb"

    client = MongoClient(uri,
                        connectTimeoutMS=30000,
                        socketTimeoutMS=None,
                        socketKeepAlive=True)
    db = client.marsdb
    mars = db.mars.find_one()

    client.close()

    return render_template('index.html', mars=mars)


@app.route("/scrape")
def scrape():
    # Connect to MongoDB
    db_user = 'stsoi'
    db_pass = 'Ripfrosty13'
    uri = f"mongodb://{db_user}:{db_pass}@ds257579.mlab.com:57579/marsdb"

    client = MongoClient(uri,
                        connectTimeoutMS=30000,
                        socketTimeoutMS=None,
                        socketKeepAlive=True)
    db = client.marsdb
    # db.authenticate(db_user, db_pass)

    mars_data = scrape_mars.scrape()
    db.mars.update(
        {},
        mars_data,
        upsert=True
    )

    client.close()

    # return redirect("http://127.0.0.1:5000/", code=302)
    return redirect("https://sleepy-depths-19458.herokuapp.com/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

