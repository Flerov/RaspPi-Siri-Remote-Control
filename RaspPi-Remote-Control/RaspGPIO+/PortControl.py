#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

commands = ["port"]
available_ports = [4, 5, 6, 13, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27]


def exc(command):
    command_list = command.lower().split()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    if "activate" in command_list:
        port = check(command_list, "activating")
        GPIO.output(port, GPIO.HIGH)
    elif "deactivate" in command_list:
        port = check(command_list, "deactivating")
        GPIO.output(port, GPIO.LOW)
    if not port:
        print("no valid port")


def check(cmd, status):
    for i in cmd:
        try:
            if int(i) in available_ports:
                print("{0} port: {1}".format(status, i))
                GPIO.setup(int(i), GPIO.OUT)
                return int(i)
        except ValueError:
            pass

#if __name__ == '__main__':
#    exc("deactivate port 17")
