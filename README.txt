pip install selenium

If it is not running properly could be from the time.sleep() timers - Adjust them +5 like.. time.sleep(5)

Also the program could not start properly without having geckodriver installed and the path added to "Edit environment variables" into PATH
On my pc is set like this in PATH "D:\Projects\pyproj\geckodriver" where the .exe file is

The csv file is usually created in the environment's main folder and it is not necessary to appear in the project's folder.
