#!/usr/bin/env python
import argparse

from time import sleep

import validators
from tlsBook import TlsChecker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='Please enter the email you used to create your TLS application.')
    parser.add_argument('password',
                        help='Please enter the password you used to create your TLS application (We will not record your password). if your password contains special characters, put it in quotations marks')
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
    
    appointmentFound = False
    mins = 5

    while not appointmentFound:
        print('Starting TLS checking')
        if checker.login(): 
            appointmentFound = checker.check()
            print('------------- Will try again in ' + str(mins) + ' minutes ----------------------------')
            sleep(60 * mins)  # minutes

        else: 
            print("Someting does not seem right with your credentials, Try agin please")
            break


if __name__ == '__main__':
    main()
