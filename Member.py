#!/usr/bin/python


# Represent member of the house
class Member:

    memberCount = 0
    ActiveList = {}
    MaxMember = 3

    def __init__(self, member):
        self.Name = member
        self.Owes = {}
        increment_member_count()
        self.next = None


# decrement_member_count - decrement member count by 1
def decrement_member_count():
    Member.memberCount -= 1


# increment_member_count - increment member count by 1
def increment_member_count():
    Member.memberCount += 1


# reset mem_count and ActiveList
def reset():
    Member.memberCount = 0
    Member.ActiveList = {}
