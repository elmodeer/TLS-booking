#!/usr/bin/env python
import argparse

from time import sleep

import validators
from tlsBook import TlsChecker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='Please enter the email you used to create your TLS application.')
    parser.add_argument('password',
                        help='Please enter the password you used to create your TLS application (We will not record your password).')
    parser.add_argument('target_emails',
                        help='Please enter a list of email recipients when there is an appointment separated by a comma character')
    args = parser.parse_args()

    emails = validators.concat_emails(args.email, args.target_emails)
    if not args.target_emails or not validators.validate_emails(emails):
        print('Please provide valid email addresses')
        exit(1)

    if not validators.validate_required(args.password):
        print('Password is required')
        exit(1)

    checker = TlsChecker(args.email, args.password, emails)
    while True:
        checker.check()
        print('Starting TLS checking')
        sleep(60 * 5)  # 5 minutes


if __name__ == '__main__':
    main()
