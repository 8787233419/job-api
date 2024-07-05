from django.shortcuts import render 
from django.http import JsonResponse
import json, random, string
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer, SessionSerializer ,JobSerializer , CandidateSerializer
from main.models import users,session,JobDetails
import random
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
            return Response(registered_data, status=201)
        else:
            return Response(session_serializer.errors, status=400)
    else:
        return Response(serializer.errors, status=400)

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
                if (timezone.now()- current_session.last_activity).total_seconds() > 3600:

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


@api_view(['POST'])
def newjob(request):
    data={
        'userid':request.data.get('userid'),
        'position':request.data.get('position'),
        'companyname':request.data.get('companyname'),
        'prerequisites':request.data.get('prerequisites'),
        'details':request.data.get('details'),
    }

    idlist = JobDetails.objects.values_list('jobid', flat=True)

    for i in range(100):
        if i not in idlist:
            data['jobid']=i
            break
        else:
            continue

    detailserializer=JobSerializer(data=data)

    if detailserializer.is_valid():
        detailserializer.save()

        return Response(json.dumps(data),status=200)

    return Response(json.dumps({'message':'some error occurred'}))     

@api_view(['POST'])
def applicant(request):
    data={
        'name':request.data.get('name'),
        'jobid':request.data.get('jobid'),
        'email':request.data.get('email'),
        'mobile':request.data.get('mobile'),
        'current_company':request.data.get('current_company'),
        'designation':request.data.get('designation'),
        'resume':request.data.get('resume')
    }
    # number=random.randint(10,99)
    # str_num=str(number)
    j_id=data['jobid']
    str_id=str(j_id)
    c_id=data['name']+str_id

    data['candidate_id']=c_id

    applicantserializer=CandidateSerializer(data=data)
    if applicantserializer.is_valid():
        applicantserializer.save()
        return Response(json.dumps({'message':'done'}),status=200)
    else:
        # Return a response if the data is not valid
        return Response(applicantserializer.errors, status=400)    
    # return Response(json.dumps({'message':'try again later'}))



    
