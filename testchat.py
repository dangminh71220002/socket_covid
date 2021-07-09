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
    combo = ("World","USA","India","Brazil","France","Russia",
        "Turkey","UK","Argentina","Colombia","Italy","Spain","Germany",
        "Iran","Poland","Mexico","Indonesia","Ukraine","South Africa",
        "Peru","Netherlands","Czechia","Chile","Philippines","Canada",
        "Iraq","Sweden","Belgium","Romania","Bangladesh","Pakistan",
        "Portugal","Israel","Japan","Hungary","Malaysia","Jordan",
        "Serbia","Switzerland","Austria","Nepal","UAE","Lebanon",
        "Morocco","Saudi Arabia","Ecuador","Tunisia","Bolivia","Kazakhstan",
        "Paraguay","Greece","Belarus","Bulgaria","Panama","Slovakia",
        "Costa Rica","Uruguay","Georgia","Kuwait","Croatia","Azerbaijan",
        "Dominican Republic","Palestine","Guatemala","Thailand","Denmark","Egypt",
        "Venezuela","Oman","Lithuania","Ethiopia","Ireland","Honduras",
        "Sri Lanka","Bahrain","Slovenia","Moldova","Armenia","Qatar",
        "Cuba","Bosnia and Herzegovina","Libya","Kenya","Myanmar","Zambia",
        "Nigeria","S. Korea","North Macedonia","Algeria","Latvia","Kyrgyzstan",
        "Norway","Albania","Mongolia","Estonia","Afghanistan","Uzbekistan",
        "Montenegro","Namibia","Finland","Ghana","Uganda","Mozambique",
        "Cameroon","Cyprus","El Salvador","Maldives","Botswana","Luxembourg",
        "Singapore","Zimbabwe","Cambodia","Jamaica","Ivory Coast","Rwanda",
        "Senegal","DRC","Madagascar","Angola","Malawi","Sudan",
        "Trinidad and Tobago","Cabo Verde","Réunion","Australia","Malta","French Guiana",
        "Syria","Gabon","Guinea","Vietnam","Suriname","Mauritania",
        "Guyana","Eswatini","Mayotte","Haiti","French Polynesia","Papua New Guinea",
        "Guadeloupe","Seychelles","Taiwan","Somalia","Mali","Togo",
        "Andorra","Tajikistan","Burkina Faso","Belize","Bahamas","Congo",
        "Martinique","Curaçao","Hong Kong","Lesotho","Djibouti","Aruba",
        "South Sudan","Timor-Leste","Equatorial Guinea","Nicaragua","Benin","Fiji",
        "CAR","Yemen","Iceland","Eritrea","Gambia","Sierra Leone",
        "Burundi","Niger","Saint Lucia","San Marino","Liberia","Chad",
        "Channel Islands","Gibraltar","Barbados","Comoros","Guinea-Bissau","Liechtenstein",
        "New Zealand","Sint Maarten","Monaco","Bermuda","Laos","Turks and Caicos",
        "Sao Tome and Principe","Saint Martin","Bhutan","St. Vincent Grenadines","Mauritius","Caribbean Netherlands",
        "Isle of Man","Antigua and Barbuda","St. Barth","Faeroe Islands","British Virgin Islands","Diamond Princess",
        "Cayman Islands","Saint Kitts and Nevis","Tanzania","Wallis and Futuna","Brunei","Dominica",
        "Grenada","New Caledonia","Anguilla","Falkland Islands","Macao","Greenland",
        "Vatican City","Saint Pierre Miquelon","Montserrat","Solomon Islands","Western Sahara","MS Zaandam",
        "Vanuatu","Marshall Islands","Samoa","Saint Helena","Micronesia","China")

    
    # url = f'https://coronavirus-19-api.herokuapp.com/countries/{region}'
    # response = ur.urlopen(url)
    # data = json.loads(response.read())
    # print(data)

    for region in combo:
        region = urllib.parse.quote(region)
        url = f"https://coronavirus-19-api.herokuapp.com/countries/{region}"
        try:
            response = ur.urlopen(url)
            data = json.loads(response.read())
            print("complete")
        except:
            print("error")
def process():
    f= open('data.json',)
    data = json.load(f)

    for i in data:
        print(i['country'],end=" , ")

commandCovid()
