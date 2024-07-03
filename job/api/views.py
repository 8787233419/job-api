from django.shortcuts import render 
from django.http import JsonResponse
import json, random, string
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer, SessionSerializer ,JobSerializer
from main.models import users,session

@api_view(['POST'])
def register(request):
    registered_data = {
        'userid': request.data.get('userid'),
        'name': request.data.get('name'),
        'pswd': request.data.get('pswd'),
        'mobile': request.data.get('mobile'),
    }    

    serializer = UserSerializer(data=registered_data)
    if serializer.is_valid():
        serializer.save()

        KEYLEN = 30
        key = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(KEYLEN))
        session_data = {
            'userid': registered_data['userid'],
            'session_key': key
        }
        session_serializer = SessionSerializer(data=session_data)
        if session_serializer.is_valid():
            session_serializer.save()
            registered_data['session_key'] = key
            return Response(registered_data, status=status.HTTP_201_CREATED)
        else:
            return Response(session_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    userlist=list(users.objects.all().values())

    data={
        'userid':request.data.get('userid'),
        'pswd':request.data.get('pswd')
    }

    for user in userlist:
        if data['userid']==user.get('userid') and data['pswd']==user.get('pswd'):
            dic={
                'userid':user.get('userid'),
                'name':user.get('name'),
                'mobile':user.get('mobile'),
                'pswd':user.get('pswd')
            }
            KEYLEN=30
            key = "".join(random.choice(string.ascii_letters+string.digits) for _ in range(KEYLEN)) 
            session_data={
                'userid':data['userid'],
                'session_key':key
            }
            current_session = session.objects.filter(userid_id=data['userid']).first()
            if current_session is None:
                sessionserializer=SessionSerializer(data=session_data)
                if sessionserializer.is_valid():
                    sessionserializer.save()
                    dic['session_key']=key
                    return Response(json.dumps(dic), status=200)
                                
            else:    
                if (timezone.now()-current_session.last_activity).total_seconds() > 3600:

                    current_session.last_activity=timezone.now() #to change the value of last_activty
                    sessionserializer=SessionSerializer(data=session_data)
                    if sessionserializer.is_valid():
                        sessionserializer.save()
                        dic['session_key']=key
                        return Response(json.dumps(dic), status=200)
                else:
                    dic['session_key']=current_session.session_key
                    return Response(json.dumps(dic),status=200)
                    
    return Response(json.dumps({'message':'Invalid credentials'}), status=400)


# @api_view(['POST'])
# def newjob(request):

    
