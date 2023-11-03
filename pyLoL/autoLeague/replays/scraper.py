"""Scrapes observations from a replay file by replaying a match using
the League game client and storing the observations in a json file."""

import os
import time
import json
import subprocess
import base64
import requests
import pyautogui
import pydirectinput

