from datetime import datetime
import os
from flask import Flask ,render_template,request
from pymongo import MongoClient,DESCENDING
from dotenv import load_dotenv

load_dotenv()


def create_app():
        app=Flask(__name__)
        client=MongoClient(os.getenv("MONGODB_URI"))
        app.db = client.microblog


        @app.route("/", methods=["GET","POST"])
        def home():
            if request.method == "POST":
                entry_content = request.form.get("content")
                formatted_date = datetime.today().strftime("%Y-%m-%d")
                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                app.db.entries.insert_one({"content":  entry_content,"date": formatted_date,"time":time})
                

            entries_with_date=[
                    (entry["content"], #content we type,
                    entry["date"], #formated date 
                    datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d"))
                for entry in app.db.entries.find({})
                ]
            return render_template("Home.html",entries=entries_with_date)
        
        @app.route("/recent", methods=["GET","POST"])
        def recent_post():
            entries_with_date=[
                    (entry["content"], #content we type,
                    entry["date"], #formated date 
                    datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d"),
                    entry["time"])
                for entry in app.db.entries.find({}).sort("time",DESCENDING)
                ]
            return render_template("recent.html",entries=entries_with_date)
        
        return app
