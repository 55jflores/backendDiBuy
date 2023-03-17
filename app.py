from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import json

import os
from dotenv import dotenv_values

import sqlite3

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import cloudinary.api


# Config for cloudinary
config_values = dotenv_values('.env')
config = cloudinary.config(
  cloud_name = config_values['CLOUD_NAME'],
  api_key = config_values['API_KEY'],
  api_secret = config_values['API_SECRET'],
  secure = True
)

# Folder path
UPLOAD_FOLDER = 'static'
# Allowed files
ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG',"heic","HEIC"}

# Creating an instance of a class (object)
app = Flask( 
	__name__,
	template_folder='templates',
	static_folder='static'
)

# Setting config folder for uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Checking if file uploaded is an image
def allowed_file(filename):
    split = filename.split('.')
    if split[-1] in ALLOWED_EXTENSIONS:
        return True
    return False

# Querying DB and grabbing results
def carQuery(year,make,model):
	with sqlite3.connect('carBase.db') as conn:
		c = conn.cursor()

		# Get rid of whitespace, capitalize first letter
		make = make.strip().lower().title()
		model = model.strip().lower().title()

		# Query with user parameters
		theCar = make + model 
		carQuery = f"SELECT * FROM {theCar} where year=:year"

		# Execute query and grab results
		c.execute(carQuery,{'year':year})
		queryOutput = c.fetchall()
	conn.close()

	return queryOutput

# Formatting results in JSON format
def jsonOutput(queryOutput):
	car_array = []
	i = 0
	while i < len(queryOutput):
		user_dictionary = {
			'id': queryOutput[i][0],
			'user': queryOutput[i][1],
			'contact': queryOutput[i][2],
			'year': queryOutput[i][3],
			'price': queryOutput[i][4],
			'date': queryOutput[i][5],
		}
		urls_arr = queryOutput[i][6].split(" ")
		user_dictionary['urls'] = urls_arr

		car_array.append(user_dictionary)
		i += 1
	return car_array

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# Grabbing the list of image files
		files = request.files.getlist('file')

		# Grabbing make and model
		userMake = request.form.get('umake')
		userModel = request.form.get('umodel')
		
		# String that will store Cloudinary urls
		srcURLS = ''
		# Going through each file and saving it
		for file in files:
			if file and allowed_file(file.filename):
				# Saving file to disk
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				saved_file = "static/" + filename
				
				# Uploading image
				cloudinary.uploader.upload(saved_file,public_id=filename,unique_filename=False, overwrite=True)
				# Building URL for image and save it in variable
				srcURL = cloudinary.CloudinaryImage(filename).build_url()
				# Appending each unique url to a string with a space in between
				srcURLS += ' ' + srcURL

				# Delete file from disk
				os.remove(saved_file)
				

		# Saving upload to DataBase
		with sqlite3.connect('carBase.db') as conn:
			c = conn.cursor()
			c.execute("INSERT INTO cars VALUES (?,?,?,?)",('1',userMake,userModel,srcURLS))
			conn.commit()

		#img_name = "static/" + filename
		#return render_template("post.html",img_name = img_name, my_index = 1)
		return 'Hello'
																	
	return render_template("main.html")

@app.route('/cars/<year>/<make>/<model>')
def available_cars(year,make,model):
	# Make query to the DB
	queryOutput = carQuery(year,make,model)
	# Formatting query results in json format
	cars_array = jsonOutput(queryOutput)
	# Flask version of JSOn
	cars_array = jsonify(cars_array)
	cars_array.headers.add('Access-Control-Allow-Origin', '*')
	
	return cars_array

if __name__ == "__main__":
  app.run()