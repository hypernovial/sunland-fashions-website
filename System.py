from email import message
from os import access
from flask import *
app =Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login',methods =['POST','GET'])

def login():
    if request.method == 'POST':
        email =request.form['email']
        password =request.form['password']
        import pymysql
        connection =pymysql.connect(host='localhost',user='root',password='',database='kelvinprojectdb')

        sql ='select * from sign_up where email =%s and password =%s'
        cursor =connection.cursor()
        cursor.execute(sql,(email,password))
        # how many rows are returned after the above query is executed
        if cursor.rowcount ==0:
            return render_template('login.html', message ='wrong username/password')
        elif cursor.rowcount ==1:
            return redirect('/order')
        else:
            return render_template('login.html',message ='Something went wrong...')
    else:
        return render_template('login.html')


@app.route ('/signup',methods =['POST','GET'])
def register():
    if request.method =='POST':
        firstname =request.form['firstname']
        surname =request.form['surname']
        email =request.form['email']
        password1 =request.form['password1']
        password2 =request.form['password2']
        phone =request.form['phone']


        if len(password1) <8:
            return render_template('signup.html',message ="password must be 8 characters")
        elif password1 != password2:
            return render_template('signup.html',message ="password Do not match")
        else:
            import pymysql
            connection =pymysql.connect(host='localhost',user='root',password='',database='kelvinprojectdb')
            sql ="insert into sign_up(firstname,surname,email,password,phone) values(%s,%s,%s,%s,%s)"
            cursor =connection.cursor()
            cursor.execute(sql,(firstname,surname,email,password2,phone))
            connection.commit()
            return render_template('signup.html',message ='Account made successfuly')
    else:
        return render_template('signup.html')




@app.route('/order')
def route():
    import pymysql
    connection =pymysql.connect(host='localhost',user='root',password='',database='kelvinprojectdb')
    sql ='select * from orders order by price desc'
    cursor =connection.cursor()
    cursor.execute(sql)


    if cursor.rowcount == 0:
        return render_template('order.html', message ='The product is not available')
    else:
        rows =cursor.fetchall()# we retrieve all rows
        return render_template('order.html', rows=rows) #put rows in a var






# we create an m-pesa route
# daraja is presented through two url
# one url is for authentification,the other url is for SIM Tool Kit PUSH
import requests  #used to accsess the url
import datetime #used to the current computer time
import base64 #converting plain text to more computer readable format and transmit it over the internet
from requests.auth import HTTPBasicAuth #FOR AUTHENTICATION/login to API
@app.route('/mpesa', methods = ['POST','GET'])
def mpesa_payment():
        if request.method == 'POST':
            # we recieve the amount and phone
            phone = str(request.form['phone'])
            amount = str(request.form['amount'])
            # GENERATING THE ACCESS TOKEN
            # we generate below keys from daraja portal 
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"
            # url 1
            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
            #  you get a beare accsess token,its unique to every request
            data = r.json()
            access_token = "Bearer" + ' ' + data['access_token']
            print(access_token)

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919' #belongs to safcom
            business_short_code = "174379" #this is test paybill
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())#convert encoded it,compress it
            password = encoded.decode('utf-8')
            print(password)


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "account",
                "TransactionDesc": "account"
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }
            # url 2 tjhis send a payment prompt to your phone
            url = "httloaderIDPrimaryps://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL
            #  trigger the prompt
            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
            return 'Please Complete Payment in Your Phone'
        else:
            return redirect('order')
@app.route('/viewcustomers')
def view():
     import pymysql
     connection =pymysql.connect(host='localhost',user='root',password='',database='kelvinprojectdb')
     sql ='select * from customers order by name desc'
     cursor =connection.cursor()
     cursor.execute(sql)


     if cursor.rowcount == 0:
         return render_template('viewcustomers.html', message ='No customer')
     else:
         rows =cursor.fetchall()# we retrieve all rows
         return render_template('viewcustomers.html', rows=rows) #put rows in a variable





















app.run(debug=True)