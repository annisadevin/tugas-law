from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import *
from django.utils import timezone
import datetime
import random
import hashlib
import string

@api_view(['POST'])
def token(request):
    if request.content_type not in ["application/x-www-form-urlencoded"]:
        error_msg_body = {
            "error" : "invalid_request",
            "error_description" : "Request content-type must be application/x-www-form-urlencoded"
        }

        error_message = Response(
            error_msg_body, 
            status=status.HTTP_400_BAD_REQUEST
        )

        return error_message

    value = field_getter(request)
    username, password, grant_type, client_id, client_secret = value[0], value[1], value[2], value[3], value[4]

    try: 
        # validate user
        user_account = UserAccount.objects.get(username=username, password=password, grant_type=grant_type, client_id=client_id, client_secret=client_secret)
        # generate session id
        try:
            next_session_id = Session.objects.latest('id').id + 1
            
        except:
            next_session_id = 1

        # generate token contains session id
        token = generate_token(next_session_id)
        access_token, refresh_token = token[0], token[1]

        # create session
        id = next_session_id
        expires_in_seconds = 300
        login_time = timezone.now()

        try:
            session = Session.objects.create(id=id, akun=user_account, access_token=access_token, refresh_token=refresh_token, expires_in_seconds=expires_in_seconds, login_time=login_time)
            session.save()

        except Exception as e:
            # asumsi non multi session / 1 akun 1 session
            last_session = Session.objects.get(akun=user_account)
            last_session.delete()
            
            session = Session.objects.create(id=id, akun=user_account, access_token=access_token, refresh_token=refresh_token, expires_in_seconds=expires_in_seconds, login_time=login_time)
            session.save()

        response_body = {
            "access_token" : session.access_token,
            "expires_in" : session.expires_in_seconds,
            "token_type" : "Bearer",
            "scope" : None,
            "refresh_token" : session.refresh_token
        }

        response = Response(
            response_body, 
            status=status.HTTP_201_CREATED, 
            content_type="application/json"
        )

        return response

    except Exception as e:
        error_msg_body = {
            "error" : "invalid_request",
            "error_description" : "Data yang Anda masukan masih salah masbro!"
        }

        error_message = Response(
            error_msg_body, 
            status=status.HTTP_400_BAD_REQUEST
        )

        return error_message


def field_getter(request):
    username = request.data["username"]
    password = request.data["password"]
    grant_type = request.data["grant_type"]
    client_id = request.data["client_id"]
    client_secret = request.data["client_secret"]
    return [username, password, grant_type, client_id, client_secret]
    

def generate_token(session_id):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(39)).encode()
    random_string2 = ''.join(random.choice(letters) for i in range(39)).encode()
    
    gen_access_token = hashlib.sha1(random_string).hexdigest()
    gen_refresh_token = hashlib.sha1(random_string2).hexdigest()
    
    access_token = gen_access_token[:-1] + str(session_id)[-1]
    refresh_token = gen_refresh_token[:-1] + str(session_id)[-1]
    return [access_token, refresh_token]


@api_view(['POST'])
def resource(request):
    request_access_token = request.headers["Authorization"]
    request_access_token = request_access_token[7:] 
    
    try :
        session = Session.objects.get(access_token=request_access_token)
        session_is_not_expired = validate_session(session)

        if session_is_not_expired:
            user_account = session.akun
            profile = Profile.objects.get(akun=user_account)

            response_body = {
                "access_token" : session.access_token,
                "client_id" : user_account.client_id,
                "user_id" : user_account.username,
                "full_name" : profile.full_name,
                "npm" : profile.npm,
                "expires" : None,
                "refresh_token" : session.refresh_token
            }

            response = Response(
                response_body, 
                status=status.HTTP_201_CREATED, 
                content_type="application/json"
            )

            return response

        else :
            error_msg_body = {
                "error" : "invalid_token",
                "error_description" : "Token Salah masbro"
            }

            error_message = Response(
                error_msg_body, 
                status=status.HTTP_400_BAD_REQUEST
            )

            return error_message

    except : 
        error_msg_body = {
            "error" : "invalid_token",
            "error_description" : "Token Salah masbro"
        }

        error_message = Response(
            error_msg_body, 
            status=status.HTTP_400_BAD_REQUEST
        )

        return error_message


def validate_session(session):
    time_now = timezone.now()
    login_time = session.login_time
    expires_in_seconds = datetime.timedelta(0, session.expires_in_seconds)
    
    print(f"login_time: ",login_time)
    print(f"expired_time: ", login_time + expires_in_seconds)
    print(f"time_now: ", time_now)

    if login_time + expires_in_seconds >= time_now:
        return True

    else:
        session.delete()
        return False

