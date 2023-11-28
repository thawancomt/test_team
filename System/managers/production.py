from managers.dbconnection import DbConnection


class Production():
    articles = {
        'big_ball': 'Big Ball',
        'small_ball': 'Small Ball',
        'garlic_bread': 'Garlic bread',
        'mozzarela': 'Mozzarela',
        'edamer': 'Edamer',


    }

    def __init__(self, date, data={}):
        self.store = 0
        self.data = data  # Data
        self.date = date  # Date

    def send_production(self):
        DbConnection('databases/production.json').insert_production(
            self.store, self.date, self.data)

    def get_already_produced(self, store):
        return DbConnection('databases/production.json').get_day_production(store, self.date)


class Stores(Production):

    def __init__(self):
        super().__init__(self.get_already_produced)
        self.store = 0
