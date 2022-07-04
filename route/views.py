from django.shortcuts import render,redirect
from  django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .mixins import tabuSearch
import json
import math
import os
from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
distance_matrix =[[(0, 0), (8473, 637), (15056, 1307), (27365, 1823), (29239, 1976), (27544, 1867), (32189, 2301), (19155, 1284), (20490, 2086), (44299, 3842), (43844, 2420), (3218, 
425), (7507, 550)], [(8698, 622), (0, 0), (22823, 1734), (35132, 2250), (37006, 2403), (35311, 2294), (39956, 2728), (11192, 800), (21597, 1811), (45406, 3568), (35881, 1936), (10724, 876), (2842, 312)], [(15430, 1486), (22467, 1855), (0, 0), (13289, 1098), (14440, 1198), (22200, 1587), (26845, 2021), (29723, 1883), (35652, 3517), (59461, 5273), (56340, 3277), (14376, 1563), (21501, 1768)], [(27880, 1889), (34917, 2258), (13329, 1057), (0, 0), (3241, 388), (10456, 920), (18191, 1461), (40103, 2264), (48102, 3920), (71911, 5676), (66720, 3658), (26826, 1966), (33951, 2171)], [(29753, 2055), (36790, 2424), (14395, 1182), (3241, 388), (0, 0), (14851, 1126), (21228, 1640), (41976, 2430), (49975, 4086), (73784, 5842), (68593, 3824), (28699, 2132), (35824, 2337)], [(27968, 1952), (35005, 2321), (22157, 1581), (10374, 912), (14942, 1153), (0, 0), (12808, 948), (40191, 2327), (48190, 3983), (71999, 5739), (66808, 3721), (26914, 2029), (34039, 2234)], [(32515, 2327), (39552, 2696), (26704, 1956), (18118, 1443), (21191, 1630), (12817, 944), (0, 0), (44738, 2702), (52737, 4358), (76546, 6114), (63981, 4242), (31461, 2404), (38586, 2609)], [(22261, 
1341), (14940, 945), (31034, 2099), (40900, 2389), (42774, 2542), (41079, 2433), (38484, 2897), (0, 0), (22930, 1912), (46739, 3669), (26746, 1433), (24287, 1595), (12605, 1110)], [(20416, 2051), (21971, 1813), (35471, 3358), (47780, 3874), (49654, 4027), (47959, 3918), (52604, 4352), (22621, 1865), (0, 0), (31360, 2494), (44394, 2938), (23367, 2434), (23266, 2011)], [(44198, 3794), (45753, 3555), (59253, 5101), (71562, 5617), (73436, 5770), (71741, 5661), (76386, 6095), (46403, 3607), (31240, 2444), (0, 0), (57891, 4214), (47149, 4177), (47048, 3753)], [(43899, 2453), (36578, 2057), (58024, 3565), (67486, 3832), (69360, 3985), (67665, 3876), (65070, 4339), (26830, 1497), (44568, 3024), (53435, 4191), (0, 0), (45925, 2707), (37873, 2254)], [(2822, 440), (10839, 879), (15795, 1518), (28104, 2034), (29978, 2187), (28283, 2078), (32928, 2512), (21149, 1525), (23043, 2471), (46852, 4227), (46113, 2677), (0, 0), (9873, 793)], [(10190, 711), (2397, 226), (24315, 1823), (36624, 2339), (38498, 2492), (36803, 2383), (41448, 2817), (13079, 874), (23483, 1885), (47292, 3642), (37767, 2010), (12216, 965), (0, 0)]]

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)





@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        vehicleNumber = request.POST.get('vehicleNumber')
        ans = tabuSearch(distance_matrix, 10000, 100, 2, int(vehicleNumber))



        locs = None
        json_data = open(os.path.join(BASE_DIR, 'data.json'))   
        locs = json.load(json_data)


        # with open(os.path.join(BASE_DIR, '/static/data.json')) as json_file:
        #     locs = json.load(json_file)

        for v in range(int(vehicleNumber)):
            print("\nVEHICLE %d :" % (v + 1))
            print(" |>Optimal route = ", end="")
            for i in range(len(ans[0][v]) - 1):
                print(locs['locations'][ans[0][v][i]]['name'], end="")
                print(' ---> ', end="")
            print(locs['locations'][ans[0][v][0]]['name'])
            km = float(ans[1][v] / 1000)
            print(" |>Total route distance = ", km, "kilometers")
            print(" |>Total route duration = ", convert(ans[2][v]), "\n")

         
        
        return redirect('tabuResult')
    context = {}

    return render(request , 'index.html' , context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username=username, password=password)

        if user is not None:
            login(request,user)
            return  redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect.')

    context = {}

    return render(request , 'route/loginPage.html' , context)


def logoutPage(request):
    logout(request)
    return redirect('login')

def profilePage(request):
    context = {}
    return render(request , 'route/profile.html' , context)



def addUser(request):
    context = {}
    return render(request , 'route/addUser.html' , context)


def tabuResult(request):
    locs = None
    jsonData = open(os.path.join(BASE_DIR, 'data.json'))   
    locs = json.load(jsonData)

    # lat_a =  -20.16782
	# long_a = request.GET.get("long_a", None)
	# lat_b = request.GET.get("lat_b", None)
	# long_b = request.GET.get("long_b", None)
	# lat_c = request.GET.get("lat_c", None)
	# long_c = request.GET.get("long_c", None)
	# lat_d = request.GET.get("lat_d", None)
	# long_d = request.GET.get("long_d", None)

    return HttpResponse("nda printer you can view the map")