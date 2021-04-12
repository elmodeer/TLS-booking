import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_valid(emails):
    valid = True
    for checkEmail in emails:
        if not EMAIL_REGEX.match(checkEmail):
            valid = False
            break
    return valid


def validate_required(string):
    if string == '':
        return False
    return True


def concat_emails(email, emails):
    # Replace commas and semi-columns by spaces then split the emails
    emails = emails.replace(',', ' ').replace(';', ' ').split(' ')
    emails.append(email)
    return emails
