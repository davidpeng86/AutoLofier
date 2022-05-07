# AutoLofier
Make all your music Lofi-esque!!!

### How to use:
__Make sure there are NO SPACES in your folder and file names__
  
Put script in folder and edit *source* in the script

Open Audacity and enable 'mod-script-pipe' in preference

The file hierchy should be:

> autolofi.py
>> artistfolder
>>>  albumfolder
>>>>    songs

Run the script.

To edit, change parameters in "do_command" according to [Script Reference](https://manual.audacityteam.org/man/scripting_reference.html)

'''
do_command('ChangePitch:percentage=%d' % -5)
'''


All results should be in a newly created result folder.
