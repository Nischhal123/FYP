from flask import Flask


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

app = Flask(name)

@app.route('/hello')
def helloIndex():
    return 'Hello World from Python Flask!'

app.run(host='0.0.0.0', port=5000)

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