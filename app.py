from flask import Flask,render_template, flash, redirect, url_for,request, session, logging
from passlib.hash import sha256_crypt
import cx_Oracle

app = Flask(__name__)
conn = cx_Oracle.connect('sude/pass')

@app.route("/")
def index():
        cur = conn.cursor()
        cur.execute("SELECT id,title,author FROM articles")
        articles = cur.fetchall()
        cur.close()
        if cur.rowcount > 0 :
            return render_template('home.html', articles=articles)
        return render_template('home.html')

@app.route("/about")
def aboutfunc():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            cpassword = request.form['cpassword']
            cur = conn.cursor()
            
            cur.execute('select * from user_info where email = :a',{'a' : email})
            cur.fetchall()
            if cur.rowcount > 0 :
                flash('Email Already Exists')
                return redirect(url_for('register'))
            cur.execute('select * from user_info where username = :a',{'a' : username})
            cur.fetchall()
            if cur.rowcount > 0 :
                flash('Username Already Exists')
                return redirect(url_for('register'))
            elif password != cpassword:
                flash('Passwords do not Match')
                return redirect(url_for('register'))
            else:
                cur.execute('insert into user_info(name,email,username,password,register_date) values(:a,:b,:c,:d,sysdate)',{'a' : name,'b' : email,'c' : username,'d' : sha256_crypt.encrypt(str(request.form['password']))})
                conn.commit()
                cur.close()
                flash('You are now registered and can log in', 'success')
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        username = request.form['username']
        password_candidate = request.form['password']

        cur = conn.cursor()
        cur.execute('select password from user_info where username= :a',{'a' : username})
        password = cur.fetchone()
        if cur.rowcount == 0 :
                flash('No Such username')
                return redirect(url_for('login'))

        if sha256_crypt.verify(password_candidate,password[0]):
            session['username'] = username
            session['logged_in'] = True
            cur.close()
            return redirect(url_for('dashboard'))
        else:
            flash('Password Does not Match')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route("/dashboard")
def dashboard():
    if session:
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles where author = :a",{'a': session['username']})
        articles = cur.fetchall()
        cur.close()
        if cur.rowcount > 0 :
            return render_template('dashboard.html', articles=articles)
        else:
            flash("You don't have any articles yet!")
            return render_template('dashboard.html')
    else:
        flash("You are not Logged in")
        return redirect(url_for('login'))

@app.route("/add_article",methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        body = request.form['body']
        title = request.form['title']
        cur = conn.cursor()
        cur.execute('insert into articles(title,author,body,post_date) values(:title,:author, utl_raw.cast_to_raw(:a),sysdate)',{'a' : body,'title':title,'author':session['username']})
        conn.commit()
        flash("Article added")
        return redirect(url_for('dashboard'))
    return render_template("add_article.html")

@app.route("/article/<string:id>")
def article(id):
    cur = conn.cursor()
    cur.execute("SELECT id,title,author,UTL_RAW.CAST_TO_VARCHAR2(body),post_date FROM articles where id= :id",{'id' : id})
    article = cur.fetchall()
    return render_template("article.html",article = article)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))



if __name__=="__main__":
    app.secret_key='testkey'
    app.run(debug=True,port=80,host='0.0.0.0')
