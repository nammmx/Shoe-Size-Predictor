import pandas as pd
from flask import Flask, request, render_template, url_for, redirect
import pickle
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

ENV = "prod"

if ENV =="dev":
  app.debug = True
  #development database
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:**********@localhost/shoe_size"
else:
  app.debug = False
  #production database
  app.config["SQLALCHEMY_DATABASE_URI"] = "********"

#warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#delete cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#database object
db = SQLAlchemy(app)

#create model
class Shoes(db.Model):
  __tablename__ = "shoes"
  id = db.Column(db.Integer, primary_key=True)
  height = db.Column(db.Integer)
  gender = db.Column(db.Integer)
  shoe_size = db.Column(db.Integer)

  #initializer/constructor
  def __init__(self, height, gender, shoe_size):
    self.height = height
    self.gender = gender
    self.shoe_size = shoe_size


#secret key for session
#app.secret_key = 'super secret key'
#load model
model = pickle.load(open('model.pkl', 'rb'))

#homepage
@app.route('/')
def home():
  return render_template('index.html')

#prediction & result
@app.route('/predict', methods=['POST'])
def predict():
  if request.method == 'POST':
    height = int(request.form['height'])
    gender = int(request.form['gender'])
    #data into dataframe
    data = pd.DataFrame([[gender, height]], columns=['gender', 'height'])
    #prediction
    prediction = model.predict(data)
    shoe_size = int(round(prediction[0], 0))
    #insert in database
    new_shoe = Shoes(height, gender, shoe_size)
    db.session.add(new_shoe)
    db.session.commit()
  return render_template('result.html', prediction_text='Prediction of your shoe size: {}'.format(shoe_size))

#if prediction correct
@app.route('/redirect_yes', methods=['POST'])
def redirect_yes():
  #if request.method == 'POST':
  return redirect(url_for('home'))

#if prediction wrong
@app.route('/redirect_no', methods=['POST'])
def redirect_no():
  #if request.method == 'POST':
  #delete from database
  db.session.delete(Shoes.query.order_by(Shoes.id.desc()).first())
  db.session.commit()
  return render_template('redirect_no.html')

#feedback if prediction wrong
@app.route('/feedback', methods=['POST'])
def feedback():
  if request.method == 'POST':
    #new data
    height = int(request.form['height'])
    gender = int(request.form['gender'])
    shoe_size = int(request.form['shoe_size'])
    #insert in database
    new_shoe = Shoes(height, gender, shoe_size)
    db.session.add(new_shoe)
    db.session.commit()    
  return redirect(url_for('home'))

#run app
if __name__ == "__main__":
  app.run()
