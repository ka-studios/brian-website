from tkinter import Tk, Canvas, Button
from flask import Flask, render_template, session, url_for, Response, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import hashlib

app = Flask(__name__, template_folder=".")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

root = Tk()
root.title("Tutor App")
root.wm_attributes("-topmost", 1)
window = Canvas(root, width=650, height=550)
window.pack()

class Main:
    def __init__(self):
        self.getTutorAppointment = Button(root, text="Schedule Appointment", command=self.getAppointment)
        self.getTutorAppointment.pack(anchor='nw')

    def getAppointment(self):
        pass

main = Main()

try:
    while True:
        main
        root.update()
        root.update_idletasks()
except KeyboardInterrupt:
    exit(0)
