
from flaskr.blueprints.users.services.UserService import UserService, check_password_hash, generate_password_hash
from flaskr.blueprints.users.models.UserModel import User, db

from flask_login import login_user, logout_user, current_user
from flaskr.extensions import login_manager

from flask import  redirect, flash, url_for

from datetime import datetime

class LoginService:
    def __init__(self, email = None, password = None) -> None:
        
        if email is None or password is None:
            return self.logout()
        
        self.email = email
        self.password = password
        self.user = UserService().get_user_by(email = self.email)
        
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()
        
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash('You must be logged to see that page')
        return redirect(url_for('auth.login'))
    
    def login(self):
        if self.user and self.verify_password(self.user.password):
            self.user.last_login = datetime.now()
            db.session.commit()            
            login_user(self.user)
            return True
        
        return False
    
    def verify_password(self, hashed_password):
        return check_password_hash(hashed_password, self.password)

    def logout(self):
        logout_user()

        