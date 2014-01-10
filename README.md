# Update Endpoints

It can be a pain to update endpoints in keystone by hand, so this script
should automate the ability to update the endpoints. 

## Warnings

This script has not been well tested. You are strongly advised to backup 
the relevant database entries for the keystone endpoints or at least dump them
to a file so you can manually restore if needed.

You assume all liability for running this script against your openstack
instance.

## Usage

Copy the script to your control node. Then run as follows:

`update-endpoints.py [-h] --username USERNAME --password PASSWORD --host HOST --endpoint ENDPOINT --type (public, internal, or admin)`

For example, to update the hostname in all the public endpoints to point at foo.com, run the following:

`./update-endpoints.py --username root --password blargh --host localhost --endpoint foo.com --type public`

## Validation

After running the script, validate the changes with

`keystone endpoint-list`
