#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Menu, Song, Comment
from flask import session as login_session
from datetime import datetime
from datetime import date
import random
import string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
app = Flask(__name__)

"""File name: Project.py

It is web server for my the web applaction:
    1. read, update, create, delete from database
    2. using Oauth2 (google +)
    3. having login and logout button
    4. show lastadded Car posts
    
More details can be found in the README.md file,
which is included with this project.
"""



# Connect to Database and create database session
engine = create_engine('sqlite:///lyrics.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# JSON APIs to view Restaurant Information
@app.route('/menu/<int:menu_id>/menu/JSON')
def languages(menu_id):    
    items = session.query(Menu).filter_by(
        id=menu_id).all()
    return jsonify(language=[i.serialize for i in items])


@app.route('/menu/<int:menu_id>/song/<int:song_id>/JSON')
def menuItemJSON(menu_id, song_id):
    menu_item = session.query(Song).filter_by(id=song_id).one()
    return jsonify(song=menu_item.serialize)


@app.route('/languages/JSON')
def lyricsJSON():
    cars = session.query(Menu).all()
    return jsonify(cars=[r.serialize for r in cars])


@app.route('/')
@app.route('/lyrics/', methods=['GET', 'POST'])
def user_interface():
        return render_template('index.html')
        
    

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    def age(birthdate):
	today = date.today()
	return today.year - birthdate.year - ((today.month,
				       today.day) < (birthdate.month,
						     birthdate.day))
    def salatMaker():
        letters = string.ascii_lowercase    
        return ''.join(random.choice(letters) for i in range(10))

                                 
    if request.method == 'POST':
        birthdate = request.form['birth']
        umain = request.form['pass']
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        user_age = age(birthdate)
        user_salat = salatMaker()
        user_idea = str(hash(umain + user_salat))[::-1]
        newUser = User(name=request.form['name'], username=request.form['user'],
                       password=user_idea, gender=request.form.get('gender'),
                       age = user_age, birthd = request.form['birth'],
                       salaty = user_salat, email=request.form['mail'],
                       picture=request.form['pic'])
        session.add(newUser)
        flash('Thanks For Subcribing MR/Mss %s' % newUser.name)
        session.commit()        
        return redirect(url_for('user_interface'))
    else:
        return render_template('index.html')
    print(new_user.mail)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user']
        idea_user = request.form['pass']        
        user = session.query(User).filter_by(username=user_name).one()  
        if user:
            user_idea = str(hash(idea_user + user.salaty))[::-1]
            if user_idea == user.password:
                link = '/profile/' + str(user.id) + '/'
                flash('Nice to see you again Mr %s' % user.name)
                login_session['username'] = user.username
                login_session['id'] = user.id
                login_session['name'] = user.name
                login_session['gender'] = user.gender
                login_session['age'] = user.age
                login_session['birthdate'] = user.birthd
                login_session['email'] = user.email
                return redirect(url_for('user_interface'))
            else:
                flash('Sorry You have enter wrong pass or user Try Again')
                return render_template('index.html')
        else:
            flash('Sorry You have enter wrong pass or user click forget password!')
            return render_template('index.html')
                
                
@app.route('/disconnect')       
def gdisconnect():
    check_user = login_session.get('username')
    if check_user == None:
        print('UserName is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    else:
        
        print('In gdisconnect username is %s', check_user)
        print(login_session['username'])
        del login_session['username']
        del login_session['id']
        del login_session['name']
        del login_session['gender']
        del login_session['age']
        del login_session['birthdate']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('Successfully disconnected Bye Bye.')
        return redirect(url_for('user_interface'))
    

    
    



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
