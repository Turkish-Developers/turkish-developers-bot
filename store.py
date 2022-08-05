import dbm

class PdmManager:
    
    @staticmethod
    def add_sended_key(item, key):
        with dbm.open('general', 'c') as db:
            if key in db:
                db[key] = str(db[key].decode("utf-8")) + ',' + item + ','
            else:
                db[key] = item + ','

    @staticmethod
    def is_key_in_db(item, key):
        with dbm.open('general', 'c') as db:
            if key not in db:
                return False 

            items = str(db[key].decode("utf-8"))

        return item in items.split(',')

    @staticmethod
    def get_key_value(item, key):
        with dbm.open('general', 'c') as db:
            if key not in db:
                return item
            item = str(db[key].decode("utf-8"))

        return item

    @staticmethod
    def set_key_value(item, key):
        with dbm.open('general', 'c') as db:
            db[key] = item

        return item

    @staticmethod
    def show_detail(key):
        with dbm.open('general', 'c') as db:
            return str(db[key].decode("utf-8"))

    def clear_key_in_db(key):
        with dbm.open('general', 'c') as db:
            db[key] = ''

        
        

