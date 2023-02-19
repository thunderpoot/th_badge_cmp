#!/usr/bin/env python3

'''Compare badges of two Telehack users'''

from datetime import datetime
import time
import sys
import json
import pydoc
import requests


def get_badges(username):
    '''Get user badges, returns a dictionary and response status'''
    url = "http://telehack.com/u/" + username + ".json"
    response = requests.get(url)
    if response.status_code != 200:
        return ({}, response.status_code)
    page_data = json.loads(response.text)
    badges = page_data.get('badges')
    return (badges, 0)


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
        out = f"[+] {user_a} is missing {badges} that {user_b} has:\n  "
        out += ",\n  ".join(missing_badges)
    return out


def delta_time(delta):
    '''Calculate time differential, returns a formatted string'''
    if ( delta + 0.5 ) < 60:
        return f"{int(delta+0.5)} seconds"
    if ( delta/60+0.5) < 60:
        return f"{int(delta/60+0.5)} minutes"
    if ( delta/3600+0.5) < 24:
        return f"{int(delta/3600+0.5)} hours"
    if ( delta/86400+0.5) < 365:
        return f"{int(delta/86400+0.5)} days"
    return f"{int(delta/31536000)} years"


def user_delta(username,badges):
    '''Return formatted string of when user created account'''
    user_epoch = badges.get( 'ACCT' )
    user_since = datetime.utcfromtimestamp(user_epoch).strftime('%Y-%m-%d %H:%M:%S')
    now = time.time()
    user_deltatime = delta_time(now-user_epoch)
    return f"{username: <9} (user since {user_since}, {user_deltatime})\n"


def main(args):
    '''Main function, takes command-line arguments, invokes pager to display output'''
    out = ''

    user1 = args[1].upper()
    user2 = args[2].upper()

    if user1 == user2:
        print(f"Error: cannot compare {args[1]} with {args[2]}.")
        sys.exit(1)

    user1_badges, err = get_badges(user1)
    if err == 404:
        print(f"{err}: user {user1} not found.")
        sys.exit(err)
    elif err:
        print(f"{user1}: {err}")
        sys.exit(err)

    user2_badges, err = get_badges(user2)
    if err == 404:
        print(f"{err}: user {user2} not found.")
        sys.exit(err)
    elif err:
        print(f"{user2}: {err}")
        sys.exit(err)

    # Badge count for each user
    len1 = len(user1_badges)
    len2 = len(user2_badges)

    hdr_message = f"{user1} ({len1}) vs {user2} ({len2})"
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
    out += f"\n[+] Both users have {thisthese} {count} badge{'s'*(count>1)}:\n  "
    out += ",\n  ".join(sorted(common_badges)) + "\n\n"

    diff1 = get_difference(user1, user2, user1_badges, user2_badges)
    diff2 = get_difference(user2, user1, user2_badges, user1_badges)

    if diff1 != '' and diff2 != '':
        out += f"{diff1}\n\n{diff2}\n"
    else:
        out += f"{user1} and {user2} have the same badges\n"

    out += "\nEnd of report"
    pydoc.pager(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"  Usage: {sys.argv[0]} <user1> <user2>\n")
        sys.exit(1)

    main(sys.argv)
