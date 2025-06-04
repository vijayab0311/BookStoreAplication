from main import app
import category_op as cat
import book_op as book
import admin
import user



#----------------Category---------------------------------#
app.add_url_rule("/addCategory",
                 view_func=cat.addCategory,methods=["GET","POST"])
app.add_url_rule("/showAllCategories",
                 view_func=cat.showAllCategories)
app.add_url_rule("/editCategory/<cid>",view_func = cat.editCategory,
                 methods=["GET","POST"])
app.add_url_rule("/deleteCategory/<cid>",view_func = cat.deleteCategory,
                 methods=["GET","POST"])


#----------------Book(done)-------------------------------#
app.add_url_rule("/addBook", view_func=book.addBook, methods=["GET", "POST"])
app.add_url_rule("/showAllBooks", view_func=book.showAllBooks)
app.add_url_rule("/editBook/<bookid>", view_func=book.editBook, methods=["GET", "POST"])
app.add_url_rule("/deleteBook/<bookid>", view_func=book.deleteBook, methods=["GET", "POST"])

#------------ Admin ----------------------------------
app.add_url_rule("/adminLogin",view_func=admin.adminLogin,methods=["GET","POST"])
app.add_url_rule("/adminDashboard",view_func=admin.adminDashboard)
app.add_url_rule("/adminLogout",view_func=admin.adminLogout)



# --------------User Routes for Book Store-----------------------


# Homepage
app.add_url_rule("/", view_func=user.homepage)

# View books by category
app.add_url_rule("/view_books/<int:cid>", view_func=user.ViewBooks)

# Book details and add to cart
app.add_url_rule("/ViewDetails/<int:bookid>", view_func=user.ViewDetails, methods=["GET", "POST"])

# User registration
app.add_url_rule("/signup", view_func=user.signup, methods=["GET", "POST"])

# User login
app.add_url_rule("/login", view_func=user.login, methods=["GET", "POST"])

# User logout
app.add_url_rule("/logout", view_func=user.logout)

# View cart
app.add_url_rule("/cart", view_func=user.showCart)

# Payment route
app.add_url_rule("/makepayment", view_func=user. makepayment, methods=["GET", "POST"])
# app.add_url_rule("/PaymentSuccess", view_func=user. makepayment, methods=["GET", "POST"])

app.add_url_rule('/offers', view_func=user.offers ,methods=["GET", "POST"])
app.add_url_rule('/aboutus', view_func=user.about_us ,methods=["GET", "POST"])

# app.add_url_rule("/remove_from_cart/<int:cart_id>", view_func=user. remove_from_cart, methods=["GET", "POST"])
app.add_url_rule('/removeCart/<int:cartid>',  view_func=user. removeCart, methods=["GET", "POST"])

app.add_url_rule('/myorders', view_func=user.my_orders, methods=["GET", "POST"])