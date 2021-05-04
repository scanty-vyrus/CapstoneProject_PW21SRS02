#------------------------------------------------database------------------------------------------------------
import sqlite3
conn = sqlite3.connect('new.db')
cur = conn.cursor()
print('connection')
try:
   cur.execute('''create table ip_data (
           id integer primary key autoincrement ,
           ip varchar(100), 
           day varchar(20),
           CaloriesBurned varchar(20),
           steps varchar(20),
           distance varchar(20),
           heartbeat varchar(20),
           TotalMinutesAsleep varchar(20),
           TotalTimeinBed varchar(20),
           showdata int)''')

   cur.execute('''CREATE TABLE users (
   id integer Primary key  AUTOINCREMENT,
   name varchar(20),
   email varchar(50),
   password varchar(20),
   gender varchar(10),
   age varchar(50),
   ip varchar(100),
   admin int )''')
   pass
except:
    print("table already created")  # Import socket module
#------------------------------------------------database---------------------------------------------------------------

from flask import Flask,render_template, url_for,request, flash, redirect, session
import os
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = '881e69e15e7a528830975467b9d87a98'

#-------------------------------------home_page-------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
def index():
   if len(sys.argv) > 1:
       return render_template('index.html', day=sys.argv[1],CaloriesBurned=sys.argv[2],steps=sys.argv[3]
                              ,distance=sys.argv[4],heartbeat=sys.argv[5],TotalMinutesAsleep=sys.argv[6],
                              TotalTimeinBed=sys.argv[7],
                              ip=sys.argv[8])
   return render_template('home.html')
import json

@app.route('/yes',methods = ['POST', 'GET'])
def yes():
   conn = sqlite3.connect('new.db')
   cur = conn.cursor()
   if request.method == 'POST':
      #print("this is msg",request.form['msg'])
      print("this is ip",request.form['ip'])
      #msg = request.form['msg']
      ip = request.form['ip']
      #msg encrptionip varchar(100),
      # msg = json.loads(msg)
      day = request.form["day"]
      CaloriesBurned = request.form["CaloriesBurned"]
      steps = request.form["steps"]
      distance = request.form["distance"]
      heartbeat = request.form["heartbeat"]
      TotalMinutesAsleep = request.form["TotalMinutesAsleep"]
      TotalTimeinBed = request.form["TotalTimeinBed"]
      print(day,CaloriesBurned,steps,distance,heartbeat,TotalMinutesAsleep,TotalTimeinBed)
      cur.execute('''insert into ip_data (ip,day,CaloriesBurned,steps,distance,heartbeat,TotalMinutesAsleep,TotalTimeinBed,showdata) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(ip,day,CaloriesBurned,steps,distance,heartbeat,TotalMinutesAsleep,TotalTimeinBed,1))
      conn.commit()
      print('data inserted')
      shutdown()
      os.system("taskkill /im chrome.exe /f")
      os.system("taskkill /im msedge.exe /f")
   return render_template('index.html')

@app.route('/no')
def no():
    print('exit')
    shutdown()
    os.system("taskkill /im chrome.exe /f")
    os.system("taskkill /im msedge.exe /f")
    return index()

#-------------------------------------home_page-------------------------------------------------------------------------

#-------------------------------------about_page------------------------------------------------------------------------
@app.route("/about")
def about():
   return render_template('about.html')
#-------------------------------------about_page------------------------------------------------------------------------
email = ''
@app.route('/showdata',methods = ['POST', 'GET'])
def showdata():
   global email
   conn = sqlite3.connect('new.db')
   cur = conn.cursor()
   print('email = ', email)
   cur.execute('select ip from users where email = "{}"'.format(email))
   ip = cur.fetchone()
   print('ip = ',ip[0])
   cur.execute('update ip_data set showdata = 1 where ip = "{}"'.format(ip[0]))
   conn.commit()
   cur.execute('SELECT * FROM ip_data where ip = "{}"'.format(ip[0]))
   s = cur.fetchall()
   print(s)
   count = cur.execute('SELECT * FROM users WHERE email = "%s"' % (email))
   print(count)
   # conn.commit()
   # cur.close()
   l = len(cur.fetchall())
   print('l = ', l)
   if l > 0:
      flash( f'Successfully Logged in' )
      #decreption
      return render_template('user_account.html',b = s,admin=0)
   return render_template('user_login.html')

@app.route('/hidedata',methods = ['POST', 'GET'])
def hidedata():
   global email
   conn = sqlite3.connect('new.db')
   cur = conn.cursor()
   print('email = ',email)
   cur.execute('select ip from users where email = "{}"'.format(email))
   ip = cur.fetchone()
   print('ip = ',ip[0])
   cur.execute('update ip_data set showdata = 0 where ip = "{}"'.format(ip[0]))
   conn.commit()
   cur.execute('SELECT * FROM ip_data where ip = "{}"'.format(ip[0]))
   s = cur.fetchall()
   print(s)
   count = cur.execute('SELECT * FROM users WHERE email = "%s"' % (email))
   print(count)
   # conn.commit()
   # cur.close()
   l = len(cur.fetchall())
   print('l = ', l)
   if l > 0:
      flash( f'Successfully Logged in' )
      #decreption
      return render_template('user_account.html',b = s,admin=0)
   return render_template('user_login.html')



#-------------------------------------user_login_page-------------------------------------------------------------------
@app.route('/user_login',methods = ['POST', 'GET'])
def user_login():
   global email
   conn = sqlite3.connect('new.db')
   cur = conn.cursor()
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['psw']
      cur.execute('SELECT * FROM users')
      print(cur.fetchall())
      print(email,password)
      count = cur.execute('SELECT * FROM users WHERE email = "%s" AND password = "%s"' % (email, password))
      print(count)
      #conn.commit()
      #cur.close()
      l = len(cur.fetchall())
      print('l = ',l)
      if email == 'admin':
         cur.execute('SELECT * FROM ip_data where showdata = 1')
         s = cur.fetchall()
         print('im admin ',s)
         flash(f'Successfully Logged in')
         # decreption
         return render_template('user_account.html', b=s , admin = 1)
      else:
         cur.execute('select ip from users where email = "{}"'.format(email))
         ip = cur.fetchone()
         print('ip = ',ip[0])
         cur.execute('SELECT * FROM ip_data where ip = "{}"'.format(ip[0]))
         s = cur.fetchall()
         print(s)
         if l > 0:
            flash( f'Successfully Logged in' )
            #decreption
            return render_template('user_account.html',b = s,admin = 0)
         else:
            print('hello')
            flash( f'Invalid Email and Password!' )
   return render_template('user_login.html')

# -------------------------------------user_register_page-------------------------------------------------------------------------
@app.route('/user_register', methods=['POST', 'GET'])
def user_register():
   conn = sqlite3.connect('new.db')
   cur = conn.cursor()
   if request.method == 'POST':
      name = request.form['uname']
      email = request.form['email']
      password = request.form['psw']
      gender = request.form['gender']
      age = request.form['age']
      ip = request.form['IP']
      admin = request.form['admin']
      #showdata = request.form['showdata']
      cur.execute("insert into users(name,email,password,gender,age,IP,admin) values ('%s','%s','%s','%s','%s','%s','%s')" % (name, email, password, gender, age,ip,admin))
      conn.commit()
      # cur.close()
      print('data inserted')
      return redirect(url_for('user_login'))
   return render_template('user_register.html')
# -------------------------------------user_register_page-------------------------------------------------------------------------

# -------------------------------------user_account_page-------------------------------------------------------------------------
@app.route('/user_account',methods = ['POST', 'GET'])
def user_account():
   return render_template('user_account.html')
# -------------------------------------user_account_page-------------------------------------------------------------------------

# -------------------------------------user_logout_page-------------------------------------------------------------------------
@app.route("/logout")
def logout():
   session['logged_in'] = False
   return index()

from flask import request
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
# -------------------------------------user_logout_page-------------------------------------------------------------------------

if __name__ == '__main__':
   app.secret_key = os.urandom(12)
   app.run(debug=True)
   conn = sqlite3.connect('new.db')
   cur = conn.cursor()
   