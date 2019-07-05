from flask import Flask
from flask import render_template
from flask import request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:password@localhost/mydatabase2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Teacher1(db.Model):
	S_No=db.Column(db.Integer,primary_key=True)
	department_name = db.Column(db.String(80), nullable=False)
	is_hod = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
	teaching_subjects = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

	def __repr__(self):
		return 'success'
class students1(db.Model):
	roll_no=db.Column(db.Integer,primary_key=True)
	student_name = db.Column(db.String(80), nullable=False)
	is_monitor = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
	studying_subjects = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

	def __repr__(self):
		return 'success'
@app.route("/")
def start():
	return render_template("start.html")		
@app.route("/students",methods=["GET","POST"])
def students():
	students=[]
	students=students1.query.all()
	return render_template("students.html",students=students)
@app.route("/students/adds", methods=["GET", "POST"])
def adds():
	students = []
	if request.form:
		student=students1(student_name=request.form.get("student_name"),is_monitor=request.form.get("is_monitor"),studying_subjects=request.form.get("studying_subjects"))
		db.session.add(student)
		db.session.commit()
		return redirect('/students')

@app.route("/students/updates", methods=["GET", "POST"])
def updates():
	try:
		if request.method == "POST":
			data = request.get_json()
			print(data)
			Id=data.get('roll_no')
			s_name=request.json['student_name']
			monitor=request.json['is_monitor']
			subjects=request.json['studying_subjects']
			obj = students1.query.filter_by(roll_no=Id).first()
			obj.student_name = s_name
			obj.is_monitor = monitor
			obj.studying_subjects =subjects
			db.session.commit()                                          
			return jsonify(result)
	except:
		return "Error updating."
	
@app.route("/students/deletes/<int:roll_no>", methods=["GET", "POST"])
def deletes(roll_no):
	student = students1.query.filter_by(roll_no=roll_no).delete()
	db.session.commit()
	return redirect("/students")

@app.route("/teachers",methods=["GET","POST"])
def home():
	teachers=[]
	teachers=Teacher1.query.all()
	return render_template("teachers.html",teachers=teachers)
@app.route("/teachers/add", methods=["GET", "POST"])
def add():
	teachers = []
	if request.form:
		teacher=Teacher1(department_name=request.form.get("department_name"),is_hod=request.form.get("is_hod"),teaching_subjects=request.form.get("teaching_subjects"))
		db.session.add(teacher)
		db.session.commit()
		return redirect('/teachers')

@app.route("/teachers/update", methods=["GET", "POST"])
def update():
	try:
		if request.method == "POST":
			data = request.get_json()
			print(data)
			Id=data.get('s_no')
			d_name=request.json['department_name']
			hod=request.json['is_hod']
			sub=request.json['teaching_subjects']
			obj = Teacher1.query.filter_by(S_No=Id).first()
			obj.department_name = d_name
			obj.is_hod = hod
			obj.teaching_subjects =sub
			db.session.commit()
			resp = jsonify(success=True)
			return resp
	except:
		return "Error updating user."
	
@app.route("/teachers/delete/<int:S_No>", methods=["GET", "POST"])
def delete(S_No):
	teacher = Teacher1.query.filter_by(S_No=S_No).delete()
	db.session.commit()
	return redirect("/teachers")
if __name__=="__main__":
	db.create_all()
	app.run(debug=True)



