import json
import re
import urllib2
import csv
import random
import xml.etree.ElementTree as ElementTree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "getForecastIntent":
        return getForecast(intent, session)
    elif intent_name == "getCurrentIntent":
        return getCurrent(intent, session)
    elif intent_name == "getAstronomyIntent":
        return getAstronomy(intent, session)
    elif intent_name == "getHumidIntent":
        return getHumidity(intent, session)
    elif intent_name == "getPressureIntent":
        return getPressure(intent, session)
    elif intent_name == "getSurfIntent":
        return getSurf(intent, session)
    elif intent_name == "getEarthquakeIntent":
        return getEarthquake(intent, session)
    elif intent_name == "getAirQualityIntent":
        return getAirQuality(intent, session)
    elif intent_name == "getHeadlineNewsIntent":
        return getHeadlineNews(intent, session)
    elif intent_name == "getRandomQuoteIntent":
        return getRandomQuote(intent, session)
    elif intent_name == "getJokeIntent":
        return getJoke(intent, session)
    elif intent_name == "getCatFactsIntent":
        return getCatFacts(intent, session)
    elif intent_name == "getStocksIntent":
        return getStocks(intent, session)
    elif intent_name == "getTrafficIntent":
        return getTraffic(intent, session)
    elif intent_name == "getTodoIntent":
        return getTodo(intent, session)
    elif intent_name == "getRepeatIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.NoIntent":
        return signoff()
    elif intent_name == "AMAZON.YesIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"

    # Get your greeting and generate the report
    url = 'https://raw.githubusercontent.com/ekt1701/Alexa-Good-Morning/master/morning.csv'
    response = urllib2.urlopen(url)
    contents = csv.reader(response)
    records = []
    element = ""
    report = ""

    for row in contents:
        greeting = row[0]
        for element in row:
            if element == "todo":
                report = reportTodo()
            elif element == "traffic":
                report = reportTraffic()
            elif element == "weather":
                report = reportCurrent()
            elif element == "forecast":
                report = reportForecast()
            elif element == "humidity":
                report = reportHumidity()
            elif element == "pressure":
                report = reportPressure()
            elif element == "astronomy":
                report = reportAstronomy()
            elif element == "surf":
                report = reportSurf()
            elif element == "quake":
                report = reportEarthquake()
            elif element == "air":
                report = reportAirQuality()
            elif element == "news":
                report = reportHeadlineNews()
            elif element == "quote":
                report = reportRandomQuote()
            elif element == "cat":
                report = reportCatFacts()
            elif element == "joke":
                report = reportJoke()
            elif element == "stocks":
                report = reportStocks()
            records.append(report)
        myReport = ' '.join(records)
    speech_output = str(greeting) + " " + str(myReport) + " Is there anything else you want to hear?"
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help():
    session_attributes = {}
    card_title = "Help"
    speech_output = " You can say current, forecast, humidity, pressure, astronomy, surf, earthquakes, air quality, news, stocks, quote, positive, joke or cat. What would you like to hear?"
    should_end_session = False
    reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getTodo(intent, session):
    session_attributes = {}
    card_title = "My Todo"
    todoReport = reportTodo()
    speech_output = todoReport + "  Would you like to hear something else?"
    reprompt_text = "I must be deaf, what did you say?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportTodo():
    url = 'https://raw.githubusercontent.com/ekt1701/Alexa-Good-Morning/master/todo.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    todo = ""
    for row in cr:
        for element in row:
            todo = todo + element
    reportTodo = "Here are the things you need to do " + todo
    return reportTodo


def getTraffic(intent, session):
    session_attributes = {}
    card_title = "Traffic Time"
    trafficReport = reportTraffic()
    speech_output = trafficReport + "  Would you like to hear something else?"
    reprompt_text = "I must be deaf, what did you say?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportTraffic():
    url = "https://raw.githubusercontent.com/ekt1701/Alexa-Good-Morning/master/traffic.csv"
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    row = []
    for row in cr:
        trafficOrigin = row[0]
        trafficDest = row[1]

    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + trafficOrigin + "&destination=" + trafficDest
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    duration = data['routes'][0]['legs'][0]['duration']['text']
    route = data['routes'][0]['legs'][0]['steps']
    direct = []
    for step in route:
        directions = step['html_instructions']
        direct.append(directions)
    instructions = ', '.join(direct)

    temp = "<body" + str(instructions) + "</body"
    text = html2text(temp)

    replace = {
        "Dest": " Dest"
    }
    text = multiple_replace(replace, text)
    reportTraffic = "Average traffic time to your destination is " + str(duration) + " Here are the Directions: Head " + str(text)
    return reportTraffic


def getCurrent(intent, session):
    session_attributes = {}
    card_title = "Current Weather"
    currentReport = reportCurrent()
    session_attributes = {}
    speech_output = currentReport + "  Would you like to hear something else?"
    reprompt_text = "I must be deaf, what did you say?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportCurrent():
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%3D12795729&format=json"
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    title = data['query']['results']['channel']['item']['title']
    temp = data['query']['results']['channel']['item']['condition']['temp']
    status = data['query']['results']['channel']['item']['condition']['text']
    humidity = data['query']['results']['channel']['atmosphere']['humidity']
    temppressure = data['query']['results']['channel']['atmosphere']['pressure']
    rising = data['query']['results']['channel']['atmosphere']['rising']
    dp = float(temppressure)
    pressure = str(round((dp * 0.0295301), 2))
    if rising == 1:
        rising = "Rising"
    elif rising == 2:
        rising = "Falling"
    else:
        rising = "Steady"
    wind = data['query']['results']['channel']['wind']['speed']
    winddirection = data['query']['results']['channel']['wind']['direction']
    dw = int(winddirection)
    directionnumber = round(((dw - 11.25) / 22.5), 0)
    convertnumber = ['North', 'North northeast', 'Northeast', 'East northeast', 'East', 'East southeast', 'Southeast', 'South southeast', 'South', 'South southwest', 'Southwest', 'West southwest', 'West', 'West northwest', 'Northwest', 'North northwest']
    dn = int(directionnumber)
    directionstring = str(convertnumber[dn])
    forecast = data['query']['results']['channel']['item']['forecast']
    day0all = forecast[0]
    day0data = ". Today it will be " + day0all['text'] + " and " + day0all['high'] + " degrees. "
    currentReport = title + ". It is " + status + ". The temperature is " + temp + " degrees. Wind Speed is " + wind + " miles per hour, the direction is " + directionstring + ". The humidity is " + humidity + " percent. " + " The pressure is " + pressure + " millibars and is " + rising + day0data
    return currentReport


def getForecast(intent, session):
    session_attributes = {}
    card_title = "Weather Forecast"
    forecastReport = reportForecast()
    speech_output = forecastReport + "  Would you like to hear something else?"
    reprompt_text = "I must be deaf, what did you say?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportForecast():
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%3D12795652&format=json"
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    item = data['query']['results']['channel']['item']
    data = []
    for forecast in item['forecast'][1:6]:
        shortname = forecast['day']
        fullday = fullname(shortname)
        daydata = "On " + fullday + " it will be " + forecast['text'] + " and " + forecast['high'] + " degrees. "
        data.append(daydata)
    myForecast = ' '.join(data)
    forecast = "Here is your weather forecast " + str(myForecast)
    return forecast


def fullname(shortday):
    if shortday == "Mon":
        fullday = "Monday"
    if shortday == "Tue":
        fullday = "Tuesday"
    if shortday == "Wed":
        fullday = "Wednesday"
    if shortday == "Thu":
        fullday = "Thursday"
    if shortday == "Fri":
        fullday = "Friday"
    if shortday == "Sat":
        fullday = "Saturday"
    if shortday == "Sun":
        fullday = "Sunday"
    return fullday


def getHumidity(intent, session):
    session_attributes = {}
    card_title = "Humidity"
    humidityReport = reportHumidity()
    speech_output = humidityReport + "  Would you like to hear something else?"
    reprompt_text = "Audio error, please repeat your request."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportHumidity():
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20atmosphere%20from%20weather.forecast%20where%20woeid%3D12795652&format=json&diagnostics=true&callback="
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    humidity = data['query']['results']['channel']['atmosphere']['humidity']
    humidityReport = "The humidity is currently " + humidity + " percent."
    return humidityReport


def getPressure(intent, session):
    session_attributes = {}
    card_title = "Barometric Pressure"
    pressureReport = reportPressure()
    speech_output = pressureReport + " Would you like to hear something else?"
    reprompt_text = "I must be deaf, what did you say?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportPressure():
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20atmosphere%20from%20weather.forecast%20where%20woeid%3D12795652&format=json&diagnostics=true&callback="
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    temppressure = data['query']['results']['channel']['atmosphere']['pressure']
    rising = data['query']['results']['channel']['atmosphere']['rising']

    dp = float(temppressure)
    pressure = str(round((dp * 0.0295301), 2))

    if rising == 1:
        rising = "Rising"
    elif rising == 2:
        rising = "Falling"
    else:
        rising = "Steady"

    pressureReport = "The pressure is currently " + pressure + " millibars and is " + rising
    return pressureReport


def getAstronomy(intent, session):
    session_attributes = {}
    card_title = "Astronomy"
    astronomyReport = reportAstronomy()
    speech_output = astronomyReport + "  Would you like to hear something else?"
    reprompt_text = "I must be deaf, what did you say?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportAstronomy():
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20astronomy%20from%20weather.forecast%20where%20woeid%3D12795729&format=json&diagnostics=true&callback="
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))

    sunrise = data['query']['results']['channel']['astronomy']['sunrise']
    sunset = data['query']['results']['channel']['astronomy']['sunset']

    riseA, riseB = sunrise.split(":")
    setA, setB = sunset.split(":")

    if len(setB) == 4:
        timesunset = setA + ":" + "0" + setB
    else:
        timesunset = sunset

    if len(riseB) == 4:
        timesunrise = riseA + ":" + "0" + riseB
    else:
        timesunrise = sunrise

    url = "http://api.burningsoul.in/moon"
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))

    moonphase = data['stage']
    moonillumination = data['illumination']

    textillumination = str(moonillumination)

    illumationpercent, splitB = textillumination.split(".")
    fullmoon = str(data['FM']['DT'])
    fullmoonA, fullmoonB = fullmoon.split("-")
    astronomyReport = "Sunrise is at " + timesunrise + ". Sunset is at " + timesunset + ". Moon phase is " + moonphase + ". Illumination is at " + illumationpercent + " percent. Full moon will be on " + fullmoonB
    return astronomyReport


def getSurf(intent, session):
    session_attributes = {}
    card_title = "Surf Conditions"
    surfReport = "I'm sorry the surf report is currently broken."
    speech_output = surfReport + ".   Would you like to hear something else?"
    reprompt_text = "Audio error, please repeat your request."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportSurf():
    url = "http://tgftp.nws.noaa.gov/data/raw/fz/fzus56.klox.srf.lox.txt"
    html = urllib2.urlopen(url).read()
    text = re.search(r'(?<=CAZ041)(?s)(.+?)(?=LOW TIDE)', html).group()
    replace = {
        "[": "",
        "]": "",
        " FT": " feet",
        "RIP": " rip",
        "WATER": " WATER",
        "LIGHTNING": " LIGHTNING",
        "UV": " UV",
        "..M": "M",
        "..B": "B",
        "..H": "H",
        "\\n": ""
    }
    report = multiple_replace(replace, text)
    text = re.search(r'(?<=2017.)(?s)(.+?)(?=TIDES)', report).group()
    text = text.replace('*', ' ')
    text = re.sub('\.\.+', ' ', text)
    text = re.sub('\s+', ' ', text).strip()
    text = text.lower()
    surfReport = "Here are the surf conditions. " + text
    return surfReport


def getEarthquake(intent, session):
    session_attributes = {}
    card_title = "CA earthquakes"
    quakeReport = reportEarthquake()
    speech_output = quakeReport + "   Would you like to hear something else?"
    reprompt_text = "Audio error, please repeat your request."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportEarthquake():
    url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.csv'
    # Other feeds that are available for the Past Day.
    # url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.csv"
    # url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.csv"
    # url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv"
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    titles = []
    for row in cr:
        if "CA" in row[13]:
            event = row[4] + " magnitude, at " + row[13]
            titles.append(event)
        elif "California" in row[13]:
            event = row[4] + " magnitude, at " + row[13]
            titles.append(event)
    quake = '. '.join(titles)

    replace = {
        "'": "\\",
        "CA": "",
        "California": ""
    }

    quakereport = multiple_replace(replace, quake)

    if quakereport == "":
        quakeReport = "There were no magnitude 2.5 or larger earthquakes in California in the past day."
    else:
        quakeReport = "Here are the latest magnitude 2.5+ earthquakes in California " + str(quakereport)
    return quakeReport


def getAirQuality(intent, session):
    session_attributes = {}
    card_title = "Air Quality"
    airQualityReport = reportAirQuality()
    speech_output = airQualityReport + "   Would you like to hear something else?"
    reprompt_text = "Audio error, please repeat your request."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportAirQuality():
    aqicn_url = "http://feed.aqicn.org/feed/los-angeles/en/feed.v1.json"
    aqicn_response = urllib2.urlopen(aqicn_url)
    aqicn_data = json.loads(aqicn_response.read())
    date = aqicn_data['aqi']['date']
    aqi_value = aqicn_data['aqi']['val']
    rating = aqicn_data['aqi']['impact']
    if rating != "no data":
        o3_value = aqicn_data['iaqi']['o3']['val']
        co_value = aqicn_data['iaqi']['co']['val']
        no2_value = aqicn_data['iaqi']['no2']['val']
        airQualityReport = "On " + str(date) + ", the aqi is " + str(aqi_value) + ", which is " + rating + ". The ozone level was " + str(o3_value) + ". The carbon monoxide level was " + str(co_value) + ". The sulfur dioxide level was " + str(no2_value)
    else:
        airQualityReport = "The Air quality feed appears to be down, please try again later."
    return airQualityReport


def getHeadlineNews(intent, session):
    session_attributes = {}
    card_title = "Headline News"
    headlineNewsReport = reportHeadlineNews()
    speech_output = headlineNewsReport + "   Would you like to hear something else?"
    reprompt_text = "Input failed, please say again."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportHeadlineNews():
    url = "http://rss.cnn.com/rss/cnn_topstories.rss"
    req = urllib2.Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    try:
        xml = urllib2.urlopen(req).read()
        tree = ElementTree.fromstring(xml)
        data = []
        news = []
        for item in tree.findall('.//item'):
            for title in item.findall('.//title'):
                headline = title.text
                headline = headline.replace("%", " percent ").replace("&", " and ").replace(" & ", " and ").replace("- CNET", "")
                headline = re.sub('[^A-Za-z0-9]+\'', ' ', headline)
            for description in item.findall('.//description'):
                response = description.text
                result = re.sub(r'<(.|\n)+?>', '', response)
                result = re.sub("[\(\[].*?[\)\]]", "", result)
                result = result.replace("&#8217;", "'").replace("&#8211;", " ").replace("&#8212;", " ").replace("[&#8230;]", " ").replace("&#8220;", " ").replace("&#8221;", " ").replace("&#8230;", " ").replace("&ldquo;", " ").replace(" & ", " and ")
                result = result.replace("&hellip;", " ").replace("&nbsp;", " ").replace("&rsquo;", "'").replace("&#39;", "").replace("&raquo;", "")
                result = result.replace("&mdash;", " ").replace("&rdquo;", " ").replace('&#38;', ' and ').replace("&", " and ").replace("%", " percent ")
                result = re.sub('[^A-Za-z0-9]+\'', ' ', result)
                result = ' '.join(result.split())
            data.append(headline + ": <break time='250ms'/> " + result)
        for x in xrange(0, 5):
            result = data[x]
            news.append(result)
        news = " <break time='500ms'/> ".join(news)
        newsReport = news + " <break time='1s'/> "
    except:
        newsReport = "I'm sorry, there was an error with the news feed."
    return newsReport


def getRandomQuote(intent, session):
    session_attributes = {}
    card_title = "Random Quote"
    randomquoteReport = reportRandomQuote()
    speech_output = randomquoteReport + "   Would you like to hear something else?"
    reprompt_text = "Input failed, please say again."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportRandomQuote():
    randomwords = ['positive', 'funny', 'inspiration', 'nature', 'courage', 'laugh', 'tech', 'exercise', 'health', 'fitness', 'laughter', 'silly', 'sunny', 'happy', 'cheerful', 'animals', 'friendship', 'success', 'patience', 'love', 'peace']
    randomstring = str(randomwords[random.randint(0, 20)])
    url = "http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=1&q=https://www.quotesdaddy.com/feed/tagged/" + randomstring
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    RandomQuote = data['responseData']['feed']['entries']
    titles = []
    for site in RandomQuote:
        titles.append(site['title'])

    quoterandom = '. '.join(titles)
    randomquoteReport = "Here is a quote for you. " + quoterandom
    return randomquoteReport


def getCatFacts(intent, session):
    session_attributes = {}
    card_title = "Cat facts"
    catFactsReport = reportCatFacts()
    speech_output = catFactsReport + "   Would you like to hear something else?"
    reprompt_text = "Input failed, please say again."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportCatFacts():
    url = "http://catfacts-api.appspot.com/api/facts?number=1"
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    catfact = data['facts']
    temp = str(catfact)
    replace = {
        "'": "\'",
        "[u": "",
        "]": ""
    }
    webtext = multiple_replace(replace, temp)
    catFactsReport = "Here is a cat fact " + str(webtext)
    return catFactsReport


def getJoke(intent, session):
    session_attributes = {}
    card_title = "Random Jokes"
    jokeReport = reportJoke()
    speech_output = jokeReport + " Would you like to hear something else?"
    reprompt_text = "No joy, say again."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportJoke():
    i = random.randint(0, 99)
    if i < 50:
        url = "http://api.icndb.com/jokes/random"
        response = urllib2.urlopen(url)
        data = dict(json.loads(response.read()))
        randomjoke = data['value']['joke']
    else:
        url = "http://tambal.azurewebsites.net/joke/random"
        response = urllib2.urlopen(url)
        data = dict(json.loads(response.read()))
        randomjoke = data['joke']

    jokeReport = "Here is joke for you: " + randomjoke
    return jokeReport


def getStocks(intent, session):
    session_attributes = {}
    card_title = "Dow Jones"
    stockReport = reportStocks()
    speech_output = stockReport + "   Would you like to hear something else?"
    reprompt_text = "No joy, say again."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def reportStocks():
    # Stocklist Dow Jones, Amazon, Google
    stocklist = ["983582", "660463", "304466804484872"]
    myreport = []
    i = 0
    while i < len(stocklist):
        url = "https://www.google.com/finance?cid=" + stocklist[i]
        file = urllib2.urlopen(url)
        text = file.read()

        namelocation = '<title>(.+?):'
        pricelocation = '<span id="ref_' + stocklist[i] + '_l">(.+?)</span>'
        changelocation = '<span class="chg" id="ref_' + stocklist[i] + '_c">(.+?)</span>'
        changelocation2 = '<span class="chr" id="ref_' + stocklist[i] + '_c">(.+?)</span>'

        namepattern = re.compile(namelocation)
        pricepattern = re.compile(pricelocation)
        changepattern = re.compile(changelocation)
        changepattern2 = re.compile(changelocation2)

        name = re.findall(namepattern, text)
        price = re.findall(pricepattern, text)
        change = re.findall(changepattern, text)
        change2 = re.findall(changepattern2, text)

        stock = str(name) + " price was " + str(price) + " the change was " + str(change) + str(change2)

        replace = {
            "[": "",
            "]": ""
        }

        stockreport = multiple_replace(replace, stock)

        myreport.append(stockreport)
        i += 1
    stockReport = '. '.join(myreport)
    return stockReport


def signoff():
    session_attributes = {}
    card_title = "Signing off"
    speech_output = "This is your Info Center signing off"
    should_end_session = True
    reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    should_end_session = True
    return build_response({}, build_speechlet_response(
        None, None, None, should_end_session))


def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


def html2text(strText):
    str1 = strText
    int2 = str1.lower().find("<body")
    if int2 > 0:
        str1 = str1[int2:]
    int2 = str1.lower().find("</body>")
    if int2 > 0:
        str1 = str1[:int2]
    list1 = ['<br>', '<tr', '<td', '</p>', 'span>', 'li>', '</h', 'div>', '<em>', '</em>']
    list2 = [chr(13), chr(13), chr(9), chr(13), chr(13), chr(13), chr(13), chr(13), chr(13), chr(13)]
    bolFlag1 = True
    bolFlag2 = True
    strReturn = ""
    for int1 in range(len(str1)):
        str2 = str1[int1]
        for int2 in range(len(list1)):
            if str1[int1:int1 + len(list1[int2])].lower() == list1[int2]:
                strReturn = strReturn + list2[int2]
        if str1[int1:int1 + 7].lower() == '<script' or str1[int1:int1 + 9].lower() == '<noscript':
            bolFlag1 = False
        if str1[int1:int1 + 6].lower() == '<style':
            bolFlag1 = False
        if str1[int1:int1 + 7].lower() == '</style':
            bolFlag1 = True
        if str1[int1:int1 + 9].lower() == '</script>' or str1[int1:int1 + 11].lower() == '</noscript>':
            bolFlag1 = True
        if str2 == '<':
            bolFlag2 = False
        if bolFlag1 and bolFlag2 and (ord(str2) != 10):
            strReturn = strReturn + str2
        if str2 == '>':
            bolFlag2 = True
        if bolFlag1 and bolFlag2:
            strReturn = strReturn.replace(chr(32) + chr(13), chr(13))
            strReturn = strReturn.replace(chr(9) + chr(13), chr(13))
            strReturn = strReturn.replace(chr(13) + chr(32), chr(13))
            strReturn = strReturn.replace(chr(13) + chr(9), chr(13))
            strReturn = strReturn.replace(chr(13) + chr(13), chr(13))
    strReturn = strReturn.replace(chr(13), chr(32))
    return strReturn

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
