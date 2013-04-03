#!/usr/bin/python
import datetime
from random import randint

__author__ = 'Messiah'
logString = '{date} {time} {user} CMD: "{cmd}"\n'
users = []
commands = {0: ["ps", "ls", "ls -la", "cd", "top", "date", "cal", "uptime", "w", "whoami",
                "uname -a", "cat /proc/cpuinfo", "cat /proc/meminfo", "df", "du", "free"],
            1: ["ls ", "ls -la ", "cd ", "rm ", "rm -r ", "rm -f ", "rm -rf ", "touch ",
                "cat >  ", "more ", "head ", "tail ", "tail -f ", "chmod +x "],
            2: ["cp ", "cp -r ", "mv ", "ln -s ", "grep "],
            3: ["ssh root@", "ping ", "whois ", "dig "]}
paths = {0: ["etc", "mnt", "opt", "share", "home", "root", "tmp", "var"],
         2: ["Documents", "Hello", "Music", "configs", ".ssh", "pictures",
             "nginx", "www", "my_folder", "Dropbox", "projects", ".config", "files"],
         3: ["my_file", ".bashrc", "file", "readme.txt", "picture.jpg", "config.cfg",
             "httpd.conf", "index.php", "index.html", "index.py", "about.html"]}

dns = {0: ["home", "some", "host", "ip", "admin", "mail", "front", "web", "post", "analyzer", "user", "gateway",
           "peer", "a", "b", "c", "d", "e", "f", "0day", "ftp", "router", "dns", "dhcp", "smb", "design"],
       1: ["e1", "wiki", "google", "mail", "domain", "irc", "ucoz", "telenet", "ructf", "urfu", "xakep"],
       2: ["ru", "com", "org", "net", "su", "uk", "zh", "fi", "fr", "pl", "py"]}


def generatePath(user):
    result = ""
    for i in range(4):
        if i == 1:
            result += "/" + user
            continue
        if i == 2:
            if randint(0, 1) == 0:
                continue
        result += "/" + paths[i][randint(0, len(paths[i]) - 1)]
    return result


def generateHost():
    result = ""
    for i in range(3):
        if (i == 1) and (randint(0, 1) == 0):
            continue
        result += dns[i][randint(0, len(dns[i]) - 1)] + "."
    return result[:-1]


def main():
    log = open("secure.log", "w")
    start = datetime.date(1941, 1, 1)
    finish = datetime.date(2013, 4, 5)
    delta = (finish - start).days
    for day in range(delta):
        date = start + datetime.timedelta(days=day)
        times = ["{:02}:{:02}:{:02},{:03}".format(randint(0, 23),
                                          randint(0, 59),
                                          randint(0, 59),
                                          randint(0, 999)) for i in range(randint(3, 10))]
        times.sort()
        for time in times:
            username = users[randint(0, len(users) - 1)]
            user = "(" + username + "):"
            while len(user) < 27:
                user += ' '
            command = ""
            for i in range(randint(1, 5)):
                args = randint(0, 3)
                cmd = commands[args][randint(0, len(commands[args]) - 1)]
                if args == 1:
                    cmd += generatePath(username)
                elif args == 2:
                    cmd += generatePath(username) + " " + generatePath(username)
                elif args == 3:
                    cmd += generateHost()
                if i == 0:
                    command = cmd
                else:
                    command += " && " + cmd
            log.write(logString.format(date=date, time=time, user=user, cmd=command))


if __name__ == '__main__':
    try:
        f = open("bruteforce.txt", "r").readlines()[22:]
    except:
        print "I can't read file"
        exit(1)
    else:
        for name in f:
            try:
                users.append(name.split()[1])
            except:
                pass
    main()
