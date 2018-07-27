# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

conn = 'mongodb://localhost:27017/mars'
client = pymongo.MongoClient(conn)

db1 = client.mars_db
collection1 = db1.items
collection1.drop()

# create instance of Flask app
app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
# # Use flask_pymongo to set up mongo connection
# mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    dynamic_dic = collection1.find_one()

    # return template and data
    return render_template("index.html", dynamic_dic=dynamic_dic)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    news = scrape_mars.mars_news()
    featured_image = scrape_mars.JPL_image()
    mars_weather = scrape_mars.mars_weather()
    table = scrape_mars.mars_fact()

    dynamic_dic = {
        "news_title": news.title,
        "news_p": news.news,
        "featured_image": featured_image,
        "weather": mars_weather,
        "facts": table
    }

    
    # Insert into database
    collection1.insert_one(dynamic_dic)



    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)







    # # Run scraped functions
    # weather = scrape_info.scrape_weather()
    # surf = scrape_info.scrape_surf()

    # # Store results into a dictionary
    # forecast = {
    #     "time": weather["time"],
    #     "location": weather["name"],
    #     "min_temp": weather["min_temp"],
    #     "max_temp": weather["max_temp"],
    #     "surf_location": surf["location"],
    #     "height": surf["height"]
    # }

   

    


if __name__ == "__main__":
    app.run(debug=True)
