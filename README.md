# Alexa-Good-Morning

This skill allows you to customize Alexa's response using a csv file.  You can set the greeting and then the order of items you want to hear when you open the skill.

Currently you can select from these items: todo, traffic, weather, forecast, humidity, pressure, astronomy, surf, quake, air, news, stocks, quote, joke or cat.

The todo and traffic require a separate csv file.  Sample files are posted.

The csv files need to be hosted somewhere.  Personally, I saved the csv files to DropBox, which can easily be edited with a text editor. (Note when you get the link from DropBox change ?dl=0 to ?raw=1)

I have also included an others modules.  These items require you to register for an API key to use those services.

If you have other useful or fun API's, please let me know.

The configuration is Runtime: Python 2.7, Handler: lambda_function.lambda_handler, Existing Role: lambda_basic_execution. The code is entered in-line.

Possibly to do:
Allowing the skill to select different csv configurations depending on the time or day of the week.

