import datetime

from flask import Flask, render_template

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template("main.html")


@app.route('/only_timetable')
def only_timetable():
    return render_template("only_timetable.html", change="static/images/announcement3.png")


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")
