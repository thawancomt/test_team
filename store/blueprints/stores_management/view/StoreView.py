from store.extensions import *
from store.utils import *

from ..services.StoreService import StoreService

# Our goal is make this code OOP, so we will create a class StoreView

class StoreView(BlueprintBase):
    def __init__(self, name = None, static_folder = None, url_prefix = None, template_folder = None, import_name = None) -> None:
        super().__init__(name, static_folder, url_prefix, template_folder, import_name)


    def register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.index, methods=['GET'])
        self.blueprint.add_url_rule('/create', view_func=self.create, methods=['POST'])
        self.blueprint.add_url_rule('/update', view_func=self.update, methods=['POST'])
        self.blueprint.add_url_rule('/delete', view_func=self.delete, methods=['POST'])
        return self.blueprint
    
    @login_required
    def index(self):
        context = {
            'stores' : StoreService().get_all_stores()
        }
        return render_template('create_store.html', **context)
    
    @login_required
    def create(self):
        name = request.form.get('name')
        store_id = request.form.get('id')
        place = request.form.get('place')
        
        try:
            StoreService(store_id=store_id, store_name=name, store_place=place).create()

        except ValueError as e:
            flash(f'{e}')
        
        return redirect(url_for('store.home'))



StoreView = StoreView(name='store', import_name=__name__, template_folder='../templates', url_prefix='/store').blueprint