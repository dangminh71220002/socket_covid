import threading
import urllib, json
import urllib.request as ur
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def foo():
    print("hello")

def commandCovid():
    url = 'https://coronavirus-19-api.herokuapp.com/countries'
    response = ur.urlopen(url)
    data = json.loads(response.read())
    with open('data.json', 'w') as f:
        json.dump(data, f)

def process():
    f= open('data.json',)
    data = json.load(f)

    for i in data:
        print(i['country'],end=" , ")

commandCovid()
process()