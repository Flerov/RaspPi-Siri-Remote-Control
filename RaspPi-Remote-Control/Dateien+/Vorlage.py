#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os  # ermöglicht den Zugriff auf das Dateisystem

commands = ["directory"]  # dieses Skript wird dann ausgeführt, wenn das Wort 'directory' gesagt wurde


def exc(command):  # diese Funktion wird explizit aufgerufen. Ihr wird das gesagte als String übergeben
    list_command = command.strip()  # die einzelnen Wörter des Strings werden getrennt und in eine Liste gepackt
    if "current" in list_command:  # es wird abgefragt ob sich das Wort 'current' in der Liste befindet
        print(os.getcwd())  # der aktuelle Dateipfad wird in der Konsole ausgeben
