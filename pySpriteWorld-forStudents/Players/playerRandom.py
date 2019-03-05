#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:33:23 2019

@author: 3415762
"""
import random

me = ""

def setMe(name):
    global me
    me = name

def joueCoup(jeu):
    """
    Jeu -> (int, int)
    """
    (row, col) = jeu.getPlayerPos(name)
    return (row + random.randint(-1,1), col + random.randint(-1,1))