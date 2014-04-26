##iWi GUI - an irc client - from humans, for humans   

**Created by Reyuu and maciej01.**    

![That's my son!](http://www.maciej01.tk/bb32f80c44.png)

###Commands:    
| Command | Parameters  | Description |
| :------------: |:---------------:| :-----:|
| :j | [channel] | joins a specified channel |
| :q |  | quits the client |
| :ch | [channel] | changes the default output channel to a specified one|
|:l|[message]|sends the previous message, the parameter appends something to end - **optional param**|
|:p|[user/channel]|sends a private message to specified user or channel|
|:r|[raw data]|sends raw data to server, for ex. PRIVMSG #channel :hi|
|:ms|[id] [message]|predefinies a message to use later|
|:md|[id]|sends an already definied (by :ms) message|
|:vs|[variable] [content]|definies a variable to use later [without $ before variable]|
|:v|[message]|sends a message, but with variables replaced to their values [with $ before variables]|
|:n/:names|[channel]|shows a list of users for default channel, **the channel argument is optional**|
|:part|[channel]|quits from a specified channel|
|:nick|[nick]|changes your nick|
|:me|[action]|sends an action to a specified channel|

###Predefinied variables:     
| Variable | Description |
| :------: | :---------: |
| $hl | last user that higlighted you |
| $lm | last message you sent|

###Requirements:    
* Python 2.7 - get it from [the official python website](https://www.python.org/download/releases/2.7.6/)
* Tkinter - install it using [pip](https://pypi.python.org/pypi/pip) - *pip install Tkinter*

Highlight sound is at the moment only getting played on Windows OS - due to usage of winsound package.

#Enjoy!
