from flask import Flask, render_template, request, redirect
# from werkzeug.security import secure_filename
from werkzeug.utils import secure_filename


from helpers import *


app = Flask(__name__)
app.config.from_object("flask_s3_upload.config")

#C 'create'     POST        = Get memes into the AWS3 system, from here have an URL that gets saved into MONGODB
#R 'read'       GET         = 
#U 'update'     PUT/ PATH
#D 'delete'     DELETE


@app.route("/", methods=["POST"])
def upload_file():

#READ exactly what the code is doing, DO NOT CONCEPTUALIZE

#Checking if the user file is not in request.files(asking for the files)
#for this to happen it need to have the "user_file" not be in the request.files
    if "user_file" not in request.files:
        return "No user_file key in request.files" #if is not then you get the answer, there is not user_file KEY in request.files 

#Layer of complexity, everytime I'm calling file I'm calling request.files["user_file"]
    file = request.files["user_file"] 

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype
    """

#if the file.filename (getting the actual name of the file) is equal to empty string, request the selection of a file
    if file.filename == "":
        return "Please select a file"

#Checking that what you are requesting is the same as what you are getting
    if file and allowed_file(file.filename):
        #Since the file you are requesting is the same as the file.filename,  
        file.filename = secure_filename(file.filename) #adding one more layer of complexity to file.filename, making the file.filename secure
        output = upload_file_to_s3(file, app.config["S3_BUCKET"]) #Putting after all the effort the file on an S3_BUCKET
        return str(output)
    else:
        return redirect("/") #throwing you of the curve in case the first condition did not succed

@app.route("/", methods=["GET"])
def view_file():
    #If the user_file is not in the owned files, return "it is not there"
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    #We are just setting the variable file to the requested file
    file = request.files["user_file"] #There must be a conditional


# @app.route("/", methods=["PUT"]) 
# def update_complete_file():


# @app.route("/", methods=["PATCH"])
# def update_one_item_in_file():


# @app.route("/", methods=["DELETE"])
# def delete_file():

if __name__ == '__main__':
    app.run
    app.config["DEBUG"] = True
    