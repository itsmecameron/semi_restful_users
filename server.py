from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)


@app.route("/users")
def index():
    mysql = connectToMySQL('semi-users')
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template("index.html", new_user = users)

#----------------------------------------------------

@app.route("/users/create_user") #create page
def create_user():
    mysql = connectToMySQL('semi-users')
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template("create_user.html", new_user = users)


@app.route("/users/create_user", methods=["POST"]) #button
def add_user():
    db = connectToMySQL('semi-users')
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s,%(em)s, NOW(), NOW());"

    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email"]
    }
    db = connectToMySQL('semi-users')
    id = db.query_db(query, data)
    return redirect("/users/" + str(id))
#------------------------------------------------------------read
@app.route("/users/<id>")
def read_user(id):
    mysql = connectToMySQL('semi-users')
    query = 'SELECT * FROM users WHERE ID =' + id + ";"
    user = mysql.query_db(query)
    return render_template("read1.html", new_user = user)

#----------------------------------------------------------------------

@app.route("/users/<id>/edit") #create page
def update_user(id):
    mysql = connectToMySQL('semi-users')
    query = 'SELECT * FROM users WHERE ID ='+ id +';'
    users = mysql.query_db(query)
    return render_template("edit.html", new_user = users)

@app.route("/users/update", methods=["POST"]) #button
def edit_user():
    mysql = connectToMySQL('semi-users')
    query = 'UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s, updated_at = now() Where id = %(id)s'
   
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email"],
        "id": request.form["id"]
    }
    mysql.query_db(query, data)
    # id = db.query_db(query, data)
    return redirect("/users")

@app.route("/users/<id>/delete")
def delete_user(id):
    mysql = connectToMySQL('semi-users')
    query = ('DELETE FROM users WHERE id = %(id)s')
    data = {
        "id": id
    }
    mysql.query_db(query, data)
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)

