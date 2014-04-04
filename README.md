Attempt to create simple irc framework.    
This is just a proof of concept.    
Working on sockets.    

Many thanks to maciej01.    

Requires Tkinter for gui (pip install Tkinter)

Commands:    
| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |

:j channel - joins a channel    
:q - quits the bot    
:ch channel - sets the default channel to send messages and output to specified channel    
:l message - sends back the previous message, the parameter is not necessary, it appends it at end    
:p user/channel message - sends a private message to specified user or channel    
:r input - sends raw messages to server, for ex PRIVMSG #channel :message    
:ms id message - definies a message to use later    
:md id - sends the specified message    
:vs variable text - definied a variable to use later [without $ before variable]    
:v text - sends text, but with variables replaced to their values [with $ before variables]    
:n/:names [channel] - shows list of users for default channel, the channel argument is optional    

Predefinied variables:    
$hl - last user that highlighted    
$lm - last message you sent    
