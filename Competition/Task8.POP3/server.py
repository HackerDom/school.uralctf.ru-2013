#!/usr/bin/python
# -*- coding: utf-8 -*-

"""server: a file-based pop3 server

Usage:
    python server.py <port> <path_to_message_file>
"""
import logging
import os
import socket
import sys

logging.basicConfig(filename="/var/log/pop3.log", format="%(name)s %(levelname)s - %(message)s")
log = logging.getLogger("server")
log.setLevel(logging.DEBUG)


class ChatterboxConnection(object):
    END = "\r\n"

    def __init__(self, conn):
        self.conn = conn
        self.dispatch = {'USER': self.handleUser, 'PASS': self.handlePass, 'STAT': self.handleStat,
                         'LIST': self.handleList, 'TOP': self.handleTop, 'DELE': self.handleNoop,
                         'RETR': self.handleRetr, 'NOOP': self.handleNoop, 'QUIT': self.handleQuit}
        self.user = ""
        self.authorized = 0

    def __getattr__(self, name):
        return getattr(self.conn, name)

    def sendall(self, data, END=END):
        if len(data) < 50:
            log.debug("send: %r", data)
        else:
            log.debug("send: %r...", data[:50])
        data += END
        self.conn.sendall(data)

    def recvall(self, END=END):
        data = []
        while True:
            chunk = self.conn.recv(4096)
            if END in chunk:
                data.append(chunk[:chunk.index(END)])
                break
            data.append(chunk)
            if len(data) > 1:
                pair = data[-2] + data[-1]
                if END in pair:
                    data[-2] = pair[:pair.index(END)]
                    data.pop()
                    break
        log.debug("recv: %r", "".join(data))
        return "".join(data)

    def handleUser(self, data, msg):
        try:
            cmd, self.user = data.split()
        except ValueError:
            return "-ERR you must send name"
        else:
            if self.user == "user":
                return "+OK it is a valid mailbox"
            else:
                return "-ERR never heard of mailbox %s" % self.user

    def handlePass(self, data, msg):
        if self.user == "user":
            if data == "PASS passw0rd":
                self.authorized = 1
                return "+OK user authorized"
            return "-ERR invalid password"
        else:
            return "-ERR send me your name firstly"

    def handleStat(self, data, msg):
        if not self.authorized:
            return "-ERR authorize firstly"
        return "+OK 1 %i" % msg.size

    def handleList(self, data, msg):
        if not self.authorized:
            return "-ERR authorize firstly"
        return "+OK 1 messages (%i octets)\r\n1 %i\r\n." % (msg.size, msg.size)

    def handleTop(self, data, msg):
        if not self.authorized:
            return "-ERR authorize firstly"
        try:
            cmd, num, lines = data.split()
        except ValueError:
            return "-ERR send me message number and number of lines"
        else:
            if num != "1":
                return "-ERR unknown message number: %s" % num
            lines = int(lines)
            text = msg.top + "\r\n\r\n" + "\r\n".join(msg.bot[:lines])
            return "+OK top of message follows\r\n%s\r\n." % text

    def handleRetr(self, data, msg):
        if not self.authorized:
            return "-ERR authorize firstly"
        try:
            cmd, num = data.split()
        except ValueError:
            return "-ERR send me a number of message"
        else:
            if num != "1":
                return "-ERR unknown message number: %s" % num
            log.info("message sent")
            return "+OK %i octets\r\n%s\r\n." % (msg.size, msg.data)

    def handleNoop(self, data, msg):
        return "+OK"

    def handleQuit(self, data, msg):
        return "+OK POP3 server signing off"


class Message(object):
    def __init__(self, filename):
        msg = open(filename, "r")
        try:
            self.data = data = msg.read()
            self.size = len(data)
            self.top, bot = data.split("\n\n", 1)
            self.bot = bot.split("\n")
        except Exception as e:
            log.error("Bad message file: {}".format(e))
        finally:
            msg.close()


def serve(host, port, filename):
    """
    :param host:
    :param port:
    :param filename:
    """
    assert os.path.exists(filename)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    try:
        if host:
            hostname = host
        else:
            hostname = "localhost"
        log.info("POP3 serving '%s' on %s:%s", filename, hostname, port)
        while True:
            sock.listen(200)
            conn, addr = sock.accept()
            log.debug('Connected by %s', addr)
            try:
                msg = Message(filename)
                conn = ChatterboxConnection(conn)
                conn.sendall("+OK Welcome to our POP3 server!")
                while True:
                    data = conn.recvall()
                    if not data.split(None, 1):
                        continue
                    command = data.split(None, 1)[0]
                    try:
                        cmd = conn.dispatch[command]
                    except KeyError:
                        conn.sendall("-ERR unknown command")
                    else:
                        conn.sendall(cmd(data, msg))
                        if cmd == conn.handleQuit:
                            break
            finally:
                conn.close()
                msg = None

    except (SystemExit, KeyboardInterrupt):
        log.info("Server stopped")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit(0)
    except Exception, ex:
        log.critical("fatal error", exc_info=ex)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: [<host>:]<port> <path_to_message_file>"
    else:
        _, port, filename = sys.argv
        if ":" in port:
            host = port[:port.index(":")]
            port = port[port.index(":") + 1:]
        else:
            host = ""
        try:
            port = int(port)
        except Exception:
            print "Unknown port:", port
        else:
            if os.path.exists(filename):
                while True:
                    serve(host, port, filename)
            else:
                print "File not found:", filename
