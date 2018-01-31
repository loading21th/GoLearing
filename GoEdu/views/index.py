
# coding:utf-8

from django.shortcuts import render 
from django.http import HttpResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import threading
from dwebsocket.decorators import accept_websocket,require_websocket
# Create your views here.

import os 
import json

clients = {} 

@csrf_exempt
def hlsroompage(request,schoolname,classname):
    print('**************************')
    if request.method == 'POST':
        upload_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'uploadfile',schoolname,classname)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        if request.FILES:
            file_obj = request.FILES.getlist('filename')[0]
            with open(os.path.join(upload_path,file_obj.name), 'wb') as newfile:
                for chunk in file_obj.chunks():
                    newfile.write(chunk)
        hlsdic = {'Courseware_name':os.listdir(upload_path)}
        response = JsonResponse(hlsdic, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        hlsdic = {'schoolname':schoolname,'classname':classname}
        return render(request,'index.html',hlsdic);


def download(request,schoolname,classname,filename):
    fullpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'uploadfile',schoolname,classname,filename)
    ffile = open(fullpath,'rb')
    response = FileResponse(ffile)
    response['Content-Type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response 


@accept_websocket
def echo(request,schoolname,classname):
    print('**************************')
    if request.is_websocket:
        lock = threading.RLock()
        try:
            lock.acquire()
            if not (schoolname+classname) in clients:
                clients[schoolname+classname] = []
            clients[schoolname+classname].append(request.websocket)
            for message in request.websocket:
                if not message:
                    break
                for client in clients[schoolname+classname]:
                    client.send(message)
        finally:
            lock.release()
