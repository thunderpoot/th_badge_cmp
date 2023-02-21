#!/usr/bin/env python3

'''Compare badges of two Telehack users'''

from datetime import datetime
import time
import sys
import json
import pydoc
import requests


CYAN = "\033[36m"
RED = "\033[31m"
RESET = "\033[m"


def get_badges(username):
    '''Get user badges, returns a dictionary and response status'''
    url = "http://telehack.com/u/" + username + ".json"
    response = requests.get(url)
    if response.status_code != 200:
        err = response.status_code
        if err == 404:
            print(f"{err}: user {username} not found.")
            sys.exit(1)
        elif err:
            print(f"{username}: {err}")
            sys.exit(1)

    page_data = json.loads(response.text)
    return page_data.get('badges')


def get_difference(user_a, user_b, set_b, set_a):
    '''Get difference between user_a and user_b, returns a formatted string'''
    missing_badges = sorted(list(set(set_a) - set(set_b)))
    out = ''
    thisthese = 'this'
    count = len(missing_badges)
    if count > 1:
        thisthese = 'these'
    if missing_badges:
        badges = f"{thisthese} {count} badge{'s'*(count>1)}"
        out = f"[+] {user_a} is missing {badges} that {user_b} has:\n{RED}"
        out += " ".join(missing_badges)
        out += f"{RESET}"
    return out


def delta_time(delta):
    '''Calculate time differential, returns a formatted string'''
    seconds = delta+0.5
    minutes = delta/60+0.5
    hours   = delta/3600+0.5
    days    = delta/86400+0.5
    years   = delta/31536000

    if seconds < 60:
        return f"{int(seconds)} seconds"
    if minutes < 60:
        return f"{int(minutes)} minutes"
    if hours < 24:
        return f"{int(hours)} hours"
    if days < 365:
        return f"{int(days)} days"

    return f"{int(years)} years"


def user_delta(username,badges):
    '''Return formatted string of when user created account'''
    user_epoch = badges.get( 'ACCT' )
    user_since = datetime.utcfromtimestamp(user_epoch).strftime('%Y-%m-%d %H:%M:%S')
    now = time.time()
    user_deltatime = delta_time(now-user_epoch)
    return f"{username: <9} (user since {user_since}, {user_deltatime})\n"


def main(args):
    '''Main function, takes command-line arguments, invokes pager to display output'''
    user1 = args[1].upper()
    user2 = args[2].upper()

    if user1 == user2:
        print(f"Error: cannot compare {args[1]} with {args[2]}.")
        sys.exit(1)

    user1_badges = get_badges(user1)
    user2_badges = get_badges(user2)

    # Badge count for each user
    len1 = len(user1_badges)
    len2 = len(user2_badges)

    hdr_message = f"{user1} ({len1}) vs {user2} ({len2})"

    out = ''
    out += f"{hdr_message}\n"
    out += ( "=" * len(hdr_message) ) + "\n\n"
    out += user_delta(user1,user1_badges)
    out += user_delta(user2,user2_badges)

    # Badges users have in common
    common_badges = list(set(user1_badges) & set(user2_badges))
    thisthese = 'this'
    count = len(common_badges)
    if count > 1:
        thisthese = 'these'
    out += f"\n[+] Both users have {thisthese} {count} badge{'s'*(count>1)}:\n{CYAN}"
    out += " ".join(sorted(common_badges)) + "\n\n"
    out += f"{RESET}"

    diff1 = get_difference(user1, user2, user1_badges, user2_badges)
    diff2 = get_difference(user2, user1, user2_badges, user1_badges)

    if diff1 != '' and diff2 != '':
        out += f"{diff1}\n\n{diff2}\n"
    else:
        out += f"{user1} and {user2} have the same badges\n"

    out += "\nEnd of report"
    pydoc.pipepager(out, cmd='less -R')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"  Usage: {sys.argv[0]} <user1> <user2>\n")
        sys.exit(1)

    main(sys.argv)
