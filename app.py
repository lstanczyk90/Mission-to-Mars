# Import dependencies

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create initial route

@app.route("/")
def index():

    # uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. 
    # We will also assign that path to themars variable for use later

   mars = mongo.db.mars.find_one()

   # Tells Flask to return an HTML template using an index.html file

   return render_template("index.html", mars=mars)

# This route will be the "button" of the web application, the one that will scrape updated data when we tell it to from the homepage of our web app. 
# It'll be tied to a button that will run the code when it's clicked.

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()

   # We're inserting data, so first we'll need to add an empty JSON object with {} in place of the query_parameter. 
   # Next, we'll use the data we have stored in mars_data. Finally, the option we'll include is upsert=True. 
   # This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).

   mars.update({}, mars_data, upsert=True)

   # Add a redirect after successfully scraping the data. This will navigate our page back to / where we can see the updated content.

   return redirect('/', code=302)

# Code to tell Flask to run
   
if __name__ == "__main__":
    app.run()