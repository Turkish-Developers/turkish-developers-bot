import dbm

class PdmManager:
    
    @staticmethod
    def add_sended_link(item):
        with dbm.open('article_links', 'c') as db:
            if 'link' in db:
                db['link'] = str(db['link']) + ',' + item + ','
            else:
                db['link'] = item + ','

    @staticmethod
    def is_link_in_db(item):
        with dbm.open('article_links', 'c') as db:
            if 'link' not in db:
                return False 

            items = str(db['link'])

        return item in items.split(',')
        

