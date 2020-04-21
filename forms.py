
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('שם משתמש',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('דואר אלקטרוני',
                        validators=[DataRequired(), Email()])
    password = PasswordField('סיסמה', validators=[DataRequired()])
    confirm_password = PasswordField('וידוא סיסמה',
                                     validators=[DataRequired(), EqualTo('סיסמה')])
    submit = SubmitField('הרשם עכשיו')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('שם המשתמש כבר קיים. נסה שם אחר')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('כתובת דואר אלקטרוני זו כבר קיימת. נסה כתובת אחרת')


class LoginForm(FlaskForm):
    email = StringField('דואר אלקטרוני',
                        validators=[DataRequired(), Email()])
    password = PasswordField('סיסמה', validators=[DataRequired()])
    remember = BooleanField('זכור אותי')
    submit = SubmitField('התחבר')

class UpdateAccountForm(FlaskForm):
    username = StringField('שם משתמש',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('דואר אלקטרוני',
                        validators=[DataRequired(), Email()])
    picture = FileField('עדכן תמונת פרופיל', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('עדכן')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('שם המשתמש כבר קיים. נסה שם אחר')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('כתובת דואר אלקטרוני זו כבר קיימת. נסה כתובת אחר')


class PostForm(FlaskForm):
    title = StringField('כותרת', validators=[DataRequired()])
    content = TextAreaField('תוכן הפוסט', validators=[DataRequired()])
    submit = SubmitField('שלח')
