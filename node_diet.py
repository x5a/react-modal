import os, sys, json
from subprocess import call

def run():
    dirs = ["node_modules", ".git"]

    package = json.load(open("package.json"))
    m = package.get("main", None)
    if os.path.isfile(m + ".js"):
        if m.split("/")[0] == ".":
            assert len(m.split("/")) > 2
            dirs.append(m.split("/")[1])
        else:
            assert len(m.split("/")) > 1
            dirs.append(m.split("/")[0])
    else:
        raise Exception("Unable to find isolated entry point - exiting without modification")

    dirs = set(dirs)

    for d in os.listdir(CWD):
        if os.path.isdir(os.path.join(CWD, d)) and d not in dirs:
            print "removing %s" % d
            call(["git", "rm", "-rf", d])
            call(["rm", "-rf", d])

    allowed_files = {"node_diet.py","package.json", "LICENSE"}

    for f in os.listdir(CWD):
        if os.path.isfile(os.path.join(CWD, f)) and f not in allowed_files:
            print "removing %s" % f
            # os.remove(os.path.join(CWD, f))
            call(["git", "rm", "-f", f])

    forbidden_modules = {"classnames", "lodash", "react"}
    nm = os.path.join(CWD, "node_modules")
    mods_left = False
    if os.path.isdir(nm):
        for f in os.listdir(nm):
            d = os.path.join(nm, f)
            rd = os.path.join("node_modules", f)
            if os.path.isdir(d) and f in forbidden_modules:
                print "removing %s" % d
                call(["git", "rm", "-rf", rd])
                # call(["rm", "-rf", d])
            else:
                mods_left = True
    if not mods_left:
        call(["git", "rm", "-rf", nm])
        # call(["rm", "-rf", nm])

    for p in ["readme", "keywords", "scripts", "bugs", "homepage", "jest"]:
        package.pop(p)
    with open("package.json", "wb") as f:
        json.dump(f, package, sort_keys=True, indent=2, separators=(',', ': '))

CWD = os.getcwd()
print("We're about to put your package on an aggressive diet.")
print("WE WILL REMOVE FORCEFULLY. MAKE SURE YOU'RE CHECKED IN.")
RUN = False
while True:
    try:
        p = raw_input("enter path [%s]: " % CWD)
        if p == "q":
            break
        CWD = os.path.abspath(os.path.expanduser(p))
        if os.path.isfile(os.path.join(CWD,"package.json")):
            s = raw_input("path is [%s] are you sure? [n]: " % CWD)
            if s.lower()[0] == "y":
                RUN = True
                break
        else:
            print("no package.json file found!")
    except Exception as e:
        print(e)
        print("I don't understand what you entered")

if RUN:
    os.chdir(CWD)
    run()
