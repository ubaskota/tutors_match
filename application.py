import os

from flask import Flask, render_template, session, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response



@app.route("/")
def index():
	#flights = db.execute("SELECT * FROM login_signup").fetchall()
	session['login'] = None
	#message = None
	return render_template("homepage.html")



@app.route("/registration_signup", methods = ["POST", "GET"])
def registration_login():

	first_name = request.form.get('f_name')
	last_name = request.form.get('l_name')
	j_num = request.form.get('j_num')
	email = request.form.get('email')
	password = request.form.get('psw')
	re_password = request.form.get('re_psw')

	message = None
	if request.method == "POST":

	#check if the password is valid and the length of j_number is equal to 9
		if len(password) < 5 or len(password) > 30 or len(j_num) != 9:
			message = "Invalid password or J#"
			return render_template("signup.html", message=message)

		#check if the password is equal to the re-written password
		elif password != re_password:
			message = "Please, make sure your passwords are same!"
			return render_template("signup.html", message=message)
			
		elif "@" not in email or ".com" not in email:
			message = "Invalid address! Pleae enter the correct email."
			return render_template("signup.html", message=message)

		else:
			if db.execute("SELECT j_num FROM login_signup WHERE j_num=:j_num",{'j_num': j_num}).rowcount == 0:
				db.execute('INSERT INTO login_signup (first_name, last_name, j_num, email, password) VALUES(:first_name, :last_name,\
					:j_num, :email, :password)',{"first_name":first_name, "last_name":last_name, "j_num":j_num, "email":email, "password":password})
				db.commit()
				session['login'] = True

				message = "Congratulations %s , Account successfully created!!!" % (first_name)
				return render_template("registered.html", message=message)
			else:
				message = "The account already exists!!! Please login!"
				return render_template("signup.html", message=message)
	else:
		return render_template("signup.html")
		
		
		
		



@app.route("/registration_signup_tutor", methods = ["POST", "GET"])
def registration_login_tutor():

	first_name = request.form.get('f_name')
	last_name = request.form.get('l_name')
	j_num = request.form.get('j_num')
	email = request.form.get('email')
	secretcode = request.form.get('secretcode')
	uniquecode = request.form.get('uniquecode')
	password = request.form.get('psw')
	re_password = request.form.get('re_psw')

	message = None
	if request.method == "POST":

	#check if the password is valid and the length of j_number is equal to 9
		if len(password) < 5 or len(password) > 30 or len(j_num) != 9:
			message = "Invalid password or J#"
			return render_template("signUpTutor.html", message=message)

		#check if the password is equal to the re-written password
		elif password != re_password:
			message = "Please, make sure your passwords are same!"
			return render_template("signUpTutor.html", message=message)
			
		elif "@" not in email or ".com" not in email:
			message = "Invalid address! Pleae enter the correct email."
			return render_template("signUpTutor.html", message=message)

		else:
			if db.execute("SELECT j_num FROM login_signup WHERE j_num=:j_num",{'j_num': j_num}).rowcount == 0 and \
			db.execute("SELECT secretcode, uniquecode FROM student_code JOIN login_signup_tutor ON student_code.uniquecode = login_signup_tutor.secretcode", {'uniquecode':uniquecode, 'secretcode':secretcode}).rowcount == 1:
				db.execute('INSERT INTO login_signup_tutor (first_name, last_name, j_num, secretcode, email, password) VALUES(:first_name, :last_name,\
					:j_num, :secretcode, :email, :password)',{"first_name":first_name, "last_name":last_name, "j_num":j_num, "secretcode":secretcode, "email":email, "password":password})
				db.commit()
				session['login'] = True

				message = "Congratulations %s , Account successfully created!!!" % (first_name)
				return render_template("registered.html", message=message)
			else:
				message = "The account already exists or invalid secret code. Make sure your code is right."
				return render_template("signUpTutor.html", message=message)
	else:
		return render_template("signUpTutor.html")

				
				
				


#This method can be useful when we don't use the "POST" and "GET" method that is mentioned below.
"""@app.route("/login", methods = ["POST", "GET"])
def login():
	return render_template("login.html")"""



@app.route("/login_submit", methods = ["POST", "GET"])
def login_submit():

	message = None
	if request.method == "POST":
		l_email = request.form.get('email')
		l_password = request.form.get('password')

		if db.execute("SELECT * FROM login_signup WHERE email=:email and password=:password", {'email':l_email, 'password':l_password}).fetchone():
			username = db.execute("SELECT first_name FROM login_signup WHERE email=:email", {'email':l_email}).fetchone()
			message = "Welcome %s" % (username)
			session['login'] = True
			return render_template("dashboardOne.html", message=message)

		else:
			message = "Incorrect Password or the the username doesn't exist."
			return render_template("login.html", message=message)
	else:
		return render_template("login.html")







@app.route("/admin_login", methods = ["POST", "GET"])
def admin_login():

	message = "This page is used by admins only. ADMINS ONLY!!!"
	if request.method == "POST":
		first_name = request.form.get('first_name')
		j_num = request.form.get('login_id')
		password = request.form.get('password')

		if db.execute("SELECT * FROM admin WHERE first_name=:first_name and j_num=:j_num and password=:password", {'first_name':first_name, 'j_num':j_num, 'password':password}).fetchone():
			message = "Welcome Adminstrator!!!"
			session['login'] = True
			return render_template("adminDashboard.html", message=message)

		else:
			message = "Incorrect Password or the the username doesn't exist."
			return render_template("adminLanding.html", message=message)
	else:
		return render_template("adminLanding.html", message=message)




#
#db.execute('INSERT INTO login_signup (first_name, last_name, j_num, email, password) VALUES(:first_name, :last_name,\
#	:j_num, :email, :password)',{"first_name":first_name, "last_name":last_name, "j_num":j_num, "email":email, "password":password})


@app.route("/view_credentials", methods = ["POST", "GET"])
def view_credentials():
	
	if request.method == "GET":
#		if request.form['submit_button'] == 'View Admin':
#		output = db.execute('SELECT * FROM admin').fetchall()
#		return render_template("adminDashboard.html", output=output)
#		elif request.form['submit_button'] == 'View Tutor':
		tutors = db.execute('SELECT first_name, last_name, j_num, email FROM login_signup_tutor').fetchall()
		admins = db.execute('SELECT first_name, j_num FROM admin').fetchall()
		return render_template("adminDashboard.html", tutors=tutors, admins=admins)




@app.route("/success")
def success_message():
	message = "Congratulations, you successfully created an account!!!"
	return render_template("registered.html", message = message)


@app.route("/contact")
def contact_us():
	return render_template("contactus.html")

@app.route("/logout")
def logout():
	message = "You have been successfully logged out!"
	session['login'] = False
	flash("You are logged out.")
	return render_template("homepage.html", message=message)

