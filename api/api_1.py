from flask import Flask,flash, render_template, request, redirect
import pymysql
from tables import Results
from app import app
from db_config import mysql
from jinja2 import Template
from flaskext.mysql import MySQL
import time
#import MySQLdb
"""
app = Flask(__name__)
app.secret_key = "secret key"
#app.config["DEBUG"] = True

mysql = MySQL()
 # MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'clientDB'
app.config['MYSQL_DATABASE_HOST'] = 'api_db_blend'
mysql.init_app(app)
"""

@app.route('/')
def client_data():
	#return render_template('add.html', client_type = "your")
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_client11")
		rows = cursor.fetchall()
		print "here1"
		table = Results(rows)
		table.border = True
		client_type = "your"
		"""
		_name = "Shraddha thakkar"
		print _name
		sql = "INSERT INTO tbl_client11(client_name) VALUES(%s)"
		data = _name
		cursor.execute(sql, data)
		cursor.execute("SELECT * FROM tbl_client11")
		rows = cursor.fetchall()
		print "here3"
		table = Results(rows)
		table.border = True
		print table
		print "Here2"
		"""
		return render_template('add.html', table=table, client_type = client_type)
		#return render_template('add.html', client_type = client_type)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

	

@app.route('/home', methods=['POST'])
@app.route('/home/<client_type>/', methods=['POST'])
@app.route('/home/<client_type>/<clientId>', methods=['POST'])
def add_client(client_type, clientId=None):
	client_type = client_type
	try:
		if client_type == "your":
			_name = request.form['inputName']
			_age = request.form['inputAge']
			_username = request.form['inputUsername']
			_option = request.form['inputOption']
			#validating client entered values
			if _name and _age and _username and _option and request.method == 'POST':
				# saving in DB
				sql = "INSERT INTO tbl_client11(client_name, client_age, client_username, client_option) VALUES(%s, %s, %s, %s)"
				data = (_name, _age, _username, _option )
				print "here1"
				conn = mysql.connect()
				print "here2"
				cursor = conn.cursor()
				cursor.execute(sql, data)
				cursor.execute("SELECT * FROM tbl_client11 WHERE client_username = %s", _username)
				records = cursor.fetchone()
				print records
				_id = records[0]
				conn.commit()
				flash('Client registered successfully!')
				if _option == "Refinance":
					return render_template('refinance.html',client_type=client_type, clientId = _id)
					#return redirect('/<client_type>/refinance')
				elif _option == "New Purchase":
					return render_template('co-borrower.html', client_type=client_type, clientId = _id)
					#return redirect('/client_type>/coborrower')
				return redirect('/')
			else:
				return "Couldn't register the client. Please check the details entered"
		elif client_type == "co-borrower's":
			_coborrowerName = request.form['inputName']
			print _coborrowerName
			_coborrowerAge = request.form['inputAge']
			print _coborrowerAge
			_id = clientId
			if _coborrowerAge and _coborrowerName and request.method == 'POST':
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute("SELECT * FROM tbl_client11 WHERE id=%s", _id)
				records = cursor.fetchone()
				if _coborrowerName.lower() == records[1].lower():
					return render_template('add.html', client_type=client_type, clientId=_id, 
						errorMessage="You can not be the co-borrower as well, please re-enter the co-borrower details")
				elif  _coborrowerName.lower() != records[1].lower():
					# saving in DB
					sql = "UPDATE tbl_client11 SET coborrower_name=%s, coborrower_age=%s WHERE id=%s"
					data = (_coborrowerName, _coborrowerAge, _id)
					cursor.execute(sql, data)
					conn.commit()
					#time.sleep(5)
					cursor.execute("SELECT * FROM tbl_client11 WHERE id=%s", _id)
					records = cursor.fetchone()
					return render_template("final.html", value= records, client_type=client_type)
				else:
					return "Couldn't register co-borrower entries. Please check the details entered"
	except Exception as e:
		if e[0] == 1062:
			return render_template('add.html', client_type = client_type, errorMessage="User with entered username already exists, please re-enter your details")
			print(e)
		
	finally:
		cursor.close() 
		conn.close()

"""
@app.route('/<client_type>/refinance')
def refinance_client_view():
	return render_template('refinance.html')
"""

@app.route('/home/<client_type>/refinance/<int:clientId>', methods=['POST'])
def refinance_client(client_type, clientId):
	try:
		_id = clientId
		_street = request.form['inputStreet']
		_city = request.form['inputCity']
		_state = request.form['inputState']
		_zipcode = request.form['inputZipcode']
		if _street and _city and _state and _zipcode and request.method == 'POST':
			sql = "UPDATE tbl_client11 SET client_street=%s, client_city=%s, client_state=%s, client_zipcode=%s WHERE id=%s"
			data = (_street, _city, _state, _zipcode, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Refinance details added successfully!')
			#return redirect('/home/client_type/co-borrower/clientId')
			return render_template('co-borrower.html', client_type=client_type, clientId=clientId)

		else:
			return "Couldn't register the client. Please check the details entered"
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/home/<client_type>/co-borrower/<int:clientId>')
def coborrower_client_view(client_type, clientId):
	client_type =client_type
	return render_template('co-borrower.html', client_type=client_type, clientId=clientId)

@app.route('/home/<client_type>/co-borrower/<int:clientId>/details', methods=['POST'])
def coborrower_client(client_type, clientId):
	try:
		client_type = client_type
		_id = clientId
		_choice = request.form['inputChoice']
		if _choice.lower() == "yes":
			flash('Please add co-borrower details')
			coborrower = "co-borrower's"
			return render_template('add.html', client_type=coborrower, clientId=_id)
		elif _choice.lower() == "no":
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM tbl_client11 WHERE id=%s", _id)
			records = cursor.fetchone()
			return render_template('final.html', value=records, client_type=None)
			#return redirect("/clientDetails/thankyou")
		else:
			return "Couldn't register the client. Please check the details entered"
	except Exception as e:
		print(e)
	finally:
		print "Done"

@app.route('/clientDetails/thankyou')
def final_client_view():
	return render_template('final.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form['Name']
      print result
      return render_template("result.html",result = result)


if __name__ == "__main__":
	app.run(host="0.0.0.0")
 