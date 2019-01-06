#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pkgutil
#import platform


commands = ["start", "python"]

def exc(command):
    try:
        command_list = command.lower().split()
        if command_list.__len__() == 3:
            py_skript = "python3 "
            path = os.path.join(os.path.dirname(__file__), "Python skripte")
            directory = pkgutil.iter_modules(path=[path])
            for finder, name, ispkg in directory:
                if name.lower() == command_list[-1]:
                    print("Executed the script:", name)
                    os.chdir(path)
                    py_skript = py_skript+name+".py"
                    os.system(py_skript)
                else: raise FileNotFoundError
        else:
            if command == "how do i start python scripts":
                print("-Python-Starter Help-\n"
                      "To start a python script from your iPhone you need to\n"
                      "add the script to the folder '/Siri/ProgrammStarter+/Python skripte/'.\n"
                      "The script can be executed by saying:\n"
                      "'python start [name of the script]'")
    except FileNotFoundError:
        print("File not found\nTry to say: 'how do i start python scripts' for help")
