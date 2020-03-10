from flask import Flask,request,make_response
import os,json
import pyowm
import os


app = Flask(__name__)
owmapikey='6628ad3fd90a97fb39ff9793c7569874' #or provide your key here
owm = pyowm.OWM(owmapikey)


#geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    if data['queryResult']['queryText'] == 'yes':
        reply = {
            "fulfillmentText": "Ok. Tickets booked successfully.",
        }
        return jsonify(reply)

    elif data['queryResult']['queryText'] == 'no':
        reply = {
            "fulfillmentText": "Ok. Booking cancelled.",
        }
        return jsonify(reply)

###processing the request from dialogflow
##def processRequest(req):
##    
##    result = req.get("queryResult")
##    parameters = result.get("parameters")
##    city = parameters.get("ph_no")
##
##    url = 'http://20.46.150.26/api/users/resend_verification_code/'
##    myobj = {'ph_no': city}
##
##    requests.post(url, data = myobj)
##    speech = "here1"
##
##    return {
##        "fulfillmentText": speech,
##        "source": "dialogflow-weather-by-satheshrgs"
##    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
