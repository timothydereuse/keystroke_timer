# keystroke_timer
Because I didn't find anything that worked like I wanted it to on Windows!

A quick utility to log time and character of keystrokes. Writes the results to a .csv file in rows of (time in ms, character, press or release). Requires ```pynput```.

Usage: ```keystroke_listener.py -f FILE [-q] [-r]```
* ```-f``` specifies the filename to write the results to in CSV format
* ```-q``` specifies quiet mode (suppress all messages to stdout)
* ```-r``` includes key releases in the output .csv as well as keypresses.





