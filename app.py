from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)



# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set routes for website
@app.route("/")
def home():

    # find one record of mars info
    mars_info = mongo.db.collection.find_one()

    return render_template("index.html", mars_info=mars_info)


# setup scrape route
@app.route("/scrape")
def scrape():

    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_news()
    mars_data = scrape_mars.scrape_image()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)