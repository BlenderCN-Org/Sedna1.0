#!BPY
# -*- coding: UTF-8 -*-
#
#
# 2018.05.20 Natukikazemizo

#﻿import bpy

# emotions
emotions =  (
    ("expectation", "Expectation", ""),      # (識別子, UI表示名, 説明文)
    ("joy", "Joy", ""),
    ("acceptance", "Acceptance", ""),
    ("fear", "Fear", ""),
    ("surprise", "Surprise", ""),
    ("sorrow", "Sorrow", ""),
    ("disgust", "Disgust", ""),
    ("anger", "Anger", ""))

# characters
characters =  (
    ("dorothy", "Dorothy", "Dorothy"),      # (識別子, UI表示名, 説明文)
    ("loris", "Loris", "Loris"),
    ("maid_fox", "Maid Fox", "Maid Fox"),
    ("robot", "Robot", "Robot like motion"),
    ("real", "Real", "Real motion"),
    ("cartoon", "Cartoon", "Cartoon like motion"))

# twist dictionary
char_action = {
    "dorothy"   :"Dorothy.twist",
    "loris"     :"Loris.twist",
    "maid_fox"  :"MaidFox.twist",
    "robot"     :"Robot.twist",
    "real"      :"Real.twist",
    "cartoon"   :"Cartoon.twist"
}
