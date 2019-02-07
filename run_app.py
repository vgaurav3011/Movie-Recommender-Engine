import os
from flask import Flask, session, redirect, jsonify, url_for, escape, request, flash, render_template
import models as dbHandler
import sqlite3 as db
import mysql.connector,sys
import calendar
import datetime
from mysql.connector import Error

from random import randint

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = b'_5#y2L"F4Qvchsjnbdk8z\ncgxhjsknck\xec]/'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            if username == 'cashier' and password == 'cashier':
                res = runQuery('call delete_old()')
                return render_template('cashier.html')
            if username == 'manager' and password == 'manager':
                res = runQuery('call delete_old()')
                return render_template('manager.html')
            con = db.connect('database.db')
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users where username=?",[username])
                users = cur.fetchall()
                for user in users:
                    dbUser = user[0]
                    dbPass = user[1]
                    if dbPass == password:
                        print("Securely Connected")
                        completion=(dbUser, username)
                        return render_template('book_user.html')
                    elif dbPass != password:
                        print("Incorrect Request Processed")
                        return render_template('loginfail.html')
        except:
            return render_template('loginfail.html')
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watchlist')
def watch():
    return render_template('fresh_tomatoes.html')

@app.route('/visual')
def visual():
    return render_template('visualization.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            con = db.connect('database.db')
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users where username=?",[username])
                users = cur.fetchall()
                for user in users:
                    dbUser = user[0]
                    dbPass = user[1]
                    if dbPass == password:
                        print("Securely Connected")
                        completion=(dbUser, username)
                        return render_template('index.html')
                    elif dbPass != password:
                        print("Incorrect Request Processed")
                        return render_template('loginfail.html')
        except:
            return render_template('loginfail.html')
    return render_template('login2.html')

@app.route('/getMoviesShowingOnDate', methods = ['POST'])
def moviesOnDate():
    date = request.form['date']
    res = runQuery("SELECT DISTINCT movie_id,movie_name,type FROM movies NATURAL JOIN shows WHERE Date = '"+date+"'")
    if res == []:
        return '<h4>No Movies Showing</h4>'
    else:
        return render_template('movies.html',movies = res)

@app.route('/getTimings', methods = ['POST'])
def timingsForMovie():
    date = request.form['date']
    movieID = request.form['movieID']
    movieType = request.form['type']
    res = runQuery("SELECT time FROM shows WHERE Date='"+date+"' and movie_id = "+movieID+" and type ='"+movieType+"'")
    list = []
    for i in res:
        list.append( (i[0], int(i[0]/100), i[0]%100 if i[0]%100 != 0 else '00' ) )
    return render_template('timings.html',timings = list) 

@app.route('/getShowID', methods = ['POST'])
def getShowID():
    date = request.form['date']
    movieID = request.form['movieID']
    movieType = request.form['type']
    time = request.form['time']
    res = runQuery("SELECT show_id FROM shows WHERE Date='"+date+"' and movie_id = "+movieID+" and type ='"+movieType+"' and time = "+time)
    return jsonify({"showID" : res[0][0]})

@app.route('/getAvailableSeats', methods = ['POST'])
def getSeating():
    showID = request.form['showID']
    res = runQuery("SELECT class,no_of_seats FROM shows NATURAL JOIN halls WHERE show_id = "+showID)
    totalGold = 0
    totalStandard = 0
    for i in res:
        if i[0] == 'gold':
            totalGold = i[1]
        if i[0] == 'standard':
            totalStandard = i[1]
    res = runQuery("SELECT seat_no FROM booked_tickets WHERE show_id = "+showID)
    goldSeats = []
    standardSeats = []
    for i in range(1, totalGold + 1):
        goldSeats.append([i,''])
    for i in range(1, totalStandard + 1):
        standardSeats.append([i,''])
    for i in res:
        if i[0] > 1000:
            goldSeats[ i[0] % 1000 - 1 ][1] = 'disabled'
        else:
            standardSeats[ i[0] - 1 ][1] = 'disabled'
    return render_template('seating.html', goldSeats = goldSeats, standardSeats = standardSeats)

@app.route('/getPrice', methods = ['POST'])
def getPriceForClass():
    showID = request.form['showID']
    seatClass = str('gold')
    priceID = randint(0,12)
    ticketNo = randint(0, 2147483646)
    res = runQuery("INSERT INTO halls VALUES(-1,'-1',-1)");
    res = runQuery("DELETE FROM halls WHERE hall_id = -1")
    res = runQuery("SELECT price FROM price_listing WHERE price_id = "+str(priceID))
    return '<h5>Ticket Price: ₹ '+'540'+'</h5>\
    <h5>Ticket Successfully Booked</h5>\
    <h6>Ticket Number: '+str(ticketNo)+'</h6>'

@app.route('/getShowsShowingOnDate', methods = ['POST'])
def getShowsOnDate():
    date = request.form['date']
    res = runQuery("SELECT show_id,movie_name,type,time FROM shows NATURAL JOIN movies WHERE Date = '"+date+"'")
    if res == []:
        return '<h4>No Shows Showing</h4>'
    else:
        shows = []
        for i in res:
            x = i[3] % 100
            if i[3] % 100 == 0:
                x = '00'
            shows.append([ i[0], i[1], i[2], int(i[3] / 100), x ])
        return render_template('shows.html', shows = shows)

@app.route('/getBookedWithShowID', methods = ['POST'])
def getBookedTickets():
    showID = request.form['showID']
    res = runQuery("SELECT ticket_no,seat_no FROM booked_tickets WHERE show_id = "+showID+" order by seat_no")
    if res == []:
        return '<h5>No Bookings</h5>'
    tickets = []
    for i in res:
        if i[1] > 1000:
            tickets.append([i[0], i[1] - 1000, 'Gold'])
        else:
            tickets.append([i[0], i[1], 'Standard'])
    return render_template('bookedtickets.html', tickets = tickets)

@app.route('/fetchMovieInsertForm', methods = ['GET'])
def getMovieForm():
    return render_template('movieform.html')

@app.route('/insertMovie', methods = ['POST'])
def insertMovie():
    movieName = request.form['movieName']
    movieLen = request.form['movieLen']
    movieLang = request.form['movieLang']
    types = request.form['types']
    startShowing = request.form['startShowing']
    endShowing = request.form['endShowing']
    res = runQuery('SELECT * FROM movies')
    for i in res:
        if i[1] == movieName and i[2] == int(movieLen) and i[3] == movieLang \
         and i[4].strftime('%Y/%m/%d') == startShowing and i[5].strftime('%Y/%m/%d') == endShowing:
            return '<h5>The Exact Same Movie Already Exists</h5>'
    movieID = 0
    res = None
    while res != []:
        movieID = randint(0, 2147483646)
        res = runQuery("SELECT movie_id FROM movies WHERE movie_id = "+str(movieID))
    res = runQuery("INSERT INTO movies VALUES("+str(movieID)+",'"+movieName+"',"+movieLen+\
        ",'"+movieLang+"','"+startShowing+"','"+endShowing+"')")
    if res == 'No result set to fetch from.':
        subTypes = types.split(' ')
        while len(subTypes) < 3:
            subTypes.append('NUL')
        res = runQuery("INSERT INTO types VALUES("+str(movieID)+",'"+subTypes[0]+"','"+subTypes[1]+"','"+subTypes[2]+"')")
        if res == 'No result set to fetch from.':
            return '<h5>Movie Successfully Added</h5>\
            <h6>Movie ID: '+str(movieID)+'</h6>'
    return '<h5>Something Went Wrong</h5>'

@app.route('/getValidMovies', methods = ['POST'])
def validMovies():
    showDate = request.form['showDate']
    res = runQuery("SELECT movie_id,movie_name,length,language FROM movies WHERE show_start <= '"+showDate+\
        "' and show_end >= '"+showDate+"'")
    if res == []:
        return '<h5>No Movies Available for Showing On Selected Date</h5>'
    movies = []
    for i in res:
        subTypes = runQuery("SELECT * FROM types WHERE movie_id = "+str(i[0]) )
        t = subTypes[0][1]
        if subTypes[0][2] != 'NUL':
            t = t + ' ' + subTypes[0][2]
        if subTypes[0][3] != 'NUL':
            t = t + ' ' + subTypes[0][3]
        movies.append( (i[0],i[1],t,i[2],i[3]) )
    return render_template('validmovies.html', movies = movies)

@app.route('/getHallsAvailable', methods = ['POST'])
def getHalls():
    movieID = request.form['movieID']
    showDate = request.form['showDate']
    showTime = request.form['showTime']
    res = runQuery("SELECT length FROM movies WHERE movie_id = "+movieID)
    movieLen = res[0][0]
    showTime = int(showTime)
    showTime = int(showTime / 100)*60 + (showTime % 100)
    endTime = showTime + movieLen 
    res = runQuery("SELECT hall_id, length, time FROM shows NATURAL JOIN movies WHERE Date = '"+showDate+"'")
    unavailableHalls = set()
    for i in res:
        x = int(i[2] / 100)*60 + (i[2] % 100)
        y = x + i[1]
        if x >= showTime and x <= endTime:
            unavailableHalls = unavailableHalls.union({i[0]})
        if y >= showTime and y <= endTime:
            unavailableHalls = unavailableHalls.union({i[0]})
    res = runQuery("SELECT DISTINCT hall_id FROM halls")
    availableHalls = set()
    for i in res:
        availableHalls = availableHalls.union({i[0]})
    availableHalls = availableHalls.difference(unavailableHalls)
    if availableHalls == set():
        return '<h5>No Halls Available On Given Date And Time</h5>'
    return render_template('availablehalls.html', halls = availableHalls)

@app.route('/insertShow', methods = ['POST'])
def insertShow():
    hallID = request.form['hallID']
    movieID = request.form['movieID']
    movieType = request.form['movieType']
    showDate = request.form['showDate']
    showTime = request.form['showTime']
    showID = 0
    res = None
    while res != []:
        showID = randint(0, 2147483646)
        day = randint(0,21)
        res = runQuery("SELECT show_id FROM shows WHERE show_id = "+str(showID))	
    res = runQuery("INSERT INTO shows VALUES("+str(showID)+","+movieID+","+hallID+\
        ",'"+movieType+"',"+showTime+",'"+showDate+"',"+str(day)+")")
    print(res)
    if res == 'No result set to fetch from.':
        return '<h5>Show Successfully Scheduled</h5>\
        <h6>Show ID: '+str(showID)+'</h6>'
    else:
        return '<h5>Something Went Wrong</h5>'

@app.route('/getPriceList', methods = ['GET'])
def priceList():
    res = runQuery("SELECT * FROM price_listing ORDER BY type")
    sortedDays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    res = sorted( res, key = lambda x : sortedDays.index(x[2]) )
    return render_template('currentprices.html', prices = res)

@app.route('/setNewPrice', methods = ['POST'])
def setPrice():
    priceID = request.form['priceID']
    newPrice = request.form['newPrice']
    res = runQuery("UPDATE price_listing SET price = "+newPrice+" WHERE price_id = "+priceID)
    if res == 'No result set to fetch from.':
        return '<h5>Price Successfully Changed</h5>\
            <h6>Standard: ₹ '+newPrice+'</h6>\
            <h6>Gold: ₹ '+str( int(int(newPrice) * 1.5) )+'</h6>'
    else:
        return '<h5>Something Went Wrong</h5>'

def runQuery(query):
    try:
        db = mysql.connector.connect(
            host='localhost',
            database='db_theatre',
            user='newuser',
            password='password')
        if db.is_connected():
            cursor = db.cursor(buffered = True)
            cursor.execute(query)
            db.commit()
            return cursor.fetchall()
    except Error as e:
        #Some error occured
        return e.args[1] 
    finally:
        db.close()
    #Couldn't connect to MySQL
    return None

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        dbHandler.insert(username,email,password)
        return render_template('register.html')
    else:
        return render_template('register.html')

if __name__ == '__main__':
        app.debug=True
        host=os.environ.get('IP','127.0.0.1')
        port=int(os.environ.get('PORT',8000))
        app.run(host=host,port=port)
