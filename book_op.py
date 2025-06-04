from flask import Flask, render_template, redirect, request, url_for
import mysql.connector
from werkzeug.utils import secure_filename

# DB connection
con = mysql.connector.connect(
    host="localhost",
    username="root",
    password="Kittu@1611",
    database="MyBookStoreDB"
)

# Add Book (GET/POST)
def addBook():
    if request.method == "GET":
        sql = "SELECT * FROM category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("addBook.html", cats=cats)
    else:
        book_name = request.form["book_name"]
        author = request.form["author"]
        description = request.form["description"]
        price = request.form["price"]
        cid = request.form["cid"]

        # Handle book image upload
        f = request.files['image_url']
        filename = secure_filename(f.filename)
        filepath = "static/Images/" + filename
        f.save(filepath)
        img_path = "Images/" + filename

        cursor = con.cursor()
        sql = '''INSERT INTO book 
        (book_title, author, description, price, image_url, cid) 
        VALUES (%s, %s, %s, %s, %s, %s)'''
        val = (book_name, author, description, price, img_path, cid)
        cursor.execute(sql, val)
        con.commit()

        return redirect(url_for("showAllBooks"))

# Show All Books
def showAllBooks():
    sql = "SELECT * FROM cat_book_vw"
    cursor = con.cursor()
    cursor.execute(sql)
    books = cursor.fetchall()
    return render_template("showAllBooks.html", books=books)


def editBook(bookid):
    if request.method == "GET":
        sql = "SELECT * FROM book WHERE bookid=%s"
        val = (bookid,)
        cursor = con.cursor()
        cursor.execute(sql, val)
        book = cursor.fetchone()
        return render_template("editBook.html", book=book)
    else:
        book_title = request.form["book_title"]
        author = request.form["author"]
        description = request.form["description"]
        price = request.form["price"]
        image_url = request.form["image_url"]
        cid = request.form["cid"]
        
        sql = "UPDATE book SET book_title=%s, author=%s, description=%s, price=%s, image_url=%s, cid=%s WHERE bookid=%s"
        val = (book_title, author, description, price, image_url, cid, bookid)
        cursor = con.cursor()
        cursor.execute(sql, val)
        con.commit()
        return redirect(url_for("showAllBooks"))

# # Delete Book (GET/POST)
# def deleteBook(bookid):
#     if request.method == "GET":
#         # return render_template("deleteBookConfirmation.html", bookid=bookid)
#         return render_template("deleteCategory.html", bookid=bookid)
#     else:
#         action = request.form["action"]
#         if action == "Yes":
#             sql = "DELETE FROM book WHERE bookid=%s"
#             val = (bookid,)
#             cursor = con.cursor()
#             cursor.execute(sql, val)
#             con.commit()
#         return redirect(url_for("showAllBooks"))

def deleteBook(bookid):
    if request.method == "GET":
        return render_template("deleteCategory.html", bookid=bookid)
    else:
        action = request.form["action"]
        if action == "Yes":
            cursor = con.cursor()

            # Step 1: Remove the book from the cart table first
            cursor.execute("DELETE FROM cart WHERE bookid=%s", (bookid,))

            # Step 2: Now delete the book
            cursor.execute("DELETE FROM book WHERE bookid=%s", (bookid,))

            con.commit()
        return redirect(url_for("showAllBooks"))

