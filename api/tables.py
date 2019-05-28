from flask_table import Table, Col, LinkCol
 
class Results(Table):
    #id = Col('Id', show=False)
    client_name = Col('Name')
    client_age = Col('Age', show=False)
    client_username = Col('Username')
    client_option = Col('Option')
    client_street = Col('StreetAddress', show=True)
    client_city = Col('CityAddress', show=True)
    client_state = Col('StateAddress', show=True)
    client_zipcode = Col('ZipcodeAddress', show=True)
    coborrower_name = Col('CoborrowerName', show = True)
    coborrower_age = Col('CoborrowerAge', show = True)
