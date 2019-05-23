from flask import Flask,flash, render_template, request, redirect
import pymysql
from tables import Results
#from db_config import mysql
from jinja2 import Template
from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key = "secret key"
app.config["DEBUG"] = True

mysql = MySQL()
 # MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'clientDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def client_data():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_client11")
		rows = cursor.fetchall()
		table = Results(rows)
		table.border = True
		client_type = "your"
		return render_template('add.html', table=table, client_type = client_type)
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
			print _option
			#validating client entered values
			if _name and _age and _username and _option and request.method == 'POST':
				# saving in DB
				sql = "INSERT INTO tbl_client11(client_name, client_age, client_username, client_option) VALUES(%s, %s, %s, %s)"
				data = (_name, _age, _username, _option )
				conn = mysql.connect()
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
				elif _option == "New":
					return render_template('co-borrower.html', client_type=client_type, clientId = _id)
					#return redirect('/client_type>/coborrower')
				return redirect('/')
			else:
				return "Couldn't register the client. Please check the details entered"
		elif client_type == "co-borrower's":
			_coborrowerName = request.form['inputName']
			_coborrowerAge = request.form['inputAge']
			_id = clientId
			if _coborrowerAge and _coborrowerName and request.method == 'POST':
				# saving in DB
				sql = "UPDATE tbl_client11 SET coborrower_name=%s, coborrower_age=%s WHERE id=%s"
				data = (_coborrowerName, _coborrowerAge, _id)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				return render_template("final.html")
			else:
				return "Couldn't register co-borrower entries. Please check the details entered"
	except Exception as e:
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
		if _choice == "1" or _choice == "Yes" or _choice == 'yes':
			flash('Please add co-borrower details')
			coborrower = "co-borrower's"
			return render_template('add.html', client_type=coborrower, clientId=_id)
		elif _choice == "0" or _choice == "NO" or _choice == "no" or _choice == "No":
			return redirect("/clientDetails/thankyou")
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
    app.run()
 