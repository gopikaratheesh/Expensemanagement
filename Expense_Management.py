from HouseMates import HouseMates
from Member import Member, decrement_member_count

Error_MemberNotFound = "MEMBER_NOT_FOUND"
SuccessMsg = "SUCCESS"


class ExpenseManagement:

    # extract the command and process it
    # input      - contents from file: array of string
    # output     - nil
    # error      -  if invalid command, exit
    def __init__(self, contents):
        self.head = None
        valid_commands = ("MOVE_IN", "SPEND", "DUES", "CLEAR_DUE", "MOVE_OUT")
        for each_command in contents:
            command = each_command.strip("\n").split(" ", 1)
            # if invalid command, exit
            if len(command) < 2 or command[0] not in valid_commands:
                print("Error: Invalid Input:", command[0])
                exit(1)
            fn_name = command[0].lower()
            eval("self." + fn_name + "(\"" + command[1].strip() + "\")")

    # move_in  - add member to housemates list
    # input    - name of the new member: string
    # output   - msg to STDOUT
    # return   - if member exceed the limit
    #            if invalid name provided
    #            if member already exist in HouseMates list
    def move_in(self, name):
        # if houseful, do not add new members
        if Member.memberCount >= Member.MaxMember:
            print("HOUSEFUL")
            return
        # if multiple inputs, return
        if len(name.split()) > 1:
            print("Invalid Member Name")
            return
        # if duplicate member, do not add same member again
        if Member.memberCount > 0 and HouseMates.search(self, name):
            print("Member %s already moved In. Please verify the name" % name)
            return
        # add new member
        response = HouseMates.append(self, name)
        print(response)
        return

    # spend    - process the expenses and add the owe amount to the members details
    # input    - <amount> <spent-by> <spent-for-member1> <spent-for-member2>  : string
    # output   - msg to STDOUT
    # return   - if invalid amount
    #            if spent-by name, also present in spent-for-member list
    #            if any member not found
    def spend(self, action):
        amount = int(action.strip().split(" ", 1)[0])
        spent_by = action.strip().split(" ", 2)[1]
        spent_for = action.strip().split(" ", 2)[2].split()
        # if invalid amount, return
        if amount <= 0:
            print("Invalid Amount")
            return
        # calculate per person amount
        per_person = round(amount / (len(spent_for) + 1))
        response = 0
        for name in spent_for:
            if spent_by == name:
                print("Invalid spent-for-member name")
                return
            # update Owe field for members
            response += HouseMates.update_owes(self, name, spent_by, per_person)
        # if all the members in spent-for-member are valid, print success msg, else return error msg
        if response == len(spent_for):
            print(SuccessMsg)
        else:
            print(Error_MemberNotFound)
        return

    # dues     - Balance the expenses and print the OWe amounts
    # input    - <member-who-owes>  : string
    # output   - msg to STDOUT
    # return   - if invalid member name
    #            if any member not found
    def dues(self, name):
        # if multiple members in input, return
        if len(name.split()) > 1:
            print("Invalid Member Name")
            return
        # if member not found
        if Member.memberCount == 0 or not HouseMates.search(self, name):
            print(Error_MemberNotFound)
            return
        # balance the expenses
        HouseMates.balance_expenses(self)
        # print the due amounts
        print(HouseMates.print_dues(self, name), end="")

    # clear_due - update the Owe field with amount that is paid back
    # input     - <member-who-owes> <member-who-lent> <amount>  : string
    # output    - msg to STDOUT
    # return    - if invalid input
    #             if invalid amount
    def clear_due(self, action):
        spl = action.strip().split()
        if len(spl) != 3:
            print("Invalid CLEAR_DUE input")
            return
        name = spl[0]
        pay_to = spl[1]
        amount = int(spl[2])
        if amount <= 0:
            print("Invalid Amount")
            return
        if name == pay_to:
            print("Invalid pay_to name. member-who-owes and member-who-lent cannot be same")
            return
        # balance the expenses
        HouseMates.balance_expenses(self)
        print(HouseMates.settle_dues(self, name, pay_to, amount))
        return

    # move_out  - check if member eligible to move out and remove from HouseMate list
    # remove from ActiveList and decerment member count on removing from HouseMate list
    # input     - <name-of-existing-member>  : string
    # output    - msg to STDOUT
    # return    - if invalid member name
    def move_out(self, name):
        if len(name.split()) > 1:
            print("Invalid Member Name")
            return
        # add new member
        # balance the expenses
        HouseMates.balance_expenses(self)
        response = HouseMates.remove(self, name)
        if response == SuccessMsg:
            Member.ActiveList.pop(name)
            decrement_member_count()
        print(response)
        return
