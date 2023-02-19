#!/usr/bin/env python3

print("Starting the script...")

import requests
import sys
import json

def get_status_page(username):
    url = "http://telehack.com/u/" + username + ".json"
    r = requests.get(url)
    if r.status_code != 200:
        return ([username], r.status_code)
    page_data = json.loads(r.text)
    badges = [badge for badge, obtained in page_data.items() if obtained is True]
    print(f"URL: {url}")
    print(f"Response text: {r.text}")
    return (badges, 0)


def main(args):
    user1 = args[1].upper()
    user2 = args[2].upper()

    print(f"User1: {user1}")
    print(f"User2: {user2}")

    user1_badges, err = get_status_page(user1)
    print (user1_badges)
    if err == 404:
        print(f"{err}: user {user1} not found.")
        sys.exit(err)
    elif err:
        print(f"{user1}: {err}")
        sys.exit(err)

    user2_badges, err = get_status_page(user2)
    if err == 404:
        print(f"{err}: user {user2} not found.")
        sys.exit(err)
    elif err:
        print(f"{user2}: {err}")
        sys.exit(err)

    # badge count for each user
    hdr_message = f"{user1} ({len(user1_badges)}) vs {user2} ({len(user2_badges)})"
    print("\n" + hdr_message)
    print("-" * len(hdr_message))

    print(f"{user1} badges: {user1_badges}")
    print(f"{user2} badges: {user2_badges}")

    # badges users have in common
    common_badges = list(set(user1_badges) & set(user2_badges))
    print(f"\n[+] Both users have this {len(common_badges)} badges:\n")
    print(", ".join(sorted(common_badges)))

    # badges only user2 have
    badges1 = sorted(list(set(user2_badges) - set(user1_badges)))
    print(f"\n[+] {user1} is missing this {len(badges1)} badges that {user2} already have:\n")

    if badges1:
        print(", ".join(badges1))
    else:
        print("None.")

    # badges only user1 have
    badges2 = sorted(list(set(user1_badges) - set(user2_badges)))
    print(f"\n[+] {user2} is missing this {len(badges2)} badges that {user1} already have:\n")

    if badges2:
        print(", ".join(badges2))
    else:
        print("None.")

    print ("")
    print("Script has finished.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"  Usage: {sys.argv[0]} <user1> <user2>\n")
        sys.exit(1)
    main(sys.argv)
