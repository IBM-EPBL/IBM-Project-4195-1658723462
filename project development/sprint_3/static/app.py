from glob import escape
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
 

app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cnj20398;PWD=nUQprGGfXGDBd2kg",'','')

@app.route('/')

def login():
    return render_template('signin.html')

@app.route('/signin.html',methods = ['POST'])

def getUser():
    if request.method == 'POST':
        user = request.form['uname']
        password = request.form['upwd']
        sql = "SELECT * FROM CUSTOMERS where Email = ?"
        stmt = ibm_db.prepare(conn, sql)
        email = user
        # Explicitly bind parameters
        ibm_db.bind_param(stmt, 1,user)
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_assoc(stmt)
        pwd = dictionary["PASSWORD"]
        if password != pwd:
            return render_template('error.html')
        
        return render_template('base.html')
    

@app.route('/signup.html')

def putUser():
    return render_template('register1.html')   

@app.route('/signup.html',methods = ['POST'])

def storedUser():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        mail = request.form['mail']
        npwd = request.form['npwd']
        cpwd = request.form['cpwd']

        res = fname + lname + mail + npwd + cpwd

        if npwd != cpwd:
            return render_template('register1.html')

        sql = "INSERT INTO customers (FirstName,LastName,Email,password,confirmpassword) VALUES(?,?,?,?,?);"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, fname)
        ibm_db.bind_param(stmt, 2, lname)
        ibm_db.bind_param(stmt, 3, mail)
        ibm_db.bind_param(stmt, 4, npwd)
        ibm_db.bind_param(stmt, 5, cpwd)
        ibm_db.execute(stmt)
    return render_template('login.html')



    


if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)