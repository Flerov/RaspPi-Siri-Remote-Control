#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import Main
import xml.etree.ElementTree as ElementTree # implementiert eine einfache und effiziente API zum Parsen und Erstellen von XML-Daten
from os import _exit # Schnittstelle zu Betriebssystem und Laufzeitumgebung

seperator = "---------------"


def createXML(em, pwd):
    logging = ElementTree.Element("logging")
    email = ElementTree.SubElement(logging, "email", {"typ": "str"})
    passwort = ElementTree.SubElement(logging, "passwort", {"typ": "str"})
    email.text = em
    passwort.text = pwd
    et = ElementTree.ElementTree(logging)
    et.write("User-Daten.xml")


def getLogs():
    print("Your @gmail address from which your voice input will be retrieved:")
    email = str(input("E-Mail: "))
    if not "@gmail" in email:
        print("Invalid e-mail address"); raise Exception
    else:
        # email = hashlib.sha512(bytes(email))
        print("Your @gmail password:")
        passwort = str(input("Password: "))
        # passwort = hashlib.sha512(bytes(input("Passwort: ")))
        if len(passwort) <= 7:
            print("Invalid password")
            raise Exception
        else:
            print(seperator, "\n\n")
            return email, passwort


def run():
    try:
        email, passwort = getLogs()
        createXML(email, passwort)
    except Exception:
        run()


def main():
    try:
        print(seperator)
        print("Easy-Configurator")
        print(seperator, "\n")
        print("\n", seperator, "\nTo get you started as easily as possible, the necessary files\n"
              "will be automatically created and configured so everything can work smoothly.\n"
              "Therefore your gmail credentials are needed.\n", seperator, "\n")
        run()
        print("Configuration completed\n")
    except KeyboardInterrupt:
        _exit(0)
