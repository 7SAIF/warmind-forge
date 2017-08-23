# coding=utf-8
import random
import json
import sqlite3
import zipfile
from time import sleep
from .Global_Variables import *

class AIFunctions(object):
    """
    Class to access Warmind's AI
    """
    def __init__(self):
        pass

    def get_activity(self, activity_name):
        """
        Returns an Activity from the Advisor Table to the AI
        :param activity_name: Name of the activity
        :type activity_name: String
        :return: activity, data, modifier
        :rtype: list
        """
        conn = sqlite3.connect(sqlite_warmind)
        c = conn.cursor()
        c.execute('SELECT activity, data, modifier FROM advisor WHERE activity IS ?', (activity_name,))
        out = c.fetchone()
        conn.close()
        return out

    def random_jugs(self, current_jugs):
        jugs_list = ['( o )( o )', '(o   )(   o)', '( @ )( @ )', '( . )( . )( . )', '(. Y .)', '[ # ] [ # ]', '(.) (.)',
                     '( # )( # ) ', '(< )  ( >)', '( $ )( $ )', '( 9. )( 9. )', '[ @ ][ @ ]', '( o Y o )', '( % )( % )',
                     '( + )( + )', '( | )( | )', '( 0.)( K.)', '( * )( * )', '( ? )( ? )', '( ! )( ! )', '( ^ )( ^ )',
                     '( ~ )( ~ )', '( : )( : )', '( Dr )( PC )', '( - )( - )', '( (^) )( (^) )', '( i )( i )',
                     '( ! )( ! )', '(  ÷  )(  ÷  )',
                     '(101100)(101100)', '( X )( X )', '( % )( % )', '( o )( o )', '( \' )( \' )', '( , )( , )',
                     '( 0 )( 0 )', '(\*)(\*)(\*)(\*)', '(  \`  )(  \`  )', '(  \*)(\*  )', '(  ☆  )(  ☆  )',
                     '(  BE  )(  ER  )', '( ❄️ )( ❄ ️)', '(  !!!  )(  !!!  )']
        rng_jugs = (random.choice(jugs_list))
        while current_jugs == rng_jugs:
            rng_jugs = (random.choice(jugs_list))
            print("REROLL JUGS: " + rng_jugs)
        return rng_jugs

    def crater(self, live_manifest_version):
        pass
