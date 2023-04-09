from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import scipy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import os

import pandas as pd
from nltk.corpus import stopwords
from nltk import word_tokenize
import numpy as np
from tqdm import tqdm
import nltk
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')
db = SQLAlchemy()
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app = Flask(__name__)
bcrypt = Bcrypt(app)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SECRET_KEY'] = 'thisisasecretkey'




import pickle
filename = 'Word2Vec.sav'
model = pickle.load(open(filename, 'rb'))



###
## load login class
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



## user schema

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        ## query to get record in sqlachemly
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/index')
def hom():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
 
     rawtext = request.form['rawtext']
     

    #  import csv
    #  with open("train.csv", 'r') as csvfile:
    #   rows = csv.reader(csvfile)
     df= pd.read_csv(os.path.join(basedir, 'train.csv')) # importing the dataset

     df['question1'] = df['question1'].apply(lambda x: str(x))
     df['question2'] = df['question2'].apply(lambda x: str(x))
     def wmd(q1, q2):
      q1 = str(q1).lower().split()
      q2 = str(q2).lower().split()
      stop_words = stopwords.words('english')
      q1 = [w for w in q1 if w not in stop_words]
      q2 = [w for w in q2 if w not in stop_words]
      return model.wmdistance(q1, q2)

     ct=5
     list2=[]
     question = set(df['question2'])
     question1=list(question)
     for i in tqdm(question1):
      if ct == 0:
         break    
      sim= wmd(i,rawtext)
      if sim<2.2:
        ct=ct-1
        list2+=[i]
        print(i)
      

    #   adc = tfidf_vect.transform([i])
    #   x=scipy.sparse.hstack((abc,adc))
    #   if loaded_model.predict(x)==1:
    #    list2+=[i]
    #    ct=ct-1
    # # data1 = request.form['a']
    # data2 = request.form['b']
  
    # tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
    # tfidf_vect.fit(pd.concat((data1,data2)).unique())
    # trainq1_trans = tfidf_vect.transform(data1.values)
    # trainq2_trans = tfidf_vect.transform(data2.values)
    
    # X = scipy.sparse.hstack((trainq1_trans,trainq2_trans))
    # arr = np.array([[data1, data2]])
    # pred = model.predict(arr)
    
     return render_template('after.html',data=list2)
    


  


# @app.route('/predict',methods=['POST'])
# def predict():
#     '''
#     For rendering results on HTML GUI
#     '''
#     int_features = [int(x) for x in request.form.values()]
#     final_features = [np.array(int_features)]
#     prediction = model.predict(final_features)

#     output = round(prediction[0], 2)

#     return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))


















@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    #if True:
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



# #libariries for model
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle



import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import xgboost as xgb
import scipy



# model = pickle.load(open('finalized_model.pkl', 'rb'))





if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)
