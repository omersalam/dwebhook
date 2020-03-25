from flask import Flask,request,make_response
import os,json
import pyowm
import os
import requests
from datetime import date, datetime, time, timedelta
app = Flask(__name__)
key = ''
count = 0
deviceID = 0
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
    global count
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    incomingChecker = parameters.get("incoming")
    phoneNumber = parameters.get("ph_no")
    token1 = parameters.get("token")
    primaryEntity = parameters.get("id1")
    date = parameters.get("date")
    dayCount1 = parameters.get("dayCount")
    temperature1 = parameters.get("temperature")
    endTime1 = parameters.get("endTime")
    startTime1 = parameters.get("startTime")


#################################Login##################################################################################
    if phoneNumber == '+923035588009':
        url = 'http://20.46.150.26/api/users/custom_login_iop/'
        parameterToPass = {'ph_no': phoneNumber , 'token' : '123456' }
        request1 = requests.post(url,data = parameterToPass)
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
        if requestStatus['status'] == 200:
            global key
            key = 'Token ' + str(requestStatus['response']['token'])
            speech = "Welcome " + str(requestStatus['response']['first_name'] + "  Let's Begin with Tornado assistant")
        else:
            speech = "Login Failed. Please, Retry..."
################################Login End###############################################################################

############################## show devices#############################################################################
    elif phoneNumber == 'Show devices' or phoneNumber == 'Show Devices' or phoneNumber == 'show devices':
        url = 'http://20.46.150.26/iof/get_entities_list/?type_id=62&index_a=0&index_b=100'
        request1 = requests.get(url, headers={'Authorization': key})
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
        if requestStatus['status'] == 200:
            speech = "Name of Devices" + str(int(primaryEntity)) + "up"
            global deviceID
            check = int(primaryEntity)
            for res in requestStatus['response']:
                speech = speech + str("\n "+ str(res['id'])) + str(check)
                if int(res['id']) == int(check):
                    deviceID = 127
                else:
                    deviceID = 34
        else:
            speech = "Failed to display devices"
###############################Show device End##########################################################################
    elif phoneNumber == 'Schedule of tomorrow' or phoneNumber == 'Schedule Of Tomorrow' or phoneNumber == 'schedule of tomorrow'  or phoneNumber == 'Schedule of Tomorrow':
        count = 0
        dateToday = datetime.date(datetime.now())
##        dateTime = datetime.time(datetime.now())
        presentday = datetime.now() 
        yesterday = presentday + timedelta(1)
        url = ('http://20.46.150.26/iop/get_schedules_list/?day=1&start_date=' + str(yesterday.strftime('%Y-%m-%d')) + '&appliance_id='+ str(deviceID))
        request1 = requests.get(url, headers={'Authorization': key})
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
##        print (datetime.now() - timedelta(hours=5))
##        updatedTime = (datetime.now() + timedelta(hours=5)) 
        if requestStatus['status'] == 200:
            speech = "Scedule List" + str(deviceID)
            for res in requestStatus['response']:
                print(speech)
                if res['start_date'] == str(yesterday.strftime('%Y-%m-%d')):
                    count += 1
                    speech = speech  +  str("\n Date: "+res['start_date'] + "\n Temperature:" + res['temperature'] + "\n")
            speech = "Total Schedules "+ str(count) +  "  " + speech          
        else:
            speech = "Failed to fetech"+ str(deviceID)
###########################################################select device###########################################

###############################################################################Get schedules#######################

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
