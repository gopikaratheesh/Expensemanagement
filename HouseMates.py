import operator
from Member import Member

Error_MemberNotFound = "MEMBER_NOT_FOUND"
SuccessMsg = "SUCCESS"
FailureMsg = "FAILURE"
Err_incorrectPayment = "INCORRECT_PAYMENT"


# format_dict - sort dict to expected string format
# input       - new_dict:dictionary
# output      - sorted string of <name> <due amount> format
def format_dict(new_dict):
    resp = ""
    sorted_d = {k: new_dict[k] for k in sorted(new_dict)}
    final_sorted_dict = dict(sorted(sorted_d.items(), key=operator.itemgetter(1), reverse=True))
    for k in final_sorted_dict:
        resp += "{} {}\n".format(k, final_sorted_dict[k])
    return resp


# A linked List representation of housemates
class HouseMates:

    # append  - add to the linked list
    # input   - member:string
    # return  - success msg
    def append(self, member):
        new_mem = Member(member)
        # initialise member and initial due amount
        Member.ActiveList[member] = 0
        resp = SuccessMsg
        # if it is the first element in the list
        if self.head is None:
            self.head = new_mem
            return resp
        current_node = self.head
        # add to the end of the linked list
        while current_node.next is not None:
            current_node = current_node.next
        current_node.next = new_mem
        return resp

    # search  - search for an element in the linked list
    # input   - search_string:string
    # return  - true, if element present, otherwise false
    #           error, if empty linkedList
    def search(self, search_string):
        current = self.head
        flag = False
        # Checks whether list is empty
        if self.head is None:
            print("Error: Empty list. No members found\n")
            exit(1)
        else:
            while True:
                # Compares element to be found with each node present in the list
                if search_string in current.Name:
                    flag = True
                current = current.next
                if current is None:
                    break
            return flag

    # print_list - print entire linked list and due amount (for debugging purpose)
    def print_list(self):
        current_node = self.head
        resp = ""
        while current_node:
            resp += "{} - {} - {}\n".format(current_node.Name, Member.ActiveList[current_node.Name], current_node.Owes)
            current_node = current_node.next
            if current_node is None:
                break
        return resp

    # print_dues  - search for an element and print the Owe amount
    # input   - name:string
    # return  - error if member count <2 or linked list empty
    #           string with name and due amount
    #           error if member not found
    def print_dues(self, name):
        current = self.head
        new_dict = {}
        if self.head is None:
            return "Error: Empty list. No members found\n"
        else:
            while True:
                # Compares element to be found with each node present in the list
                if name in current.Name:
                    for key in current.Owes:
                        if current.Owes[key] < 0:
                            value = 0
                        else:
                            value = current.Owes[key]
                        new_dict[key] = value
                    return format_dict(new_dict)
                current = current.next
                if current is None:
                    break
        return Error_MemberNotFound

    # initializeOweForMember - calculate all negative and positive owe amount separately
    # input                  - nil
    # return                 - tuple of pos_value, neg_value, pos_list, neg_list
    def initialize_owe_for_member(self):
        # to calculate all positive values
        pos_value = 0
        # to calculate all negative values
        neg_value = 0
        # list of members that Owe amount
        neg_list = []
        # list of members that need to get the amount back
        pos_list = []
        current = self.head
        # preProcessing- initialize all values and lists
        while True:
            if Member.ActiveList[current.Name] < 0:
                neg_list.append(current.Name)
                neg_value += Member.ActiveList[current.Name]
            elif Member.ActiveList[current.Name] > 0:
                pos_list.append(current.Name)
                pos_value += Member.ActiveList[current.Name]
            current = current.next
            if current is None:
                break
        return pos_value, neg_value, pos_list, neg_list

    # balance_expenses  - balance the expenses based on Owe field of each member and Amount_Owe in ActiveList
    # return  - true, if amount able to balance, otherwise false
    #         - error if member count <2 or linked list empty
    def balance_expenses(self):
        if self.head is None or Member.memberCount < 2:
            resp = "Error: Empty list. No members found\n"
            return resp
        # preProcessing- initialize all values and lists
        pos_value, neg_value, pos_list, neg_list = HouseMates.initialize_owe_for_member(self)
        # if Owe amount + expected amount tally, balance the amount among members
        if pos_value + neg_value == 0:
            current = self.head
            while True:
                key = ""
                value = 0
                for i in current.Owes:
                    # find the member that Owe the highest amount for each member in Housemate List
                    if current.Owes[i] > value:
                        key = i
                        value = current.Owes[i]
                    current.Owes[i] = 0
                # if one member owe to other members, update Owefield and AmountOwe of ActiveList
                if len(neg_list) < len(pos_list):
                    if key != "":
                        current.Owes[key] = Member.ActiveList[current.Name]
                    if Member.ActiveList[current.Name] < 0:
                        for i in Member.ActiveList.keys():
                            if i in current.Owes:
                                current.Owes[i] = - Member.ActiveList[i]
                # if other members owe to one member, update Owefield and AmountOwe of ActiveList
                else:
                    if Member.ActiveList[current.Name] > 0:
                        for i in Member.ActiveList.keys():
                            if i in current.Owes:
                                current.Owes[i] = -Member.ActiveList[i]
                                h = self.head
                                while h.next is not None:
                                    if h.Name == i:
                                        h.Owes[current.Name] = Member.ActiveList[i]
                                    h = h.next
                current = current.next
                if current is None:
                    break
            return True

    # update_owes - update owe value of one who spend the amount
    # and Owes field for each member and amountDue of each member in ActiveList
    # initialize all fields for valid members
    # input  - name:string, OweTo:string, amount:int
    # return - error if linkedList is empty, or members < 2
    #        - 1 if both spent_by and owe member fields are updated, else 0
    def update_owes(self, name, owe_to, amount):
        # update owe value of one who spend the amount
        current = self.head
        flag_name = False
        flag_owe = False
        # Checks whether list is empty
        if self.head is None or Member.memberCount < 2:
            return 0
        else:
            # Compares element to be found with each node present in the list
            while True:
                # Update fields of one who spent the amount
                if owe_to in current.Name and name in Member.ActiveList.keys():
                    flag_name = True
                    # if adding Owes value for first time, initialize
                    if name not in current.Owes:
                        current.Owes[name] = 0
                    current.Owes[name] += -amount
                    Member.ActiveList[current.Name] += -amount
                # Update fields of one who Owe the amount
                if name in current.Name and owe_to in Member.ActiveList.keys():
                    flag_owe = True
                    # if adding Owes value for first time, initialize
                    if owe_to not in current.Owes:
                        current.Owes[owe_to] = 0
                    current.Owes[owe_to] += amount
                    Member.ActiveList[current.Name] += amount
                # initialize Owe field for alll valid names
                if name not in current.Name and owe_to not in current.Name and name in Member.ActiveList.keys() and \
                        owe_to in Member.ActiveList.keys():
                    if owe_to not in current.Owes:
                        current.Owes[owe_to] = 0
                    if name not in current.Owes:
                        current.Owes[name] = 0
                current = current.next
                if current is None:
                    break
            # if both spent_by and owe member fields are updated, return 1
            if flag_owe and flag_name:
                return 1
            else:
                return 0

    # settle_dues - update owe value with settled amount
    # updates Owes field for each member and amountDue of each member in ActiveList
    # return the balance amount to be settled
    # input  - name:string, payto:string, amount:int
    # return - error if linkedList is empty, or members < 2
    #        - 1 if both spent_by and owe member fields are updated, else 0
    #        - balance amount to be paid
    def settle_dues(self, name, payto, amount):
        # update owe value of one who spend the amount and one who owe
        current = self.head
        resp = Error_MemberNotFound
        # Checks whether list is empty
        if self.head is None or Member.memberCount < 2:
            return Error_MemberNotFound
        else:
            # Compares element to be found with each node present in the list
            while True:
                # update Owe field of the one who paid back and update amount due field of ActiveList
                if name in current.Name and name in Member.ActiveList.keys() and payto in Member.ActiveList.keys():
                    # if they pay more, then an error message
                    if current.Owes[payto] < amount:
                        resp = Err_incorrectPayment
                        return resp
                    current.Owes[payto] -= amount
                    Member.ActiveList[current.Name] -= amount
                    Member.ActiveList[payto] += amount
                    resp = current.Owes[payto]
                # update Owe field of the one who lent amount
                if payto in current.Name and name in Member.ActiveList.keys() and payto in Member.ActiveList.keys():
                    # if they pay more, then an error message
                    if -current.Owes[name] < amount:
                        resp = Err_incorrectPayment
                        return resp
                    current.Owes[name] += amount
                current = current.next
                if current is None:
                    break

            return resp

    # remove  - remove node from the linked list
    # input   - name:string
    # return  - success msg if able to delete, else failure msg
    def remove(self, name):
        # if member not present, return
        resp = Error_MemberNotFound
        if self.head is None:
            return Error_MemberNotFound
        else:
            # if first element is to be removed
            if self.head.Name == name:
                # remove only if amount due is settled, return with error msg otherwise
                if Member.ActiveList[self.head.Name] == 0:
                    resp = SuccessMsg
                    # if only element in the list
                    if self.head.next is None:
                        self.head = None
                    else:
                        self.head = self.head.next
                else:
                    resp = FailureMsg
                return resp
            else:
                # remove the element from middle of the list
                current_node = self.head
                while current_node is not None:
                    if current_node.Name == name:
                        break
                    prev = current_node
                    current_node = current_node.next

                #  if key was not present in linked list
                if current_node is None:
                    return resp

                # Unlink the node from linked list if amount due is settled
                if Member.ActiveList[current_node.Name] == 0:
                    prev.next = current_node.next
                    resp = SuccessMsg
                else:
                    resp = FailureMsg
            return resp
