from flask import Flask
from flask import flash, render_template, request, redirect
import pymysql
from tables import Results
from app import app
from db_config import mysql
from jinja2 import Template
from flaskext.mysql import MySQL
from datetime import datetime
import time
import logging


#app.config["DEBUG"] = True
conn = mysql.connect()
cursor = conn.cursor()

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logger = logging.getLogger('root')
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

@app.route('/')
def db_connect():
	"""This function is the first entry point of the app"""
	try:
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_client")
		rows = cursor.fetchall()
		table = Results(rows)
		table.border = True
		client_type = "your"
		return render_template('add.html', table=table, client_type = client_type)
	except Exception as e:
		dateTimeObj = datetime.now()
		print  dateTimeObj
		logger.exception(e)		
		
		
	
@app.route('/blend/', methods=['POST','GET'])
def home_page():
	return redirect("/")

@app.route('/blend/<client_type>/', methods=['POST'])
@app.route('/blend/<client_type>/<int:clientId>', methods=['POST'])
def add_clientDetails(client_type="your", clientId=None):
	""" Workflow Task1: This function accepts client details and stores in the DB """ 

	client_type = client_type
	try:
		if client_type == "your":
			_name = request.form['inputName']
			_age = request.form['inputAge']
			_username = request.form['inputUsername']
			_option = request.form['inputOption']
			# saving in DB
			sql = "INSERT INTO tbl_client(client_name, client_age, client_username, client_option) VALUES(%s, %s, %s, %s)"
			data = (_name, _age, _username, _option )
			cursor.execute(sql, data)
			cursor.execute("SELECT * FROM tbl_client WHERE client_username = %s", _username)
			records = cursor.fetchone()
			_id = records[0]
			conn.commit()
			dateTimeObj = datetime.now()
			logger.info('%s Basic details for clientId=%d registered',dateTimeObj, _id)
			if _option == "Refinance":
				dateTimeObj = datetime.now()
				logger.info('%s Refinance option selected by clientId=%d ',dateTimeObj, _id)
				return render_template('refinance.html',client_type=client_type, clientId = _id)
			elif _option == "New Purchase":
				dateTimeObj = datetime.now()
				logger.info('%s New Purchase option selected by clientId=%d ',dateTimeObj, _id)
				return render_template('co-borrower.html', client_type=client_type, clientId = _id)
			return redirect('/')
		elif client_type == "co-borrower's":
			_coborrowerName = request.form['inputName']
			_coborrowerAge = request.form['inputAge']
			_id = clientId
			cursor.execute("SELECT * FROM tbl_client WHERE id=%s", _id)
			records = cursor.fetchone()
			if _coborrowerName.lower() == records[1].lower():
				dateTimeObj = datetime.now()
				logger.error('%s Error: Applicant name and co-borrower name entered same by clientId=%d ',dateTimeObj, _id)
				return render_template('add.html', client_type=client_type, clientId=_id, 
					errorMessage="You can not be the co-borrower as well, please re-enter the co-borrower details")
			elif  _coborrowerName.lower() != records[1].lower():
				sql = "UPDATE tbl_client SET coborrower_name=%s, coborrower_age=%s WHERE id=%s"
				data = (_coborrowerName, _coborrowerAge, _id)
				cursor.execute(sql, data)
				conn.commit()
				cursor.execute("SELECT * FROM tbl_client WHERE id=%s", _id)
				dateTimeObj = datetime.now()
				logger.error('%s Co-borrower details for clientId=%d registered ',dateTimeObj, _id)
				records = cursor.fetchone()
				""" Workflow Task4: Display ThankYou message and display client details entered in the application"""
				return render_template("final.html", value= records)
				#return redirect("/blend/clientDetails/thankYou", clientDetails=records)
	except Exception as e:
		if e[0] == 1062:
			return render_template('add.html', client_type = client_type, errorMessage="User with entered username already exists, please re-enter your details")
			print(e)
		else:
			dateTimeObj = datetime.now()
			logger.exception(dateTimeObj)		
	

@app.route('/blend/refinance/<int:clientId>', methods=['POST'])
def refinance_clientDetails(clientId):
	""" Workflow Task2:  This function accepts client deatils for Refinance application and stores in the DB"""

	try:
		_id = clientId
		_street = request.form['inputStreet']
		_city = request.form['inputCity']
		_state = request.form['inputState']
		_zipcode = request.form['inputZipcode']
		sql = "UPDATE tbl_client SET client_street=%s, client_city=%s, client_state=%s, client_zipcode=%s WHERE id=%s"
		data = (_street, _city, _state, _zipcode, _id,)
		cursor.execute(sql, data)
		conn.commit()
		dateTimeObj = datetime.now()
		logger.info("%s Refinance details for clientID=%d registered ",dateTimeObj, _id)
		return render_template('co-borrower.html', clientId=clientId)
	except Exception as e:
		dateTimeObj = datetime.now()
		logger.exception(dateTimeObj)		
	

@app.route('/blend/co-borrower/<int:clientId>', methods=['POST'])
def coborrower_clientDetails(clientId):
	""" Workflow Task3:  This function accepts client's choice to apply with a co-borrower or no and redirects to the next task """

	try:
		_id = clientId
		_choice = request.form['inputChoice']
		if _choice.lower() == "yes":
			dateTimeObj = datetime.now()
			logger.info("%s Redirecting to co-borrower's page (Task1) for clientID=%d ",dateTimeObj, _id)
			coborrower = "co-borrower's"
			return render_template('add.html', client_type=coborrower, clientId=_id)
		elif _choice.lower() == "no":
			dateTimeObj = datetime.now()
			logger.info("%s Opted out of co-borrower option by clientID=%d ",dateTimeObj, _id)
			cursor.execute("SELECT * FROM tbl_client WHERE id=%s", _id)
			records = cursor.fetchone()
			dateTimeObj = datetime.now()
			logger.info("%s Redirecting to ThankYou page for clientID=%d ",dateTimeObj, _id)
			return render_template('final.html', value=records)
			#return redirect("/blend/clientDetails/thankYou", value=records)
		else:
			return "Couldn't register the client. Please check the details entered"
	except Exception as e:
		dateTimeObj = datetime.now()
		logger.exception(dateTimeObj)		
	


@app.route('/blend/clientDetails/thankYou')
def close_db_connect():
	""" This function closes the connection with DB after dispaying the Thank You page and all the details entered by the client"""
	conn.close()
	cursor.close()


@app.errorhandler(404)
def page_not_found(error):
	dateTimeObj = datetime.now()
	logger.exception(dateTimeObj)		
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	dateTimeObj = datetime.now()
	logger.exception(dateTimeObj)		
	return render_template('500.html')

@app.errorhandler(405)
def internal_error(error):
	dateTimeObj = datetime.now()
	logger.exception(dateTimeObj)		
	return render_template('500.html')



if __name__ == "__main__":
	app.run(host="0.0.0.0")
 