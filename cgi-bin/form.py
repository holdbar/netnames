#!/usr/bin/env python3

# import cgi     # Uncomment if python-cgi-server is used
# import cgitb   # Uncomment if python-cgi-server is used
import subprocess

# cgitb.enable() # Uncomment if python-cgi-server is used

subprocess.call("python3 /var/www/html/cgi-bin/netnames.py") # Put here path to netnames.py. You can put all scripts in /cgi-bin folder

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Current Users</title>
        </head>
        <body>""")

print("<h1>Current Users</h1>")


with open("/var/www/html/cgi-bin/results",encoding='utf-8') as f:
    for line in f:
        print("<p> {}</p>".format(line))

print("""</body>
        </html>""")
