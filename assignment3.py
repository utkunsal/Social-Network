import sys
network = {}
with open(sys.argv[1]) as names:
    for line in names:
        name, friends = line.strip().split(":")
        network[name] = friends.split(" ")

output = open("output.txt", "w")
output.write("Welcome to Assignment 3\n-------------------------------\n")

def add_user(new_user):
    global network
    if new_user in network.keys():
        output.write("ERROR: Wrong input type! for 'ANU'! -- This user already exists!!\n")
    else:
        network[new_user] = []
        output.write(f"User '{new_user}' has been added to the social network successfully\n")

def del_user(username):
    global network
    if username not in network.keys():
        output.write(f"ERROR: Wrong input type! for 'DEU'!--There is no user named '{username}'!!\n")
    else:
        network.pop(username)
        for list in network.values():
            for name in list:
                if name == username:
                    list.remove(username)
        output.write(f"User '{username}' and his/her all relations have been deleted successfully\n")

def find_users(cmd, a, b="noone"):
    """ If usernames are not in the network, the function gives an error message.
        First parameter is the command name. The function specifies the command name in the error message.
        Second and third parameters are usernames. Third argument is optional. """
    # When function is called without b, it sets the value of b to an existing name in the network.
    if b == "noone":
        b = sorted(network)[0]
    if a not in network and b not in network:
        output.write(f"ERROR: Wrong input type! for '{cmd}'! -- No user named '{a}' and '{b}' found!\n")
    elif a not in network:
        output.write(f"ERROR: Wrong input type! for '{cmd}'! -- No user named '{a}' found!!\n")
    elif b not in network:
        output.write(f"ERROR: Wrong input type! for '{cmd}'! -- No user named '{b}' found!!\n")
    else:
        return True

def add_friend(source_user, target_user):
    global network
    if find_users("ANF", source_user, target_user):
        if target_user in network[source_user]:
            output.write(f"ERROR: A relation between '{source_user}' and '{target_user}' already exists!!\n")
        else:
            network[source_user].append(target_user)
            network[target_user].append(source_user)
            output.write(f"Relation between '{source_user}' and '{target_user}' has been added successfully\n")

def del_friend(source_user, target_user):
    global network
    if find_users("DEF", source_user, target_user):
        if target_user in network[source_user]:
            network[source_user].remove(target_user)
            network[target_user].remove(source_user)
            output.write(f"Relation between '{source_user}' and '{target_user}' has been deleted successfully\n")
        else:
            output.write(f"ERROR: No relation between '{source_user}' and '{target_user}' found!!\n")

def count_friend(username):
    if find_users("CF", username):
        output.write(f"User '{username}' has {len(network[username])} friends\n")

def find_possible_friends(username, maximum_distance):
    """ Finds the number of possible friends and their names for the given username in the range of maximum distance.
        Maximum distance must be an integer. """
    if find_users("FPF", username):
        if maximum_distance < 1 or maximum_distance > 3:
            output.write(f"ERROR: Maximum distance must be between 1 and 3\n")
        else:
            pf_list = network[username][:]
            if maximum_distance >= 2:
                for name1 in network[username]:
                    pf_list.extend(network[name1])
                if maximum_distance == 3:
                    for name2 in set(pf_list):
                        pf_list.extend(network[name2])
            pf_list = sorted(set(pf_list))
            if username in pf_list:
                pf_list.remove(username)
            output.write(f"User '{username}' has {len(pf_list)} possible friends when maximum distance is {maximum_distance}\n")
            if len(pf_list) != 0:
                pf_string = "{'" + "' ,'".join(pf_list) + "'}"
                output.write(f'''These possible friends: {pf_string}\n''')

def suggest_friend(username, MD):
    """ Finds users that have mutual friends with the given username according to the mutuality degree,
        and suggests friends based on the number of mutual friends.
        MD (Mutuality degree) must be an integer. """
    if find_users("SF", username):
        if MD <= 1 or MD >= 4:
            output.write("ERROR: Mutuality Degree cannot be less than 1 or greater than 4\n")
        elif len(network[username]) < MD:
            output.write("ERROR: User has less friends than mutuality degree\n")
        else:
            friends, suggested = [], []
            for name in network[username]:
                friends.extend(network[name])
            if MD == 2:
                for name in sorted(set(friends)):
                    if friends.count(name) == 2 and name != username:
                        suggested.append(name)
            for name in sorted(set(friends)):
                if friends.count(name) == 3 and name != username:
                    suggested.append(name)
            output.write(f"Suggestion List for '{username}' (when MD is {MD}):\n")
            sug_str = ""
            for name in suggested:
                if name in network[username]:
                    suggested.remove(name)
            for name in suggested:
                output.write(f"'{username}' has {friends.count(name)} mutual friends with '{name}'\n")
            for name in sorted(suggested):
                sug_str += "'" + name + "', "
            output.write(f"The suggested friends for '{username}': {sug_str[:-2]}\n")

with open(sys.argv[2]) as cmds:
    lists = [line.split() for line in cmds]
for list in lists:
    if list[0] == "ANU":
        add_user(list[1])
    elif list[0] == "DEU":
        del_user(list[1])
    elif list[0] == "ANF":
        add_friend(list[1], list[2])
    elif list[0] == "DEF":
        del_friend(list[1], list[2])
    elif list[0] == "CF":
        count_friend(list[1])
    elif list[0] == "FPF":
        find_possible_friends(list[1], int(list[2]))
    elif list[0] == "SF":
        suggest_friend(list[1], int(list[2]))

output.close()
