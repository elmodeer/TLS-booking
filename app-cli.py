#!/usr/bin/env python
import argparse
import signal

import atexit
from time import sleep

import validators
from tlsBook import TlsChecker

checker: TlsChecker


def main():
    global checker
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='Please enter the email you used to create your TLS application.')
    parser.add_argument('password',
                        help='Please enter the password you used to create your TLS application (We will not record your password). if '
                             'your password contains special characters, put it in quotations marks')
    parser.add_argument('target_emails',
                        help='Please enter a list of email recipients when there is an appointment separated by a comma character')
    args = parser.parse_args()

    emails = validators.concat_emails(args.email, args.target_emails)
    if not args.target_emails or not validators.is_valid(emails):
        print('Please provide valid email addresses')
        exit(1)

    if not validators.validate_required(args.password):
        print('Password is required')
        exit(1)

    checker = TlsChecker(args.email, args.password, emails)

    appointment_found = False
    minutes = 2
    print('Starting TLS checking')

    while not appointment_found:
        loggedIn = checker.login()
        if loggedIn:
            appointment_found = checker.check(loggedIn)
            print('------------- Will try again in ' + str(minutes) + ' minutes ----------------------------')
            sleep(60 * minutes)  # 5 minutes

        else:
            print("Something does not seem right with your credentials, Try again please")
            break


def handle_exit():
    global checker
    if checker:
        checker.terminate()


# Failsafe mechanism in case of program crashing
atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == '__main__':
    main()
