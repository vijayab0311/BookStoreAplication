from flask import Flask, render_template, redirect, request, url_for, session
import mysql.connector
from flask import Flask
from flask_mysqldb import MySQL


# Database Connection
con = mysql.connector.connect(host="localhost", username="root", password="Kittu@1611", database="MyBookStoreDB")

# Home Page
def homepage():
    #---------Books------------
    sql = "select * from cat_book_vw"
    cursor = con.cursor()
    cursor.execute(sql)
    books = cursor.fetchall()
    #--------Categories----------
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    categories = cursor.fetchall()
    return render_template("homepage.html", books=books, categories=categories)


def offers():
    # If you have any dynamic data to pass to the template, you can do so here.
    return render_template('offers.html')

def about_us():
    return render_template("aboutus.html")

# View Books by Category
def ViewBooks(cid):
    sql = "select * from cat_book_vw where cid=%s"
    val = (cid,)
    cursor = con.cursor()
    cursor.execute(sql, val)
    books = cursor.fetchall()
    #--------Categories----------
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    categories = cursor.fetchall()
    return render_template("homepage.html", books=books, categories=categories)

# View Book Details and Add to Cart
def ViewDetails(bookid):
    if request.method == "GET":
        sql = "select * from cat_book_vw where bookid=%s"
        val = (bookid,)
        cursor = con.cursor()
        cursor.execute(sql, val)
        book = cursor.fetchone()
        #--------Categories----------
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        categories = cursor.fetchall()
        return render_template("ViewDetails.html", book=book, categories=categories)
    else:
        if "username" in session:
            username = session["username"]
            quantity = request.form["quantity"]
            bookid = request.form.get('bookid')
            sql = "insert into cart (username, bookid, quantity, order_date) values (%s, %s, %s, now())"
            val = (username, bookid, quantity)
            cursor = con.cursor()
            cursor.execute(sql, val)
            con.commit()
            return redirect(url_for("showCart"))
        else:
            print("Not logged in")
            return redirect(url_for("login"))

def showCart():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    sql = """
        SELECT c.cartid, b.bookid, b.book_title, b.author, b.price, c.quantity, (b.price * c.quantity) AS total
        FROM cart c
        INNER JOIN book b ON c.bookid = b.bookid
        WHERE c.username = %s
    """
    cursor = con.cursor()
    cursor.execute(sql, (username,))
    cart_items = cursor.fetchall()

    grand_total = sum(item[6] for item in cart_items)  # Total of all items

    session["total"] = grand_total  # Store in session for payment use

    return render_template("showCart.html", cart_items=cart_items, grand_total=grand_total)



def removeCart(cartid):
    if request.method == "GET":
        return render_template("removeCart.html", cartid=cartid)
    else:
        action = request.form["action"]
        if action == "Yes":
            sql = "DELETE FROM cart WHERE cartid = %s"
            val = (cartid,)
            cursor = con.cursor()
            cursor.execute(sql, val)
            con.commit()
        return redirect(url_for("showCart"))
    
    
def clearCart():
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not logged in

    username = session['username']
    
    # Delete all items in the cart for the logged-in user
    cursor = con.cursor()
    cursor.execute("DELETE FROM cart WHERE username = %s", (username,))
    con.commit()
    
    return redirect(url_for("showCart"))  # Redirect to the updated cart page    



# Make Payment
def makepayment():
    if request.method == "GET":
        return render_template("makepayment.html")
    else:
        card_no = request.form["card_no"]
        cvv = request.form["cvv"]
        expiry = request.form["expiry"]
        sql = "select count(*) from payment where cardno=%s and cvv=%s and expiry=%s"
        val = (card_no, cvv, expiry)
        cursor = con.cursor()
        cursor.execute(sql, val)
        count = int(cursor.fetchone()[0])

        if count == 1:
            # Valid Card, Proceed Payment
            amount = session["total"]
            sql1 = "update payment set balance = balance - %s where cardno = %s"  # Buyer
            sql2 = "update payment set balance = balance + %s where cardno = 222"  # Store Owner (fixed card)
            val1 = (amount, card_no)
            val2 = (amount,)
            cursor.execute(sql1, val1)
            cursor.execute(sql2, val2)
            con.commit()
            return render_template("PaymentSuccess.html")
        else:
            return render_template("PaymentFailed.html")
        
     

        
def my_orders():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    cursor = con.cursor()  

    cursor.execute("SELECT * FROM orders WHERE username = %s ORDER BY order_date DESC", (username,))
    orders = cursor.fetchall()

    all_order_items = {}
    for order in orders:
        order_id = order[0]
        cursor.execute("""
            SELECT oi.*, b.book_title FROM order_items oi 
            JOIN Book b ON oi.bookid = b.bookid 
            WHERE oi.order_id = %s
        """, (order_id,))
        all_order_items[order_id] = cursor.fetchall()

    cursor.close()
    return render_template('myorders.html', orders=orders, order_items=all_order_items)


# Login
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]

        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM UserInfo WHERE username=%s AND password=%s", (uname, pwd))
        is_user = cursor.fetchone()[0]

        if is_user == 1:
            session["username"] = uname
            return redirect(url_for("homepage"))
        else:
            return render_template("login.html", message="Invalid credentials")


# Logout
def logout():
    session.clear()
    return redirect(url_for("homepage"))


# # Signup user
def signup():
    if request.method == "GET":
        message = request.args.get("message", "")
        return render_template("signup.html", message=message)
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]

        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM userinfo WHERE username=%s", (uname,))
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("INSERT INTO userinfo (username, password) VALUES (%s, %s)", (uname, pwd))
            con.commit()
            return redirect(url_for("homepage"))
        else:
            return redirect(url_for("signup", message="Username already exists!"))
        


