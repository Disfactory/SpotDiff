"""Generate a 256-bit private key."""

import sys
import secrets


argv = sys.argv
error_msg = "Must confirm by running: python gen_key.py [KEY_FILE_PATH] confirm"

if len(argv) > 2:
    if argv[2] == "confirm":
        try:
            with open(argv[1], "w") as f:
                print("A new key is generated at %s" % argv[1])
                print(secrets.token_urlsafe(32), file=f)
        except Exception as e:
            print(e)
    else:
        print(error_msg)
else:
    print(error_msg)
