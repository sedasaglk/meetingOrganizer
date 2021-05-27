import sqlite3
from urllib import request
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/view')
def view():
    con = sqlite3.connect("MeetingOrganizer.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT MeetingId,toplantiKonusu,tarih,baslangicSaati,bitisSaati,katilimcilar FROM Meetings')
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


@app.route("/viewMeetingUpdate/<string:s>",methods=["POST", "GET"])
def meetingUpdate(s):
    if request.method == "GET":
        con = sqlite3.connect("MeetingOrganizer.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""SELECT toplantiKonusu,tarih,baslangicSaati,bitisSaati,katilimcilar FROM Meetings WHERE MeetingId=?""",[s])
        rows = cur.fetchall()
    return render_template("oneMeetingInfo.html", rows=rows,s=s)


@app.route("/updateMeetingInfo/<string:id>", methods=["POST", "GET"])
def meetingDetails(id):
    if request.method == "GET":
        con = sqlite3.connect("MeetingOrganizer.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT toplantiKonusu,tarih,baslangicSaati,bitisSaati,katilimcilar FROM Meetings")
        rows = cur.fetchall()
    return render_template("submitMeetingInfo.html", rows=rows, id=id)


@app.route("/updateDetails/string:id", methods=["POST", "GET"])
def updateDetails(id):
    if request.method == "POST":
        try:
            toplantiKonusu = request.form["title"]
            tarih = request.form["tarih"]
            baslangicSaati = request.form["stime"]
            bitisSaati = request.form["btime"]
            katilimcilar = request.form["katilimcilar"]
            with sqlite3.connect("MeetingOrganizer.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                sqlQuery = """UPDATE Meetings
                SET title="{}",
                tarih="{}",
                stime="{}",
                ftime="{}",
                katilimcilar="{}"
                """.format(toplantiKonusu, tarih, baslangicSaati, bitisSaati, katilimcilar, id)
                print("line-184")
                cur.execute(sqlQuery)
                con.commit()
        except Exception as e:
            con.rollback()
        finally:
            return render_template("/index.html")
            con.close()
@app.route("/addMeeting")
def addMeeting():
    return render_template("insertMeeting.html")

@app.route("/insertMeeting", methods=["POST", "GET"])
def insertMeeting():
    if request.method == "POST":
        try:
            toplantiKonusu = request.form["title"]
            tarih = request.form["tarih"]
            baslangicSaati = request.form["stime"]
            bitisSaati = request.form["btime"]
            katilimcilar = request.form["katilimcilar"]
            with sqlite3.connect("MeetingOrganizer.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                sqlQuery = """INSERT INTO Meetings(toplantiKonusu,tarih,baslangicSaati,bitisSaati,katilimcilar)
                VALUES ("{}","{}","{}","{}","{}")""".format(toplantiKonusu, tarih, baslangicSaati, bitisSaati, katilimcilar, id)
                cur.execute(sqlQuery)
                con.commit()
        except Exception as e:
            con.rollback()
        finally:
            return render_template("/index.html")
            con.close()


@app.route("/deleteMeeting", methods=["POST", "GET"])
def deleteMeeting():
    if request.method == "GET":
        con = sqlite3.connect("MeetingOrganizer.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("DELETE FROM Meetings")
        rows = cur.fetchall()
    return render_template("index.html ")


if __name__ == '__main__':
    app.run(debug=True)
