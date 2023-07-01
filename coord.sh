#!/bin/bash
# Show the coord of the mouse on screen
# first run xinput and find the id of your mouse/touchpad
# replace 12 below with that id
watch -n 0.01 "xinput --query-state 12 | grep valuator"
