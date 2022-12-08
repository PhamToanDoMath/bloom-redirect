import pybloom
from pybloom import ScalableBloomFilter
from redis import Redis
import os
import bcrypt

table_folder = './bloom-tables'

company_names = [
    'localhost:9999',
    'apple',
    'ibm',
    'android',
    'huawei'
]

def authentication_string(username, password):
    salt = b'$2b$12$mT68qRGAX.5j5c1C9NkQju'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt).decode()
    return f'{username}{hashed_password}'



class BloomTable:
    def __init__(self):
        if not os.listdir(table_folder):
            for name in company_names:
                ScalableBloomFilter(initial_capacity=1000, error_rate=0.001).tofile(open(os.path.join(table_folder,name),'wb'))
        self.tables = {file:ScalableBloomFilter.fromfile(open(os.path.join(table_folder,file), 'rb')) for file in os.listdir(table_folder)}

    def checkUserExist(self, username, password) -> bool:
        return any([authentication_string(username, password) in bloomTable for bloomTable in self.tables])
    
    def addUser(self, username, password, company) -> bool:
        return self.tables[company].add(authentication_string(username, password))
        
    def findUserSuperset(self, username: str, password: str) -> list[int]:
        result = []
        for company, bloomTable in self.tables.items():
            if authentication_string(username=username, password=password) in bloomTable:
                result.append(company)
        return result


class AuthorizationHelper:
    def __init__(self):
        self.bloomTable = BloomTable() 
        self.redis = Redis(host='localhost', port=6379, db=0)
        
    def checkUser(self, request):
        username = request.json.get('username')
        password = request.json.get('password')
        
        if self.redis.get(authentication_string(username, password)):
            return True
        return self.bloomTable.checkUserExist(username, password)
    
    def getRedirectURL(self, request):
        username = request.json.get('username')
        password = request.json.get('password')
        company_names = self.bloomTable.findUserSuperset(username, password)
        if len(company_names) == 0:
            raise Exception('Could not find user')
        if len(company_names) == 1:
            return company_names[0]
        else:
            raise Exception('Find mutliple company names')
        
    def addUser(self, request):
        username = request.json.get('username')
        password = request.json.get('password')
        company = request.json.get('company')
        return self.bloomTable.addUser(username, password, company)