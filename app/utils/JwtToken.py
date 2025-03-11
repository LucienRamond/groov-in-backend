from flask import make_response, request, g
import jwt
from functools import wraps

from app.model.user import User

SECRET = "qwertyuioplkmjnha5526735gbsgsg"

def generate_token(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")

def validate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.cookies.get('token')
        except KeyError:
            return make_response({"message": "Token not provided"}, 403)
        
        try:
            decoded_token = jwt.decode(token, SECRET, algorithms=["HS256"])
            user_query = User.query.filter_by(id=decoded_token['_id']).first()
            
            user = {
                "name":user_query.name, 
                "email":user_query.email, 
                "id":user_query.id, 
                "bands":user_query.bands                    
                }
                   
            g.user = user
            
            return func(*args, **kwargs)
        except Exception as e:
            return make_response({"message": str(e)}, 403)   
    return wrapper