@echo off

set sikulix_jar=%SIKULIX_HOME%\sikulixapi.jar
set robot_framework_jar=%ROBOTFRAMEWORK_JAR%
del results\screenshots\*.png
del results\matches\*.png
del results\*.*ml
mkdir results\screenshots
mkdir results\matches

echo.
echo ----------------------------------
echo  Running test suite for first time
echo ----------------------------------
echo.


java -cp "%robot_framework_jar%;%sikulix_jar%;dependencies/restfb-1.35.0.jar;dependencies/twitter4j-core-4.0.6.jar;dependencies/selenium-server-standalone-3.1.0.jar" ^
     -Dpython.path="%sikulix_jar%/Lib;dependencies" ^
     org.robotframework.RobotFramework ^
     --pythonpath=workspace.sikuli ^
     --outputdir=results ^
     --loglevel=TRACE ^
     %*

:: we stop the script here if all the tests were OK
if errorlevel 1 goto DGTFO

echo.
echo ----------------------------
echo  All Tests passed, no rerun
echo ----------------------------
echo.

exit /b
:: otherwise we go for another round with the failing tests
:DGTFO
:: we keep a copy of the first log file
copy results\log.html results\first_run_log.html /Y

:: we launch the tests that failed

echo.
echo -----------------------------------------
echo  Re-running the failed tests (Attempt-1)
echo -----------------------------------------
echo.
java -cp "%robot_framework_jar%;%sikulix_jar%;dependencies/restfb-1.35.0.jar;dependencies/twitter4j-core-4.0.6.jar;dependencies/selenium-server-standalone-3.1.0.jar" ^
     -Dpython.path="%sikulix_jar%/Lib;dependencies" ^
     org.robotframework.RobotFramework ^
     --pythonpath=workspace.sikuli ^
     --outputdir=results ^
     --loglevel=TRACE ^
     --rerunfailed results/output.xml --output rerun.xml ^
     %*
:: Robot Framework generates file rerun.xml

:: we keep a copy of the second log file
copy results\log.html results\second_run_log.html /Y

:: Merging output files

echo.
echo ------------------------------------
echo   Generating consolidated report
echo ------------------------------------
echo.

cmd /c rebot --outputdir results --output output.xml --merge results/output.xml results/rerun.xml
:: Robot Framework generates a new output.xml

:: we stop the script here if all the tests were OK
if errorlevel 1 goto DGTFE

del results\first_run_log.html
del results\second_run_log.html
del results\rerun.xml

echo.
echo ----------------------------
echo  All Tests passed, no rerun
echo ----------------------------
echo.

exit /b
:: otherwise we go for another round with the failing tests
:DGTFE
:: we keep a copy of the first log file
copy results\log.html results\first_run_log.html /Y

:: we launch the tests that failed

echo.
echo --------------------------------------------
echo   Re-running the failed tests (Attempt-2)
echo --------------------------------------------
echo.
java -cp "%robot_framework_jar%;%sikulix_jar%;dependencies/restfb-1.35.0.jar;dependencies/twitter4j-core-4.0.6.jar;dependencies/selenium-server-standalone-3.1.0.jar" ^
     -Dpython.path="%sikulix_jar%/Lib;dependencies" ^
     org.robotframework.RobotFramework ^
     --pythonpath=workspace.sikuli ^
     --outputdir=results ^
     --loglevel=TRACE ^
     --rerunfailed results/output.xml --output rerun.xml ^
     %*
:: Robot Framework generates file rerun.xml

:: we keep a copy of the second log file
copy results\log.html results\second_run_log.html /Y

:: Merging output files

echo.
echo ------------------------------------
echo   Generating consolidated report
echo ------------------------------------
echo.

cmd /c rebot --outputdir results --output output.xml --merge results/output.xml results/rerun.xml
:: Robot Framework generates a new output.xml

