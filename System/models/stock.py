from .dbconnection import DbConnection
from datetime import datetime
from tinydb import Query

def get_timestamp(date = 0):

    if not date:
        date = str(datetime.today())

    date_obj = datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
    return date_obj.timestamp()



class Stock():
    pass

class StockArticles(DbConnection):
    """
    Use this class to create, edit, update or delete the articles
    of the DB
    """

    def __init__(self, db = 'System/databases/stock.json'):
        super().__init__(db)

        self.articles_names = self.get_all_articles()

    def get_all_articles(self) -> list:

        if 'articles' in self.db.tables():
            return self.db.table('articles').all()[0].get('articles', [])
        else:
            return []
    
    def check_if_articles_exist(self, article_name) -> bool:
        articles = self.get_all_articles()

        if articles:

            if article_name in articles:
                return True
            else:
                return False
        
    def insert_new_article(self, article_name) -> bool:

        """
        This function insert a new article in the database, if success
        return True

        article_name: str
        return: bool
        """
        
        if isinstance(article_name, list):
            print("You are passing a list, but this function just suport one 1 article each, calling insert_multiples_articles")
            self.insert_multiples_articles(article_name)
            return True
        
        if not isinstance(article_name, str):
            print("You are passing a invalid type, just str or list is accepted")
            return False
        
        old_data = self.get_all_articles()

        new_data = [article_name]
        

        if old_data:

            new_data = old_data
            

            if self.check_if_articles_exist(article_name):
                print('Articles already exist')
                return False
            else:
                new_data.append(article_name)
                self.update_articles(new_data)
                return True
        else:
            self.update_articles(new_data)
            return True
    
    def insert_multiples_articles(self, articles, duplicated = False) -> None:
        """
        This function insert multiples article in the database,
        if some articles is already on the database will be added into the variable

        articles : list
        return : None"""

        duplicated_articles = list()

        if isinstance(articles, list):
            for article in articles:
                self.insert_new_article(article)
    
    def update_articles(self, new_data) -> None:
        """
        This funcion update all the database, be carefull
        new_data : list
        """
        old_articles = self.get_all_articles()
        new_articles_data = []

        if old_articles:
            return self.db.table('articles').update({'articles' : new_data})
        else:
            return self.db.table('articles').insert({'articles' : new_data})

        
    
    def delete_article(self, article_name):
        """
        This function delete a article in the database,
        if the article not exist, the function return False, otherwise return True
        article_name: str
        return: bool
        """

        # Check if the user is passing multiples articles
        if isinstance(article_name, list):
            print("You are passing a list, but this function just suport one 1 article each")
            self.delete_multiples_articles(article_name)

        if self.check_if_articles_exist(article_name):
            old_articles_list = self.get_all_articles()
            try:
                old_articles_list.remove(article_name)
                new_articles = old_articles_list
                self.update_articles(new_articles)
                return True

            except ValueError:
                print(f'{article_name} Not Found')
        else:
            return False

    def delete_multiples_articles(self, articles):
        """
        This funcion delete multples articles of the database
        if some articles doesn't exist they will be added into a variable
        
        articles :  list
        return : None

        """
        not_founded_articles = list()

        for article in articles:
            if self.delete_article(article):
                pass
            else:
                not_founded_articles.append(article)

        print(f'These articles was not found {not_founded_articles}')

class StoreStock(StockArticles):
    """
    Use this class to create, edit, delete or update in the 
    Store Stock DB
    """
    def __init__(self, db='System/databases/stock.json'):
        super().__init__(db)

    def generated_data(self, store, date, data):
        return {'store' : store, 
                'date' : get_timestamp(date),
                'articles' : data}
    
    def check_if_store_exist(self, store):
        """
        This function check if the store exist in DB
        store: str
        return: bool
        """
        store_name = DbConnection.stores.get(int(store))

        if store_name in self.db.tables():
            return True
        else:
            return False

    def create_store_stock(self, store, date = 0):
        """
        This function create a new table with the store articles in DB
        store: str
        return: None
        """

        store_name = DbConnection.get_store_name(int(store))

        stock_count = {}
        articles = self.articles_names

        for article in articles:
            stock_count[article] = 0

        if self.check_if_store_exist(store):
            print('Store already exist')
        else:
            self.db.table(store_name).insert(self.generated_data(int(store), date, stock_count))
        
        return stock_count

    def reset_stock_count(self, store, date = 0):
        store_name = DbConnection.get_store_name(store)

        reseted_stock = {}
        articles = self.articles_names

        for article in articles:
            reseted_stock[article] = 0

        if self.check_if_store_exist(store):
            self.db.table(store_name).update(self.generated_data(store, date, reseted_stock))

        else:
            print("This store, doesn't exist")

    def get_stocks_dates(self, store):
        from datetime import datetime
        dates = {}
        

        def convert_timestamp(timestamp):
            # Suponhamos que seu timestamp seja 1643145028 (um exemplo qualquer)
            date = datetime.fromtimestamp(timestamp)

            # Formate a data conforme necessário
            date = date.strftime('%d/%m/%Y - %H:%M:%S')

            return date
        
        for stock in self.get_store_stock(store, all = True):
            dates[stock.get('date')] = (convert_timestamp(stock.get('date')))

        return dates
    
    # TO DO @staticmethod
    def get_store_stock(self, store, all = False, date = 0):
        """
        return the store stock count
        if you pass the parameter all as True, the function will return all the store stock count
        You also can use date filter
        store: str
        all = bool
        return: dict or list"""

        if isinstance(date, str) and '.' in date:
            date = float(date)

        store_name = DbConnection.get_store_name(int(store))

        stock_count = StoreStock().db.table(store_name).search(Query().store == int(store))

        if not stock_count:
            self.create_store_stock(int(store))
            stock_count = StoreStock().db.table(store_name).search(Query().store == int(store))

        if date:
            if date == 'last':
                return stock_count[-1].get('articles', {})
            
            elif date == 'reference':
                try:
                    return stock_count[-2].get('articles', {})
                except IndexError:
                    return stock_count[-1].get('articles', {})
        
            for stock in stock_count:
                if stock.get('date') == date:
                    return stock.get('articles')
            return {}
                
        if not all:
            return stock_count[-1].get('articles', {}) if stock_count else self.create_store_stock(int(store))
        else:
            return stock_count
        
    def update_store_count(self, store, date, data):
        store_name = DbConnection.get_store_name(int(store))

        return self.db.table(store_name).update(self.generated_data(store, date, data))

    def enter_stock(self, store, date, data):

        store_name = DbConnection.get_store_name(int(store))
        old_stock_count = StoreStock().get_store_stock(store)

        if data.get('reference'):
            pass

        

        if old_stock_count:
            if isinstance(data, dict):
                for article, amount in data.items():
                    
                    try:
                        # Convert amount o int type and verify if amount is not negative
                        amount = int(amount) if amount else 0
                        # Verify if amount is less than 0
                        if isinstance(amount, int):
                            if amount < 0:
                                amount = 0
                    except ValueError:
                        pass

                    old_stock_count[article] = amount

            new_stock_count = old_stock_count

            self.db.table(store_name).insert(self.generated_data(store, date, new_stock_count))
        else:
            return False


if __name__ == '__main__':
    data = StoreStock()
    a = data.get_stocks_dates(3)
    print(a)