from tinydb import TinyDB, Query


class DbConnection():

    permissive_keys_for_create_users = [
        'username',
        'password',
        'level',
        'email',
        'store'
    ]

    stores = {
        0: None,
        3: 'Colombo',
        5: 'Odivelas',
        11: 'Campo de Ourique',
        25: 'Baixa Chiado'
    }

    def __init__(self, db):
        self.db = TinyDB(db, indent=4)

    def search_username(self, username):
        result = self.db.search(Query().username == username)
        return result

    def insert_user(self, data):

        def check_user_exist():
            username = data['username']

            result = self.search_username(username)

            if result is not None:
                return result

        if not check_user_exist():
            if not check_user_exist():
                final_data = {key: value for key,
                              value in data.items() if key in self.permissive_keys_for_create_users}

            self.db.insert(final_data)

    def update_user(self, who, new_info):
        # If user wants to edit just one info, Ex: update just the name
        try:
            old_info = self.search_username(who.username)[0]

        except IndexError:
            raise 'UserNotFound'

        for key, value in new_info.items():

            if key in self.permissive_keys_for_create_users:
                self.db.update({key: value}, Query().username == who.username)
            else:
                print('Is not allowed to update this key or its a invalid key')

    def get_user_data(self, who):

        guest = {
            'username': 'guest',
            'password': 'erro',
            'email': 'erro',
            'store': '0',
            'level': 'guest',
            'when_was_created': 'erro',
        }

        try:
            by_username = self.db.search(Query().username == who.username)
            by_email = self.db.search(Query().email == who.email)
            if not by_username:
                return by_email[0]
            else:
                return by_username[0]

        # Dont need error thrating
        except:
            return guest

    def insert_production(self, store, date, data):

        store_name = self.stores[store]

        default_day = {
            'big_ball': 0,
            'small_ball': 0,
            'garlic_bread': 0,
            'mozzarela': 0,
            'edamer': 0,


        }

        # tem que mudar o retorno da funcao de get_day_production
        if self.get_day_production(store, date) == default_day:
            self.db.table(store_name).insert({'date': str(date),
                                              'production': data})

        else:

            old_data = self.get_day_production(store, date)

            self.update_production(
                store=store, date=date, old_data=old_data, new_data=data)

    def update_production(self, store, date, old_data, new_data):

        print(f'esses dados: {new_data} \n Data velha: {old_data}')
        store_name = self.stores[store]

        generated_data = {}

        for article_id, article_name in old_data.items():

            if new_data[article_id] == 0:
                generated_data[article_id] = old_data[article_id]
            else:
                generated_data[article_id] = old_data[article_id] + \
                    new_data[article_id]

        self.db.table(store_name).update(
            {'production': generated_data}, Query().date == str(date))

    def get_day_production(self, store, date):
        store_name = self.stores[store]

        result = self.db.table(store_name).search(Query().date == str(date))

        try:
            return result[0]['production']

        except IndexError:
            return {
                'big_ball': 0,
                'small_ball': 0,
                'garlic_bread': 0,
                'mozzarela': 0,
                'edamer': 0,


            }
        except KeyError:
            return 0
