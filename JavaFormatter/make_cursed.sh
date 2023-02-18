#!/bin/sh

set -Cef

IFS=$(echo -e '\n+')
IFS=${IFS%?}
BASEDIR=$(dirname "$0")

if [ "$#" -eq "0" ]
then
	java -jar "${BASEDIR}/bin/ReplaceUtf8.jar" |
		java -jar "${BASEDIR}/bin/ReplaceTabs.jar" |
		java -jar "${BASEDIR}/bin/MakeCursed.jar"
else
	java -jar "${BASEDIR}/bin/ReplaceUtf8.jar" "$1" |
		java -jar "${BASEDIR}/bin/ReplaceTabs.jar" |
		java -jar "${BASEDIR}/bin/MakeCursed.jar"
fi
