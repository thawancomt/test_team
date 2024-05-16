from flaskr.blueprints import *


from .services.login_service import LoginService

from datetime import datetime

login_bp = Blueprint('login_bp', __name__,
                     url_prefix='/login')

def external_ip():
    return request.remote_addr


@login_bp.route('/', methods=['GET'])
def login_page():

    
    return render_template('auth/login.html')

@login_bp.route('/', methods=['POST'])
def log_in():
    username = request.form.get('email')
    password = request.form.get('password')

    if LoginService().login(username, password):
        return redirect(url_for('home_bp.home'))
    return redirect(url_for('login_bp.login_page'))
    