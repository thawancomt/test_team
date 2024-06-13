from flaskr.blueprints import *
from datetime import datetime



homepage = Blueprint('homepage', __name__,
                     url_prefix='/homepage',
                     template_folder='../templates',
                     static_folder= '../static')


from flaskr.blueprints.tasks.services.TaskService import TaskService
from flaskr.blueprints.stores_management.services.StoreService import StoreService
from flask_login import login_required, current_user

import os



@homepage.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    
    context = {
        'tasks' : {
            'all_tasks' : TaskService.get_tasks_of_day(),
            'active_tasks' : TaskService.get_active_tasks_of_day(),
            'done_tasks' : TaskService.get_done_tasks_of_day(),
        'date' : datetime.now().strftime('%d/%m/%Y'),
        'store_name' : StoreService().get_by_id(current_user.store_id).name
        }
    }
    
    
    return render_template('homepage.html', context=context, os=os)
