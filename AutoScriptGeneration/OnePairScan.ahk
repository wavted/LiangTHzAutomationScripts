


CoordMode, Mouse, Screen
Click, %motorPosition%

CoordMode, Mouse, Screen
Click, %motorPosition%
Sleep,341
CoordMode, Mouse, Screen
Click, %motorPosition%
Sleep,341
CoordMode, Mouse, Screen
Click, %motorPosition%


Sleep, %motorWaittime%

CoordMode, Mouse, Screen
Click, %topticaTopBarPosition%

Sleep,341

CoordMode, Mouse, Screen
Click, %topticaTopBarPosition%

Sleep,341


CoordMode, Mouse, Screen
Click, %topticaTopBarPosition%
Sleep,341



SendEvent {F9}

Sleep,341
Sleep,341
Sleep,341

SendEvent {F8}

Sleep,%scanWaitTime%

CoordMode, Mouse, Screen
Click, %topticaTopBarPosition%
Sleep,240

SendEvent {F11}
Sleep,341
Sleep,200

Send %sampleName%_%temp%_%field%_%scanIndex%

Sleep,450
SendEvent {Enter}
Sleep,341
