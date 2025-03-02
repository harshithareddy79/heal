from flask import Flask,render_template, request
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute("create table if not exists user(full_name TEXT, email TEXT, password TEXT, mobile TEXT, dob TEXT, university TEXT, age TEXT, degree_level TEXT, cgpa TEXT, gender TEXT, terms TEXT)")

flask_app=Flask(__name__)

@flask_app.route('/')
def home():

    return render_template('home.html')



@flask_app.route('/support')
def support():
    return render_template('support.html')

@flask_app.route('/counsellers')
def counsellers():
    return render_template('counsellers.html')

@flask_app.route('/meditation')
def meditation():
    return render_template('meditation.html')

@flask_app.route('/games')
def games():
    return render_template('games.html')

@flask_app.route('/books')
def books():
    return render_template('books.html')

@flask_app.route('/music')
def music():
    return render_template('music.html')

@flask_app.route('/analytics', methods=['POST', 'GET'])
def analytics():
    if request.method == 'POST':
        col1 = request.form['col1']
        col2 = request.form['col2']
        print(col1, col2)

        df = pd.read_csv('MentalHealthSurvey.csv')

        # Convert the DataFrame to a long format for comparison
        long_df = df.melt(value_vars=[col1, col2], 
                        var_name='Category', 
                        value_name='Values')

        # Plot the count plot
        plt.figure(figsize=(8, 6))
        sns.countplot(data=long_df, x='Values', hue='Category')

        # Customize the plot
        plt.title('Comparison of Counts in Column1 and Column2')
        plt.xlabel('Values')
        plt.ylabel('Count')

        # Save the figure
        plt.savefig('static/comparison_count_plot.png')
        return render_template('analytics.html', img = 'http://127.0.0.1:8005/static/comparison_count_plot.png')
    return render_template('analytics.html')

@flask_app.route('/signup', methods=['POSt', 'GET'])
def signup():
    if request.method == 'POST':
        data = request.form
        values = []
        for key in data:
            values.append(data[key])
        print(values)

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute("insert into user values(?,?,?,?,?,?,?,?,?,?,?)", values)
        connection.commit()

        return render_template('login.html', msg="Successfully registered")
    return render_template('signup.html')

@flask_app.route('/login', methods=['POSt', 'GEt'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute("select * from user where email='"+email+"' or mobile = '"+email+"' and password = '"+password+"'")
        result = cursor.fetchone()

        if result:
            return render_template('logged.html', result=result)
        else:
            return render_template('login.html', msg="Entered wrong credentials")
    return render_template('login.html')

@flask_app.route('/Edit/<mob>')
def Edit(mob):
    print(mob)
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("select * from user where mobile = '"+mob+"'")
    result = cursor.fetchone()
    return render_template('Edit.html', result=result)

@flask_app.route('/Delete/<mob>')
def Delete(mob):
    print(mob)
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("delete from user where mobile = '"+mob+"'")
    connection.commit()

    return render_template('home.html', msg="Account deleted successfully")

@flask_app.route('/Update', methods=['POSt', 'GEt'])
def Update():
    if request.method == 'POST':
        data = request.form
        values = []
        for key in data:
            values.append(data[key])
        print(values)

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute("update user set full_name = ?, email = ?, password = ?, mobile = ?, dob = ?, university = ?, age = ?, degree_level = ?, cgpa = ?, gender = ?, terms = ? where mobile = '"+values[3]+"'", values)
        connection.commit()

        return render_template('login.html', msg="Successfully updated")
    return render_template('signup.html')

if __name__ =='__main__':
    flask_app.run(
        host='127.0.0.1',
        port=8005,
        debug=True
    )


