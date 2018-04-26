# import dependencies
import scrape_mars
from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient

# Create a Flask app
app = Flask(__name__)

# index route
@app.route("/")
def index():
    # Connect to MongoDB
    uri = "mongodb://stsoi:Testy13@ds257579.mlab.com:57579/marsdb"

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
    uri = "mongodb://stsoi:Testy13@ds257579.mlab.com:57579/marsdb"

    client = MongoClient(uri,
                        connectTimeoutMS=30000,
                        socketTimeoutMS=None,
                        socketKeepAlive=True)
    db = client.marsdb

    mars_data = scrape_mars.scrape()
    db.mars.update(
        {},
        mars_data,
        upsert=True
    )

    client.close()

    return redirect(url_for("index"), code=302)

if __name__ == "__main__":
    app.run(debug=True)

