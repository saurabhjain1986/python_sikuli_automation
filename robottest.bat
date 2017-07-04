@echo off

set sikulix_jar=%SIKULIX_HOME%\sikulixapi.jar
set robot_framework_jar=%ROBOTFRAMEWORK_JAR%
del results\screenshots\*.png
del results\matches\*.png
del results\*.*ml
mkdir results\screenshots
mkdir results\matches

java -cp "%robot_framework_jar%;%sikulix_jar%;dependencies/restfb-1.35.0.jar;dependencies/twitter4j-core-4.0.6.jar;dependencies/selenium-server-standalone-3.1.0.jar" ^
     -Dpython.path="%sikulix_jar%/Lib;dependencies" ^
     org.robotframework.RobotFramework ^
     --pythonpath=workspace.sikuli ^
     --outputdir=results ^
     --loglevel=TRACE ^
     %*