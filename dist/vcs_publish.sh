#!/bin/bash

BBUSER=abudden
BBPROJ=taghighlight

HEPTAPOD=ssh://hg@heptapod.host/cgtk/taghighlight

hg push $HEPTAPOD
# Only fail on error, not on "no changes to push"
if [ $? -gt 1 ]
then
	exit 255
fi
