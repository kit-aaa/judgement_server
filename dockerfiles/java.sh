#!/bin/sh

javac /opt/test/*.java > /dev/null
java -classpath "/opt/test/" "${MAIN_CLASS}" "${TEST_INPUT}"
