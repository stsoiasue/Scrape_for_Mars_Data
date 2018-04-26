# import dependencies
import scrape_mars
from flask import Flask, render_template, redirect
from pymongo import MongoClient

# Create a Flask app
app = Flask(__name__)

# index route
@app.route("/")
def index():
    # Connect to MongoDB
    uri = f"mongodb://stsoi:Testy13@ds257579.mlab.com:57579/marsdb"

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
    uri = f"mongodb://stsoi:Testy13@ds257579.mlab.com:57579/marsdb"

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

    return print('scraping complete')
    # return redirect("http://127.0.0.1:5000/", code=302)
    # return redirect("https://sleepy-depths-19458.herokuapp.com/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

