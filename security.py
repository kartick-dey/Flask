from werkzeug.security import safe_str_cmp
from user_details import UserDetails

users = [
    UserDetails(1, 'kd', 'kd@kd')
]

username_mapping = { user.username: user for user in users}
userid_mapping = { user.id: user for user in users}



def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def indentity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)