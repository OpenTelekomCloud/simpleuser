import sys
import json
import openstack

def main():
    # parse args, check whether there is either a "-r" or a "-w" option present

    if mode == "reading":
        existing_users = read_users() # von welcher domain?? --> von der aus OS_CLOUD
        print(json.dumps(existing_users))
        
    if mode == "writing":
        if len(sys.argv) > 1:
            userconfigfile = sys.argv[1]
        else:
            userconfigfile = "./users.json"
        
        with open(userconfigfile, "r") as f:
            userconfig = json.load(f)
        write_userconfig(userconfig)

def read_users():
    # aufbau der struktur
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
    
