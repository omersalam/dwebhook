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
    r.headers['Authorization'] = 'Token e89f01f5d23dd9c2172e788ade9f0e363190b843'
    return r

#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    phoneNumber = parameters.get("ph_no")

    url = 'http://20.46.150.26/iof/get_entities_list/?type_id=62&index_a=0&index_b=100'
##    parameterToPass = {'ph_no': phoneNumber , 'token' : '123456'}

    request1 = requests.get(url)
##    data = parameterToPass
    print(type(request1))
    requestStatus = request1.json()
    print(requestStatus['status'])

    if requestStatus['status'] == 200:
        speech = "Welcome" + "  " +  str(requestStatus['response']['name'])
    else:
        speech = "Login Failed" 

    return {
                "fulfillmentText": speech,
        "source": "dialogflow-weather-by-satheshrgs"
    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
