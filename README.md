Attempt to create simple irc framework.    
This is just a proof of concept.    
Working on sockets.    

Many thanks to maciej01.    

Commands:    
:j channel - joins a channel    
:q - quits the bot    
:ch channel - sets the default channel to send messages and output to specified channel    
:l message - sends back the previous message, the parameter is not necessary, it appends it at end    
:p user/channel message - sends a private message to specified user or channel    
:r input - sends raw messages to server, for ex PRIVMSG #channel :message    
:ms id message - definies a message to use later    
:md id - sends the specified message    