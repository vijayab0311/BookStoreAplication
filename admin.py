from flask import Flask,render_template,redirect,request,url_for,session
import mysql.connector

con = mysql.connector.connect(host="localhost",username="root",password="Kittu@1611",database="MyCakeShopdb")

def adminLogin():
    if request.method == "GET":
        return render_template("adminLogin.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        sql = '''
          select count(*) from adminLogin where username=%s and password=%s'''
        val = (username,password)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        count = int(count[0])
        if count == 0:
            return redirect(url_for("adminLogin"))
        else:
            session["adminuser"] =username
            return redirect(url_for("adminDashboard"))
        
def adminDashboard():
    if "adminuser" in session:
        return render_template("adminDashboard.html")
    else:
        return redirect(url_for("adminLogin"))



def adminLogout():
    session.clear()
    return redirect(url_for("adminLogin"))