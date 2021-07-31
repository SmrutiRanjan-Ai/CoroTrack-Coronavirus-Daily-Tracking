from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Book
import requests

def index(request):
    
    response=requests.get("https://localcoviddata.com/covid19/v1/cases/jhu?daysInPast=2&country=IND").json()
    final_data=response["historicData"]["historicData"]
    date=response["historicData"]["historicData"][0]["date"]
    li=[]
    for i in range(len(final_data)):
        if final_data[i]["date"]==date:
            li.append(final_data[i])
        else:
            
            for j in final_data:
                if final_data[i]["provinceStateName"]==j["provinceStateName"]:
                    old=int(final_data[i]["peoplePositiveCasesCt"])
                    new=int(j["peoplePositiveCasesCt"])
                    old_death=int(final_data[i]["deathCt"])
                    new_death=int(j["deathCt"])
                    diff_death=new_death-old_death
                    j["death"]=diff_death

                    diff=old-new
                    
                    if diff<0:
                        j["status"]='🔺'
                        j["diff"]=-diff
                    elif diff>0:
                        j["status"]='▽'
                        j["diff"]=diff
                    else:
                        j["status"]='<>'
                        j["diff"]=0
    li=sorted(li,key=lambda l:int(l["diff"]),reverse=True)
                
               


    
    return render(request,'index.html',{'response':li,'date':date})

def register(request):
    if request.method=='POST':
        
        username=request.POST['username']
        email=request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password=request.POST['password']
        if username!='':
            user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name,last_name=last_name)
            
            user.save()
            return redirect('login')
        
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        print(username)
        user = auth.authenticate(request,username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            return redirect('login')

    return render(request,'login.html')  

def logout(request):
    auth.logout(request)
    return redirect('/')   

def search(request):
    if request.method=='POST':
        country=request.POST['search']

        try:
            response=requests.get(f"https://localcoviddata.com/covid19/v1/cases/jhu?daysInPast=2&country={country}").json()
            final_data=response["historicData"]["historicData"]
            date=response["historicData"]["historicData"][0]["date"]
            return render(request,'search.html',{'response':final_data,'date':date})
        except:
            return render(request,'error.html')
    return redirect('/')
    
    
