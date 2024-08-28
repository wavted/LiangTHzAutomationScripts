# Steps For Execution
 
1. Arrange windows on BLC/Mag computer according to screenshot 
2. Specify parameters and run FlexibleBLCFullAutoGenScript.py (it will print the estimated duration of the experiment in the python terminal)
3. Run the generated xxxxx.ahk file on BLC/Mag computer
4. Make sure that the ‘laser’ and ‘emitter’ are turned on and ‘run’ is turned off
5. Save one scan manually to the desired file directory 
6. Make sure ‘wait’ button on the toptica system is pressed down
7. Press alt+z to execute the script
8. The automation script will play a sound every time a critical event is happening (i.e. changing temperature/field, starting/ending measurements)
9. Close the script by right clicking the task bar icon to stop execution 


# Parameters to Specify (BLC) In FlexibleBLCFullAutoGenScript.py
Sample/Reference Name and Directory
How many scans per temperature
List of temperatures to go to
Temperature offset between cryostat heater and sample heater
Temperature change rate (time between temperature change)
Motor Move Time

# Parameters to Specify (Magnet) In FlexibleMagFullAutoGenScript.py

Sample/Reference Name and Directory
How many scans per field
List of fields to go to
Magnet Ramp Rate
Motor Move Time