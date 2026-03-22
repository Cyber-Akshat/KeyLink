# Password-Manager
a password manager np

# Roles
## Akshat
### Encryption
- create an encryption system that encrypts/decrypts data based on the key provided
- key needs to have minimum 15 characters
- must have uppercase and special characters

## Yahyah
### UI Design
- Before anything tell us how you want the UI
- GUI or CLI

## George
### Utility
- sorting the accounts by name/website
  - for context loading the passwords loads an array from json, every obj is a dictionary that holds name, password, website
  - loop through array, get website var of each dictionary, strip the search input, (remove "https://" if found)
  - return an array that holds every dict that has the stripped search input in the website option
- password generator

## Klay
### Json Files
- saving/loading accounts to and from json
- save website/domain, username/email, password
