from random import randrange, choice
from datetime import timedelta
import re


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def pick_random_word(match):
    words = match.group(1)
    return choice(words.split("|"))


def write_comment(comment):
    r = re.compile('{([^{}]*)}')
    while True:
        comment, n = r.subn(pick_random_word, comment)
        if n == 0:
            break
    return comment



# USAGE: self.write_comment("{{so|totally} ugly|very {nice|bad}} {photo|media|upload} {:)||:D|<3}")
