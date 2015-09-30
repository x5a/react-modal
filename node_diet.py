import os, sys, simplejson
from subprocess import call

def run():
    dirs = ["node_modules"]

    package = simplejson.load(open("package.json"))
    main = package.get("main", None)

    if os.path.isfile(main):
        assert len(main.split("/")) > 1
        dirs.append(main.split("/")[0])
    else:
        raise Exception("Unable to find isolated entry point - exiting without modification")

    dirs = ["%s/" % d for d in dirs]
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
            os.remove(os.path.join(CWD, f))

    forbidden_modules = {"classnames", "lodash", "react"}
    nm = os.path.join(CWD, "node_modules")
    mods_left = False
    if os.path.isdir(nm):
        for f in os.listdir(nm):
            d = os.path.join(nm, f)
            if os.path.isdir(d) and f in forbidden_modules:
                print "removing %s" % d
                call(["git", "rm", "-rf", d])
                call(["rm", "-rf", d])
            else:
                mods_left = True
    if not mods_left:
        call(["git", "rm", "-rf", nm])
        call(["rm", "-rf", nm])

    for p in ["readme", "keywords", "scripts", "bugs", "homepage", "jest"]:
        package.pop(p)
    with open("package.json", "wb") as f:
        json.dump(f, package, sort_keys=True, indent=2, separators=(',', ': '))

CWD = os.getcwd()
print("We're about to put your package on an aggressive diet.")
print("WE WILL REMOVE FORCEFULLY. MAKE SURE YOU'RE CHECKED IN.")
while True:
    try:
        p = input("enter path [%s]: " % CWD)
        CWD = os.path.abspath(os.path.expanduser(p))
        if os.path.isfile(os.path.join(CWD,"package.json"))
            s = input("are you sure? [n]: ")
            if s.lower()[0] == "y":
                break
        else:
            print("no package.json file found!")
    except:
        print("I don't understand what you entered")

os.chdir(CWD)
run()
