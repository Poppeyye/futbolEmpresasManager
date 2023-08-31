import os
import re

def get_emails_list():
    emails = []
    with open(os.getenv('emails_file'), 'r') as f:
        for line in f:
            line = line.strip()
            if re.match(r"[^@]+@[^@]+\.[^@]+", line):
                email = {"email": line}
                emails.append(email)
    return emails