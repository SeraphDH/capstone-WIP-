from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class EditProfileForm(FlaskForm):
    new_username = StringField('New Username', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update Username')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

    def validate_current_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Current password is incorrect.')

class MainQuestForm(FlaskForm):  # New form for Main Quests
    main_quests = TextAreaField('Main Quests')
    submit = SubmitField('Save Main Quests')

class SideQuestForm(FlaskForm):  # New form for Side Quests
    side_quests = TextAreaField('Side Quests')
    submit = SubmitField('Save Side Quests')

class PlotHooksForm(FlaskForm):  # New form for Plot Hooks
    plot_hooks = TextAreaField('Plot Hooks')
    submit = SubmitField('Save Plot Hooks')

class CharacterQuestsForm(FlaskForm):  # New form for Character Quests
    character_quests = TextAreaField('Character Quests')
    submit = SubmitField('Save Character Quests')

class FunTwistsForm(FlaskForm):  # New form for Fun Twists
    fun_twists = TextAreaField('Fun Twists')
    submit = SubmitField('Save Fun Twists')

class BigBadEvilGuyForm(FlaskForm):  # New form for Big Bad Evil Guy
    big_bad_evil_guy = TextAreaField('Big Bad Evil Guy')
    submit = SubmitField('Save Big Bad Evil Guy')