def getDarkSky(intent, session):
    session_attributes = {}
    card_title = "Dark Sky Weather"
    darkSkyReport = reportDarkSky()
    speech_output = darkSkyReport + " Would you like to hear something else?"
    reprompt_text = "I must be deaf, what did you say?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def reportDarkSky():
    #Get API key from https://developer.forecast.io/
    url = "https://api.forecast.io/forecast/YOUR_KEY/34.052659,-118.248575?exclude=[minutely,hourly]"
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    timestamp = data['currently']['time']
    currentTime = convertTime2(timestamp)
    currentTemp = data['currently']['temperature']
    currentCondition = data['currently']['summary']
    currentHumidity = data['currently']['humidity']
    currentWindspeed = data['currently']['windSpeed']
    windbearing = data['currently']['windBearing']
    dw = int(windbearing)
    directionnumber = round(((dw-11.25)/22.5),0)
    convertnumber=['North','North northeast','Northeast','East northeast','East','East southeast','Southeast','South southeast','South','South southwest','Southwest','West southwest','West','West northwest','Northwest','North northwest']
    dn = int(directionnumber)
    currentWindDirection = str(convertnumber[dn])
    pressure = data['currently']['pressure']
    dp = dp =float(pressure)
    currentPressure = str(round((dp*0.0295301),2))
    currentOzone = data['currently']['ozone']
    todayall = data['daily']['data']
    today = todayall[0]
    todaySummary = today['summary']
    todayHigh = int(today['temperatureMax'])
    HighTime = today['temperatureMaxTime']
    todayHighTime = convertTime2(HighTime)
    forecastSummary = data['daily']['summary']
    humidity = int(currentHumidity*100)

    darkskyReport = "Currently, the temperature is " + str(currentTemp) + ". Humidity is " +str(humidity) + "%. Wind speed is " + str(currentWindspeed) + " mph. The direction is " + str(currentWindDirection) + " . Pressure is " + str(currentPressure) + " millibars.  Ozone level is " + str(currentOzone) + ".  Conditions will be " + str(todaySummary) + " The high temperature will be " + str(todayHigh) + ", this will occur at " + str(todayHighTime) + " " + str(forecastSummary)
    return darkskyReport


def getTraffic(intent, session):
    session_attributes = {}
    card_title = "Real Time Traffic"
    trafficReport = reportTraffic()
    speech_output =  trafficReport + " Would you like to hear something else?"
    reprompt_text = "I must be deaf, what did you say?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def reportTraffic():
    url = "https://raw.githubusercontent.com/ekt1701/Alexa-Good-Morning/master/traffic.csv"
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    row=[]
    for row in cr:
        trafficOrigin = row[0]
        trafficDest = row[1]
    #Get API key from https://developers.google.com/maps/
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+trafficOrigin+"&destination="+trafficDest+"&departure_time=now&key=YOUR_KEY"
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    route = data['routes'][0]['legs'][0]['steps']
    durationtraffic = data['routes'][0]['legs'][0]['duration_in_traffic']['text']
    direct = []
    for step in route:
        directions = step['html_instructions']
        direct.append(directions)
    instructions = ', '.join(direct)

    temp = "<body"+str(instructions)+"</body"
    text = html2text(temp)

    replace = {
            "Dest" : " Dest"
            }
    text = multiple_replace(replace, text)

    reportTraffic = "Going to "+str(trafficDesc) + " will take about "+str(durationtraffic)+". Directions: Head "+str(text)

    return reportTraffic

def reportAirNow():
    #Get API key from  https://docs.airnowapi.org/account/request/
    url = 'http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=90247&distance=10&API_KEY=YOUR_KEY'
    r = urllib2.urlopen(url)
    json_text = r.read().decode('utf-8')
    aqresult = json.loads(json_text)
    air=[]
    for line in aqresult:
        reportTime = line['HourObserved']
        if "O3" in line['ParameterName']:
            airqi = "the ozone level as " + str(line['AQI']) + " which is rated "  + str(line['Category']['Name']) + "."
        elif "PM2.5" in line['ParameterName']:
            airqi = "The Air Quality as " + str(line['AQI']) + " which is rated "  + str(line['Category']['Name']) + "."
        air.append(airqi)
    airnowtemp = " ".join(air)
    reportAirnow = "Air Now reports " + airnowtemp
    return reportAirnow

def getTechCrunch(intent, sessions):
    session_attributes = {}
    card_title = "TechCrunch"
    techCrunchReport = reportTechCrunch()
    speech_output =  techCrunchReport + "  Would you like to hear something else?"
    should_end_session = False
    reprompt_text = "No joy, say again."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def reportTechCrunch():
    #Get api from https://newsapi.org/
    url = 'https://newsapi.org/v1/articles?source=techcrunch&sortBy=latest&apiKey=YOUR_KEY'
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    newsreports = data['articles']

    titles = []
    for site in newsreports:
        title = site['title']
        desc = site['description']
        titles.append(title + " " + desc + "<break time='1s'/>")

    reportTechCrunch = '. '.join(titles)
    return reportTechCrunch
