from flask import Flask, render_template, request,url_for
import sqlite3

def create_database():
    connection = sqlite3.connect("names.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY, name TEXT,email TEXT)")
    connection.commit()
    connection.close()

def insert_name_and_email(email, name):
    connection = sqlite3.connect("names.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO names (email, name) VALUES (?, ?)", (email, name))
    connection.commit()
    connection.close()

def read_data_from_database():
    connection = sqlite3.connect("names.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM names")
    data = cursor.fetchall()

def check_email_uniqueness(email):
    connection = sqlite3.connect("names.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM names WHERE email=?", (email,))
    count = cursor.fetchone()[0]

    connection.close()

    if count > 0:
        return False
    else:
        return True


app = Flask(__name__)
app.static_folder = 'static'
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    else:
        kisi_Mail = request.form.get('MailAdress')
        kisi_Name = request.form.get('Name')
        if kisi_Mail == '' and kisi_Name == '':
            return render_template('index.html', message = 'Please Fill Form',CheckForAprrove = False)
        elif kisi_Name == ' ' or kisi_Name == '':
            return render_template('index.html', message = 'Please Try a Valid Name',CheckForAprrove = False)
        elif kisi_Mail == ' ' or kisi_Mail == '':
            return render_template('index.html', message = 'Please Try a Valid E-Mail',CheckForAprrove = False)
        else:
            if check_email_uniqueness(kisi_Mail) == True:   
                insert_name_and_email(kisi_Mail,kisi_Name)
                return render_template('index.html', message = 'You Registered Succsesfully', CheckForAprrove = True)
            else:
                return render_template('index.html', message = 'This E-Mail Adress Already In Use',CheckForAprrove = False)

@app.route('/tumkullanicilar', methods=['GET'])
def listAll():
    connection = sqlite3.connect("names.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM names")
    data = cursor.fetchall()
    listem = []
    for row in data:
        eklenecek= f"ID: {row[0]}, Isim: {row[1]}, E-Mail: {row[2]}"
        listem.append(str(eklenecek))
    return render_template('users.html', listem = listem)

if __name__ == "__main__":
    create_database()
    app.run(debug= True)