import datetime
from flask import Flask ,render_template,request
from pymongo import MongoClient


def create_app():
        app=Flask(__name__)
        client=MongoClient("mongodb+srv://shanpriya:SHANpriya2023@microblog.nj5juk6.mongodb.net/")
        app.db = client.microblog


        @app.route("/", methods=["GET","POST"])
        def home():
            if request.method == "POST":
                entry_content = request.form.get("content")
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                app.db.entries.insert_one({"content":  entry_content,"date": formatted_date})
                

            entries_with_date=[
                    (entry["content"], #content we type,
                    entry["time"], #formated date 
                    datetime.datetime.strptime(entry["time"],"%Y-%m-%d").strftime("%b %d"))
                for entry in app.db.entries.find({})
                ]
            return render_template("Home.html",entries=entries_with_date)
        return app