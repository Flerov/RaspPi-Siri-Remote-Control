#! /usr/bin/env python3
# -*- coding: utf-8 -*-


# Imports
import os
import init
import imaplib
import threading
from time import sleep
from pkgutil import iter_modules
from email import message_from_string
import xml.etree.ElementTree as ElementTree


dateiname = "User-Daten.xml"


class PlaceholderException(Exception):
    pass


class ControlThread(threading.Thread):
    def __init__(self, command, module):
        super().__init__()
        self.command = command
        self.module = module

    def run(self):
        try:
            self.module.exc(self.command)
            print("\n-X Exit '{module_name}'\n".format(module_name=self.module))
        except Exception as exc:
            print("[ERROR] An error occurred while executing "
                  "{module_Name}: {error_Message}"
                  .format(module_Name=self.module,
                          error_Message=exc))
        finally:
            print("\n-X Exit '{module_name}'\n".format(module_name=self.module))


class Main():
    def __init__(self, dateiname):
        self.modules = []
        try:
            self.baum = ElementTree.parse(dateiname)
            self.tag_list = self.baum.getroot()
            self.email = self.tag_list.find("email")
            self.passwort = self.tag_list.find("passwort")
            self.liste = [self.email.text, self.passwort.text]
            self.login()
            print("\n----RaspPi-Siri-Vernsteuerung----\n")
            if True:
                print("\nLoading folders and modules...\n")
                self.moduleLoader()
                self.control()
        except FileNotFoundError:
            init.main()
        except EOFError:
            raise KeyboardInterrupt

    def login(self):
        data_email = self.liste[0]
        data_passwort = self.liste[1]
        try:
            self.email = imaplib.IMAP4_SSL("imap.gmail.com")
            self.email.login(data_email, data_passwort)
            self.email.list()
            self.email.select("Notes", True)

            typ, data = self.email.search(None, "ALL")
            try:
                self.check_latest = data[0].split()[-1]
                return True
            except IndexError:
                pass
        except imaplib.IMAP4.error:
            print("\nIMAP is not activated\n"
                  "or invalid password / username\n")
            login_new = str(input("Would you like to renew your login information? (Y/n): ")).lower()
            if login_new == 'y':
                init.main()
                os._exit(0)
            else:
                os._exit(0)
        except FileNotFoundError:
            init.main()

    def moduleLoader(self):
        paths = []
        broken_dir = []
        broken_module = []
        for directory in os.listdir(os.getcwd()):
            if "+" in directory:
                paths.append(directory)
        print("---------------------------------")
        print("Successful loaded folders: ")
        for current_path in paths:
            try:
                directory = iter_modules(
                    path=[current_path])
                if os.path.isdir(current_path):
                    print("'{path}'".format(path=current_path))
                    for module_loader, name, ispkg in directory:
                        loader = module_loader.find_module(name)
                        module = loader.load_module(name)
                        if hasattr(module, "exc") and hasattr(module, "commands"):
                            self.modules.append(module)
                else:
                    broken_dir.append(current_path)
            except SyntaxError:
                broken_module.append(name)
        print("---------------------------------")
        print("\n---------------------------------")
        print("Successful loaded modules:")
        for module in self.modules:
            print(module)
        print("---------------------------------\n")
        if broken_dir or broken_module:
            self.helpByError(broken_dir, broken_module)

    @staticmethod
    def helpByError(broken_dir, broken_module):
        print("---------------------------------")
        print("~An ERROR occurred !~\n")
        if broken_dir:
            print("\n{0} is not a folder!\n".format(broken_dir))
        if broken_module:
            print("Check your modules for the following keywords:\n"
                  "A function called 'exc()'\n"
                  "A list called 'commands[]'\n")
            print("Faulty modules:")
            for module in broken_module:
                print("'{0}'".format(module))
            print("---------------------------------\n")

    def getCommand(self):
        self.email.list()
        self.email.select("Notes", True)

        typ, data = self.email.search(None, "ALL")
        try:
            latest_id = data[0].split()[-1]
        except IndexError:
            return

        if latest_id == self.check_latest:
            return

        self.check_latest = latest_id
        typ, data = self.email.fetch(latest_id, "(RFC822)")
        siri_command = message_from_string(data[0][1].decode('utf-8'))
        return str(siri_command.get_payload()).lower().strip()

    def control(self):
        print("Fetching commands...")
        while True:
            try:
                cmd = self.getCommand()
                command_list_length = -1
                given_length = 0
                if not cmd:
                    raise PlaceholderException()
                elif cmd == "exit":
                    print("Exit program")
                    raise KeyboardInterrupt
                cmd_list = cmd.split()
                for module in self.modules:
                    command_list_length = module.commands.__len__()
                    for word in module.commands:
                        if word in cmd_list:
                            given_length += 1
                        if command_list_length == given_length:
                            print("\n-> Start : '{0}'\n".format(module))
                            thread = ControlThread(cmd, module)
                            thread.start()
                    given_length = 0
            except PlaceholderException:
                pass
            except imaplib.IMAP4.error:
                os._exit(1)
            except Exception as exc:
                print("Runtime error: {exc}".format(**locals()))
                print("Restart...")
            sleep(1)


if __name__ == '__main__':
    try:
        Main(dateiname)
    except KeyboardInterrupt:
        print("\nExit -RaspPi-Siri-Vernsteuerung-\n")
        sleep(1)
        os.system("clear")  # on linux 'clear'
        os._exit(1)
