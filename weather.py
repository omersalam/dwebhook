from flask import Flask,request,make_response
import os,json
import pyowm
import os
import requests

app = Flask(__name__)
owmapikey='6628ad3fd90a97fb39ff9793c7569874' #or provide your key here
owm = pyowm.OWM(owmapikey)


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

    if phoneNumber == '+923035588009':
        url = 'http://20.46.150.26/api/users/custom_login_iop/'
        parameterToPass = {'ph_no': phoneNumber , 'token' : '123456'}
##    parameterToPass = {'Authorization': 'token e89f01f5d23dd9c2172e788ade9f0e363190b843'}
##    request1 = requests.get(url, headers={'Authorization': 'Token e89f01f5d23dd9c2172e788ade9f0e363190b843'})
        request1 = requests.post(url,data = parameterToPass)
##    data = parameterToPass
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
        if requestStatus['status'] == 200:
            speech = "Welcome" + str(requestStatus['status'])
        else:
            speech = "Login Failed"
    elif phoneNumber == 'Show devices' or phoneNumber == 'Show Devices' or phoneNumber == 'show devices':
        url = 'http://20.46.150.26/iof/get_entities_list/?type_id=62&index_a=0&index_b=100'
        request1 = requests.get(url, headers={'Authorization': 'Token e89f01f5d23dd9c2172e788ade9f0e363190b843'})
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
        url = 'http://20.46.150.26/iop/get_schedules_list/?day=1&start_date=2020-03-10&appliance_id=134'
        request1 = requests.get(url, headers={'Authorization': 'Token e89f01f5d23dd9c2172e788ade9f0e363190b843'})
        print(type(request1))
        requestStatus = request1.json()
        print(requestStatus['status'])
        if requestStatus['status'] == 200:
            speech = "Scedule List"
            for res in requestStatus['response']:
                print(speech)
                speech = speech + str("\n Date: "+res['start_date'] + "\n Name: " + res['scheduled_by'] + "\n Temperature:" + res['temperature'] + "\n")
        else:
            speech = "Failed to fetech"
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
