import os
from subprocess import call

CWD = os.getcwd()

dirs = ["examples","lib","specs","scripts"]
dirs = ["%s/" % d for d in dirs]

for d in dirs:
    if os.path.isdir(os.path.join(CWD, d)):
        call(["git", "rm", "-r", d])

ignored = set()
for line in open(".gitignore","r").readlines():
    if line in dirs:
        ignored.add(line)

with open(".gitignore","a") as f:
    for d in dirs:
        if os.path.isdir(os.path.join(CWD, d)) and d not in ignored:
            f.writeline(d)

allowed_files = {"node_diet.py","package.json", "LICENSE"}

for f in os.listdir(CWD):
    if os.path.isfile(os.path.join(CWD, f)) and f not in allowed_files:
        os.remove(os.path.join(CWD, f))
