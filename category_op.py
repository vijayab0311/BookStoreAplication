from flask import Flask, render_template, redirect, request, url_for
import mysql.connector

# Database connection
con = mysql.connector.connect(
    host="localhost",
    username="root",
    password="Kittu@1611",
    database="MyBookStoreDB"
)

# Add Book Category (GET/POST)
def addCategory():
    if request.method == "GET":
        return render_template("addCategory.html")
    else:
        cat_name = request.form["cat_name"]
        cursor = con.cursor()
        sql = "INSERT INTO category (cat_name) VALUES (%s)"
        val = (cat_name,)
        cursor.execute(sql, val)
        con.commit()
        return redirect(url_for("showAllCategories"))

# Show All Book Categories
def showAllCategories():
    sql = "SELECT * FROM category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    return render_template("showAllCategories.html", cats=cats)

# Edit Book Category (GET/POST)
def editCategory(cid):
    if request.method == "GET":
        sql = "SELECT * FROM category WHERE cid=%s"
        val = (cid,)
        cursor = con.cursor()
        cursor.execute(sql, val)
        cat = cursor.fetchone()
        return render_template("editCategory.html", cat=cat)
    else:
        cat_name = request.form["cat_name"]
        sql = "UPDATE category SET cat_name=%s WHERE cid=%s"
        val = (cat_name, cid)
        cursor = con.cursor()
        cursor.execute(sql, val)
        con.commit()
        return redirect(url_for("showAllCategories"))

# Delete Book Category (GET/POST)
# def deleteCategory(cid):
#     if request.method == "GET":
#         return render_template("deleteConfirmation.html", cid=cid)
#     else:
#         action = request.form["action"]
#         if action == "Yes":
#             sql = "DELETE FROM category WHERE cid=%s"
#             val = (cid,)
#             cursor = con.cursor()
#             cursor.execute(sql, val)
#             con.commit()
#         return redirect(url_for("showAllCategories"))

# def deleteCategory(cid):
#     if request.method == "GET":
#         return render_template("deleteCategory.html", cid=cid)
#     else:
#         action = request.form["action"]
#         if action == "Yes":
#             cursor = con.cursor()

#             # Step 1: Delete related books first
#             cursor.execute("DELETE FROM book WHERE cid = %s", (cid,))

#             # Step 2: Delete the category
#             cursor.execute("DELETE FROM category WHERE cid = %s", (cid,))

#             con.commit()
#         return redirect(url_for("showAllCategories"))

def deleteCategory(cid):
    if request.method == "GET":
        return render_template("deleteCategory.html", cid=cid)
    else:
        action = request.form["action"]
        if action == "Yes":
            cursor = con.cursor()

            # Step 1: Get all book ids for this category
            cursor.execute("SELECT bookid FROM book WHERE cid = %s", (cid,))
            book_ids = cursor.fetchall()

            # Step 2: Delete related rows from cart for those book ids
            for (bookid,) in book_ids:
                cursor.execute("DELETE FROM cart WHERE bookid = %s", (bookid,))

            # Step 3: Delete related books
            cursor.execute("DELETE FROM book WHERE cid = %s", (cid,))

            # Step 4: Delete the category
            cursor.execute("DELETE FROM category WHERE cid = %s", (cid,))

            con.commit()
        return redirect(url_for("showAllCategories"))


    

