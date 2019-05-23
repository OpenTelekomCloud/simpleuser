#!/usr/bin/python

import sys
import json
import getopt
import openstack

def usage(retval):
    print("%s [-h|--help] [-r|--read] [-w|--write file.json", argv[0])
    sys.exit(retval)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hrw:", ["--help", "--read", "--write="])
    except getopt.GetoptError:
        usage(1)
        
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)

        elif opt in ("-r", "--read"):
            existing_users = read_users() # von welcher domain?? --> von der aus OS_CLOUD
            print(json.dumps(existing_users))
            sys.exit(0)
            
        elif opt in ("-w", "--write"):
            # wenn ich kein Argument zu -w angebe, dann soll eine feste Datei gelesen werden.
            with open(arg, "r") as f:
                userconfig = json.load(f)
            sys.exit(write_userconfig(userconfig))

def read_users():
    # aufbau der struktur aus der OTC heraus
    # returnen der struktur
        
def write_users(userconfig):
    # check if userconfig.domain entspricht OS_CLOUD
    # wenn nicht, auf den mismatch hinweisen (warn)!
    
    # testen, ob wir überhaupt auf die eigentliche domain zugreifen dürfen (via credentials in clouds.yaml/secure.yaml)
    
            for project in users.projects:
                # check if project exists
                # if yes, warn, but continue
                # if no,
                #   create project
                #   iterate over users
                for user in project.users:
                    # check if user exists in domain
                    # if yes:
                    #   warn
                    #   check if the existing user is member in the current project
                    #   if no: warn "User {user} is assigned to project {otherproject}, but this config plans to assign him to {thisproject}.
                    #                This script requires to have users only assigned to a single project. Please adjust either the existing
                    #                user or this {userconfigfile}. This user {user} has not been changed."
                    # create user
                    #   - verify that all four attributes are present:
                    #   - set user.username, user.fullname, user.email, and user.phone
                    #   - configure MFA for the phone
                    
                    
if __name__ == "__main__":
    main()
