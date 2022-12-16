import contextlib
import unittest
from io import StringIO
from geektrust import *
from Expense_Management import *
from HouseMates import *
from Member import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        Member.MaxMember = 3
        self.head = None
        reset()

    def test_member_init(self):
        Member.memberCount = 0
        new_mem = Member("test1")
        self.assertEqual(new_mem.Name, "test1")
        self.assertEqual(new_mem.Owes, {})
        self.assertEqual(Member.memberCount, 1)
        increment_member_count()
        self.assertEqual(Member.memberCount, 2)
        decrement_member_count()
        self.assertEqual(Member.memberCount, 1)
        reset()
        self.assertEqual(Member.memberCount, 0)

    def test_append(self):
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test3")
        self.assertEqual(resp, SuccessMsg)

    def test_search(self):
        with self.assertRaises(SystemExit) as cm:
            resp = HouseMates.search(self, "test1")
        self.assertEqual(cm.exception.code, 1)
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        self.assertTrue(HouseMates.search(self, "test1"))
        self.assertFalse(HouseMates.search(self, "test2"))
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        self.assertTrue(HouseMates.search(self, "test2"))

    def test_print_list(self):
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.print_list(self)
        self.assertEqual(resp, "test1 - 0 - {}\ntest2 - 0 - {}\n")

    def test_print_dues(self):
        self.assertEqual(HouseMates.print_dues(self, "test1"), "Error: Empty list. No members found\n")
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.print_dues(self, "test2")
        self.assertEqual(resp, "")
        resp = HouseMates.print_dues(self, "test3")
        self.assertEqual(resp, "MEMBER_NOT_FOUND")
        resp = HouseMates.update_owes(self, "test1", "test2", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.print_dues(self, "test2")
        self.assertEqual(resp, "test1 0\n")
        resp = HouseMates.print_dues(self, "test1")
        self.assertEqual(resp, "test2 10\n")

    def test_format_dict(self):
        self.assertEqual(format_dict({"ANDY": 1, "BO": 2}), "BO 2\nANDY 1\n")
        self.assertEqual(format_dict({"ANDY": 0, "BO": 0}), "ANDY 0\nBO 0\n")
        self.assertEqual(format_dict({"ANDY": 1, "BO": 2, "ABI": 1}), "BO 2\nABI 1\nANDY 1\n")
        self.assertEqual(format_dict({"ANDY": 1, "BO": 2, "ABI": 1, "BOB": 2, "CINI": 4}),
                         "CINI 4\nBO 2\nBOB 2\nABI 1\nANDY 1\n")

    def test_update_owes(self):
        self.assertEqual(HouseMates.update_owes(self, "test1", "test2", 10), 0)
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test1", "test2", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.append(self, "test3")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test3", "test2", 20)
        self.assertEqual(resp, 1)
        resp = HouseMates.update_owes(self, "test3", "test4", 20)
        self.assertEqual(resp, 0)
        resp = HouseMates.append(self, "test4")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test3", "test4", 20)
        self.assertEqual(resp, 1)

    def test_initialize_owe_for_member(self):
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.initialize_owe_for_member(self)
        self.assertEqual(resp, (0, 0, [], []))
        resp = HouseMates.append(self, "test3")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test3", "test2", 20)
        self.assertEqual(resp, 1)
        self.assertTrue(HouseMates.balance_expenses(self))
        resp = HouseMates.initialize_owe_for_member(self)
        self.assertEqual(resp, (20, -20, ["test3"], ["test2"]))
        resp = HouseMates.update_owes(self, "test1", "test2", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.update_owes(self, "test1", "test3", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.initialize_owe_for_member(self)
        self.assertEqual(resp, (30, -30, ['test1', 'test3'], ['test2']))

    def test_balance_expenses(self):
        self.assertEqual(HouseMates.balance_expenses(self), "Error: Empty list. No members found\n")
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test1", "test2", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.append(self, "test3")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test3", "test2", 20)
        self.assertEqual(resp, 1)
        self.assertTrue(HouseMates.balance_expenses(self))
        resp = HouseMates.update_owes(self, "test1", "test2", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.update_owes(self, "test1", "test3", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.update_owes(self, "test2", "test3", 10)
        self.assertEqual(resp, 1)
        self.assertTrue(HouseMates.balance_expenses(self))

    def test_settle_dues(self):
        self.assertEqual(HouseMates.settle_dues(self, "test1", "test2", 10), "MEMBER_NOT_FOUND")
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test1", "test2", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.append(self, "test3")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test3", "test2", 20)
        self.assertEqual(resp, 1)
        self.assertTrue(HouseMates.balance_expenses(self))
        self.assertEqual(HouseMates.settle_dues(self, "test1", "test2", 6), 4)
        self.assertEqual(HouseMates.settle_dues(self, "test3", "test2", 20), 0)
        self.assertEqual(HouseMates.settle_dues(self, "test3", "test2", 20), "INCORRECT_PAYMENT")
        self.assertEqual(HouseMates.settle_dues(self, "test1", "test2", 10), "INCORRECT_PAYMENT")

    def test_remove(self):
        self.assertEqual(HouseMates.remove(self, "test1"), "MEMBER_NOT_FOUND")
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        self.assertEqual(HouseMates.remove(self, "test1"), "SUCCESS")
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.append(self, "test2")
        self.assertEqual(resp, SuccessMsg)
        self.assertEqual(resp, SuccessMsg)
        self.assertEqual(HouseMates.remove(self, "test1"), "SUCCESS")
        resp = HouseMates.append(self, "test1")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test1", "test2", 10)
        self.assertEqual(resp, 1)
        resp = HouseMates.append(self, "test3")
        self.assertEqual(resp, SuccessMsg)
        resp = HouseMates.update_owes(self, "test3", "test2", 20)
        self.assertEqual(resp, 1)
        self.assertTrue(HouseMates.balance_expenses(self))
        self.assertEqual(HouseMates.settle_dues(self, "test1", "test2", 6), 4)
        self.assertEqual(HouseMates.settle_dues(self, "test3", "test2", 20), 0)
        self.assertEqual(HouseMates.remove(self, "test3"), "SUCCESS")
        self.assertEqual(HouseMates.remove(self, "test1"), "FAILURE")
        self.assertEqual(HouseMates.remove(self, "test2"), "FAILURE")
        self.assertEqual(HouseMates.remove(self, "test4"), "MEMBER_NOT_FOUND")

    def test_expense_management_init(self):
        reset()
        contents = ["MOVE_IN ANDY"]
        ExpenseManagement(contents)
        contents = ["MOVE_IN"]
        with self.assertRaises(SystemExit) as cm:
            ExpenseManagement(contents)
        self.assertEqual(cm.exception.code, 1)
        contents = ["INVALID"]
        with self.assertRaises(SystemExit) as cm:
            ExpenseManagement(contents)
        self.assertEqual(cm.exception.code, 1)
        reset()
        contents = ["MOVE_IN ANDY", "MOVE_IN BO", "MOVE_OUT ANDY", "MOVE_OUT BO"]
        ExpenseManagement(contents)

    def test_move_in(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            ExpenseManagement.move_in(self, "ANDY")
            ExpenseManagement.move_in(self, "ANDY")
            ExpenseManagement.move_in(self, "ANDY BO")
            ExpenseManagement.move_in(self, "BO")
            ExpenseManagement.move_in(self, "WOODY")
            ExpenseManagement.move_in(self, "invalid")
        self.assertEqual(temp_stdout.getvalue().strip(),
                         "SUCCESS\nMember ANDY already moved In. Please verify the name\nInvalid Member Name\nSUCCESS\nSUCCESS\nHOUSEFUL")

    def test_spend(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            ExpenseManagement.move_in(self, "ANDY")
            ExpenseManagement.move_in(self, "BO")
            ExpenseManagement.move_in(self, "WOODY")
            ExpenseManagement.spend(self, "6000 WOODY ANDY BO")
            ExpenseManagement.spend(self, "0 WOODY ANDY BO")
            ExpenseManagement.spend(self, "60 WOODY WOODY")
            ExpenseManagement.spend(self, "60 WOODY BLA")
            ExpenseManagement.spend(self, "60 ABC BLA")
            ExpenseManagement.spend(self, "6000 ANDY BO")
        self.assertEqual(temp_stdout.getvalue().strip(),
                         "SUCCESS\nSUCCESS\nSUCCESS\nSUCCESS\nInvalid Amount\nInvalid spent-for-member name\nMEMBER_NOT_FOUND\nMEMBER_NOT_FOUND\nSUCCESS")

    def test_dues(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            ExpenseManagement.move_in(self, "ANDY")
            ExpenseManagement.move_in(self, "BO")
            ExpenseManagement.move_in(self, "WOODY")
            ExpenseManagement.spend(self, "6000 WOODY ANDY BO")
            ExpenseManagement.spend(self, "6000 ANDY BO")
            ExpenseManagement.dues(self, "ANDY BO")
            ExpenseManagement.dues(self, "INVALID")
            ExpenseManagement.dues(self, "ANDY")
            ExpenseManagement.dues(self, "BO")
        self.assertEqual(temp_stdout.getvalue().strip(),
                         "SUCCESS\nSUCCESS\nSUCCESS\nSUCCESS\nSUCCESS\nInvalid Member Name\nMEMBER_NOT_FOUND\nBO 0\nWOODY 0\nWOODY 4000\nANDY 1000")

    def test_clear_due(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            ExpenseManagement.move_in(self, "ANDY")
            ExpenseManagement.move_in(self, "BO")
            ExpenseManagement.move_in(self, "WOODY")
            ExpenseManagement.spend(self, "6000 WOODY ANDY BO")
            ExpenseManagement.spend(self, "6000 ANDY BO")
            ExpenseManagement.dues(self, "ANDY")
            ExpenseManagement.clear_due(self, "BO ANDY 1000 INVALID")
            ExpenseManagement.clear_due(self, "BO ANDY 0")
            ExpenseManagement.clear_due(self, "BO BO 10")
            ExpenseManagement.clear_due(self, "BO ANDY 1000")
        self.assertEqual(temp_stdout.getvalue().strip(),
                         "SUCCESS\nSUCCESS\nSUCCESS\nSUCCESS\nSUCCESS\nBO 0\nWOODY 0\nInvalid CLEAR_DUE input\nInvalid Amount\nInvalid pay_to name. member-who-owes and member-who-lent cannot be same\n0")

    def test_move_out(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            ExpenseManagement.move_in(self, "ANDY")
            ExpenseManagement.move_in(self, "BO")
            ExpenseManagement.move_in(self, "WOODY")
            ExpenseManagement.spend(self, "6000 WOODY ANDY BO")
            ExpenseManagement.spend(self, "6000 ANDY BO")
            ExpenseManagement.clear_due(self, "BO ANDY 1000")
            ExpenseManagement.move_out(self, "ANDY")
            ExpenseManagement.move_out(self, "ANDY BO")
            ExpenseManagement.move_out(self, "BO")
            ExpenseManagement.move_out(self, "BOB")
        self.assertEqual(temp_stdout.getvalue().strip(),
                         "SUCCESS\nSUCCESS\nSUCCESS\nSUCCESS\nSUCCESS\n0\nSUCCESS\nInvalid Member Name\nFAILURE\nMEMBER_NOT_FOUND")

    def test_readFromFile(self):
        f = open("demofile.txt", "w")
        f.write("")
        f.close()
        with self.assertRaises(SystemExit) as cm:
            read_from_file("invalid")
        self.assertEqual(cm.exception.code, 2)
        with self.assertRaises(SystemExit) as cm:
            read_from_file("demofile.txt")
        self.assertEqual(cm.exception.code, 2)
        f = open("demofile.txt", "w")
        s = "MOVE_IN ANDY"
        f.write(s)
        f.close()
        self.assertEqual(read_from_file("demofile.txt"), s.splitlines())

    def test_main(self):
        sys.argv.pop()
        sys.argv.append("invalid.txt")
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2)
        f = open("demofile.txt", "w")
        s = "MOVE_IN ANDY"
        f.write(s)
        f.close()
        sys.argv.pop()
        sys.argv.append("demofile.txt")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            main()
        self.assertEqual(temp_stdout.getvalue().strip(),
                         "SUCCESS")


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
