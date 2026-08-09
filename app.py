from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_email", methods=["GET","POST"])
def add_one_email():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into email (from,to,subject,content,status,created_at) values (:from,:to,:subject,:content,:status,:created_at)",hey)
        user = query_db('select * from email')

        return render_template("emailform.html", emails=user, one_user=one_user, the_title="add new email")


    user = query_db('select * from email')
    one_user = query_db("select * from email limit 1", one=True)
    return render_template("emailform.html", emails=user, one_user=one_user, the_title="add new email")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (email,password,country_id,phone,username) values (:email,:password,:country_id,:phone,:username)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['email','password','country_id','phone','username']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['email','password','country_id','phone','username']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['email','password','country_id','phone','username']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_image", methods=["GET","POST"])
def add_one_image():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslesemail= query_db("select * from email")

        one_user = query_db("insert into image (email_id,pic,order) values (:email_id,:pic,:order)",hey)
        user = query_db('select * from image')

        return render_template("imageform.html", images=user, one_user=one_user, the_title="add new image", touslesemail=touslesemail)


    touslesemail= query_db("select * from email")

    user = query_db('select * from image')
    one_user = query_db("select * from image limit 1", one=True)
    return render_template("imageform.html", images=user, one_user=one_user, the_title="add new image", touslesemail=touslesemail)

@app.route("/add_one_attachment", methods=["GET","POST"])
def add_one_attachment():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['attachment']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["attachment"]=uploaded_file.filename


        touslesemail= query_db("select * from email")

        one_user = query_db("insert into attachment (email_id,attachment,order) values (:email_id,:attachment,:order)",hey)
        user = query_db('select * from attachment')

        return render_template("attachmentform.html", attachments=user, one_user=one_user, the_title="add new attachment", touslesemail=touslesemail)


    touslesemail= query_db("select * from email")

    user = query_db('select * from attachment')
    one_user = query_db("select * from attachment limit 1", one=True)
    return render_template("attachmentform.html", attachments=user, one_user=one_user, the_title="add new attachment", touslesemail=touslesemail)

@app.route("/add_one_text", methods=["GET","POST"])
def add_one_text():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesemail= query_db("select * from email")

        one_user = query_db("insert into text (police,taille,couleur,email_id,order) values (:police,:taille,:couleur,:email_id,:order)",hey)
        user = query_db('select * from text')

        return render_template("textform.html", texts=user, one_user=one_user, the_title="add new text", touslesemail=touslesemail)


    touslesemail= query_db("select * from email")

    user = query_db('select * from text')
    one_user = query_db("select * from text limit 1", one=True)
    return render_template("textform.html", texts=user, one_user=one_user, the_title="add new text", touslesemail=touslesemail)

