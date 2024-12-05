from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ConnectionDBHendler:
    def __init__(self):     
        self.engine = 'mysql+pymysql://root:@localhost:3306/cooksytem'
        self.__engine = create_engine(self.engine)
        self.session = None
        
    def create_engine(self, URL): 
        url = URL
        create_connection = create_engine(url)
        return create_connection
    
    def get_engine(self):
        return self.__engine
    
    def __enter__(self):
        Session = sessionmaker(bind=self.__engine)
        self.session = Session()
        return self
    
    def __exit__(self, exc_type, exc_tb, ext_val):
        self.session.close()
        
        