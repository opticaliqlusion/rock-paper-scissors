import os, random
from flask import Flask, render_template, url_for, session, request


application = Flask(__name__)

application.secret_key = os.urandom(32)


colors = ["#FDB45C", "#F7464A", "#46BFBD", ]


@application.route("/",  methods=['GET', 'POST'])
def home():

    session_results = session.get('session_results', None)

    if not session_results:
        session['session_results'] = {'wins':0, 'losses':0, 'ties':0}

    old_server_choice = session.get('server_choice', None)

    session['server_choice'] = random.choice(['rock', 'paper', 'scissors'])

    choice = request.form.get('choice', None)

    if choice and old_server_choice:
        result = (choice, old_server_choice)
        if (choice == 'rock' and old_server_choice == 'scissors') \
          or (choice == 'paper' and old_server_choice == 'rock')  \
          or (choice == 'scissors' and old_server_choice == 'paper'):
            result = 'WIN'
            session['session_results']['wins'] += 1
        elif choice == old_server_choice:
            result = 'TIE'
            session['session_results']['ties'] += 1
        else:
            result = 'LOSE'
            session['session_results']['losses'] += 1
    else:
        result = None

    
    return render_template('home.html', 
        result=result, 
        session_results=session['session_results'], 
        set=zip(session['session_results'].values(), session['session_results'].keys(), colors))


if __name__ == '__main__':
    application.run(debug=True)
