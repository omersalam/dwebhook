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
    city = parameters.get("ph_no")

    url = 'http://20.46.150.26/api/users/resend_verification_code/'
    myobj = {'ph_no': city}

    x = requests.post(url, data=myobj)
    print(type(x))
    res = x.json()
    print(res['status'])

    if res['status'] == 200:
        speech = "Name: Aniq, Login sucessful"
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
