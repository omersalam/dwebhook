from flask import Flask,request,make_response
import os,json
import pyowm
import os
import requests
from datetime import date, datetime, time, timedelta
app = Flask(__name__)
owmapikey='6628ad3fd90a97fb39ff9793c7569874' #or provide your key here
owm = pyowm.OWM(owmapikey)
key = ''
#geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    phoneNumber = parameters.get("ph_no")
    token1 = parameters.get("token")
    primaryEntity = parameters.get("id")
    date = parameters.get("date")
    dayCount1 = parameters.get("dayCount")
    temperature1 = parameters.get("temperature")
    endTime1 = parameters.get("endTime")
    startTime1 = parameters.get("startTime")

    if phoneNumber == '+923035588009':
        url = 'http://20.46.150.26/api/users/custom_login_iop/'
        parameterToPass = {'ph_no': phoneNumber , 'token' : '123456' }
##    parameterToPass = {'Authorization': 'token e89f01f5d23dd9c2172e788ade9f0e363190b843'}
##    request1 = requests.get(url, headers={'Authorization': 'Token e89f01f5d23dd9c2172e788ade9f0e363190b843'})
        request1 = requests.post(url,data = parameterToPass)
##    data = parameterToPass
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
        if requestStatus['status'] == 200:
            global key
            key = 'Token e89f01f5d23dd9c2172e788ade9f0e363190b843'
            speech = "Welcome " + str(requestStatus['response']['first_name'] + "  Let's Begin") + "Token  " + str(requestStatus['response']['token'])

        else:
            speech = "Login Failed"
            
    elif  phoneNumber == 'make' or phoneNumber == 'Make':
        if(temperature1 == 'hot'):
            temperature2 = 60
        elif(temperature1 == 'very hot'):
            temperature2 = 70
        else:
            temperature2 = 50
        if(dayCount1 == 'today'):
            dayCount2 = 0
        elif(dayCount1 == 'tomorrow'):
            dayCount2 = 1
        else:
            dayCount2 = 1
        dateToday = datetime.date(datetime.now())
        url = 'http://20.46.150.26/hypernet/entity/V2/add_activity_scehdule_appliance/'
        parameterToPass = {"end_date": str(dateToday),"end_times":[str(endTime1)],"start_times":[ str(startTime1)],
                            "action_items": str(temperature2),"primary_entity": primaryEntity ,
                           "activity_route":"Dishes","activity_type":2010,"t2": 75.0 ,"start_date": str(dateToday),"day_count": dayCount2}
        request1 = requests.post(url, json = parameterToPass, headers={'Authorization': 'Token e89f01f5d23dd9c2172e788ade9f0e363190b843'})
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
        if requestStatus['status'] == 200:
            speech = "Welcome added " + requestStatus['message']['message']
        else:
            speech = "Can not add"
    elif phoneNumber == 'Show devices' or phoneNumber == 'Show Devices' or phoneNumber == 'show devices':
        url = 'http://20.46.150.26/iof/get_entities_list/?type_id=62&index_a=0&index_b=100'
        request1 = requests.get(url, headers={'Authorization': key})
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
        if requestStatus['status'] == 200:
            speech = "Name of Devices"
            for res in requestStatus['response']:
                print(speech)
                speech = speech + str("\n "+res['name'])
        else:
            speech = "Failed to fetech"
    elif phoneNumber == 'Get Schedules' or phoneNumber == 'get schedules' or phoneNumber == 'Get schedules':
        dateToday = datetime.date(datetime.now())
##        dateTime = datetime.time(datetime.now())
        url = ('http://20.46.150.26/iop/get_schedules_list/?day=1&start_date=' + str(dateToday) + '&appliance_id=127')
        request1 = requests.get(url, headers={'Authorization': key})
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
##        print (datetime.now() - timedelta(hours=5))
##        updatedTime = (datetime.now() + timedelta(hours=5)) 
        if requestStatus['status'] == 200:
            speech = "Scedule List"
            for res in requestStatus['response']:
                print(speech)
                count = 0
                if res['start_date'] == str(dateToday):
                    count += 1
                    speech = speech + str(count) + "Schedules" + str("\n Date: "+res['start_date'] + "\n Temperature:" + res['temperature'] + "\n")
        else:
            speech = "Failed to fetech"

    elif phoneNumber == 'log out' or phoneNumber == 'Log Out' or phoneNumber == 'Log out':
        key = '0'
        speech = "Log Out"
    else:
        speech = "Failed to execute"
    return {
                "fulfillmentText": speech,
        "source": "dialogflow-weather-by-satheshrgs"
    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
