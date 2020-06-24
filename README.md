# CopyPasteUserbot
Setup telegram api in ```config.py``` and then run it with ```main.py```
## Available commands
- `.dump` - dumps a message reply
- `.user` {userID} - dumps a user by id
- `.copy [name]`, `.c [name]`, `.+ [name]` - copy message reply to buffer or storage if name specified
- `.paste [name]`, `.p [name]`, `.= [name]` - paste message from buffer or by name if specified
- `.remove [name]`, `.r [name]`, `.- [name]` - remove message from buffer or by name if specified
- `.all` - prints all saved copies 