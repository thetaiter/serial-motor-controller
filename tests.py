# Import built-im testing library
import unittest

# Import Tkinter for testing
import tkinter as tk

# Import local libraries to test
from lib import variable, command, command_type, program, app

# Make class calls easier
Variable = variable.Variable
Command = command.Command
CommandType = command_type.CommandType
Program = program.Program

# Testing class
class TestMethods(unittest.TestCase):
    # Test for Variable class
    def test1(self):
        print("\nTesting Variable...")

        # Sub test for constructor with no parameters
        with self.subTest():
            print("\tTesting constructor without parameters...")

            v = Variable()

            self.assertEqual(v.getSymbol(), 'x', "New variable method 'getSymbol()' did not return correctly.")
            print("\t\tgetSymbol() test passed.")
            self.assertEqual(v.getLow(), 0, "New variable method 'getLow()' did not return correctly.")
            print("\t\tgetLow() test passed.")
            self.assertEqual(v.getHigh(), 10, "New variable method 'getHigh()' did not return correctly.")
            print("\t\tgetHigh() test passed.")
            self.assertEqual(v.getCurrentValue(), 5, "New variable method 'getCurrentValue()' did not return correctly.")
            print("\t\tgetCurrentValue() test passed.")
            self.assertIsNone(v.getEntry(), "New variable method 'getEntry()' did not return correctly.")
            print("\t\tgetEntry() test passed.")
            self.assertIsNone(v.getEntryValue(), "New variable method 'getEntryValue()' did not return correctly.")
            print("\t\tgetEntryValue() test passed.")

            l, h = v.getLowAndHigh()
            self.assertEqual(l, 0, "New variable method 'getLowAndHigh()' did not return correctly.")
            self.assertEqual(h, 10, "New variable method 'getLowAndHigh()' did not return correctly.")
            print("\t\tgetLowAndHigh() test passed.")

        # Sub test for custom variable with constructor parameters
        with self.subTest():
            print("\tTesting constructor with parameters...")
            e = tk.Entry()
            v = Variable(symbol='r', low=-56, high=193, currentValue=26, entry=e)

            self.assertEqual(v.getSymbol(), 'r', "New variable method 'getSymbol()' did not return correctly.")
            print("\t\tgetSymbol() test passed.")
            self.assertEqual(v.getLow(), -56, "New variable method 'getLow()' did not return correctly.")
            print("\t\tgetLow() test passed.")
            self.assertEqual(v.getHigh(), 193, "New variable method 'getHigh()' did not return correctly.")
            print("\t\tgetHigh() test passed.")
            self.assertEqual(v.getCurrentValue(), 26, "New variable method 'getCurrentValue()' did not return correctly.")
            print("\t\tgetCurrentValue() test passed.")
            self.assertEqual(v.getEntry(),e, "New variable method 'getEntry()' did not return correctly.")
            print("\t\tgetEntry() test passed.")
            self.assertEqual(v.getEntryValue(), "26", "New variable method 'getEntryValue()' did not return correctly.")
            print("\t\tgetEntryValue() test passed.")

            l, h = v.getLowAndHigh()
            self.assertEqual(l, -56, "New variable method 'getLowAndHigh()' did not return correctly.")
            self.assertEqual(h, 193, "New variable method 'getLowAndHigh()' did not return correctly.")
            print("\t\tgetLowAndHigh() test passed.")

        with self.subTest():
            print("\tTesting setter methods...")

            v.setSymbol('f')
            self.assertEqual(v.getSymbol(), 'f', "New variable method \"setSymbol(\'f\')\" did not set the symbol correctly.")
            print("\t\tsetSymbol('f') test passed.")

            v.setLow(0)
            self.assertEqual(v.getLow(), 0, "New variable method 'setLow(0)' did not set the low correctly.")
            print("\t\tsetLow(0) test passed.")

            v.setHigh(100)
            self.assertEqual(v.getHigh(), 100, "New variable method 'setHigh(100)' did not set the high correctly.")
            print("\t\tsetHigh(100) test passed.")

            v.setEntryValue(88)
            self.assertEqual(v.getEntryValue(), "88", "New variable method 'setEntryValue(88)' did not set the entry value correctly.")
            print("\t\tsetEntryValue(88) test passed.")

            v.setCurrentValue()
            self.assertEqual(v.getCurrentValue(), 88, "New variable method 'setCurrentValue()' did not set the current value correctly.")
            print("\t\tsetCurrentValue() test passed.")

            v.setCurrentValue(24)
            self.assertEqual(v.getCurrentValue(), 24, "New variable method 'setCurrentValue(24)' did not set the high correctly.")
            print("\t\tsetCurrentValue(24) test passed.")

            e = tk.Entry()
            v.setEntry(e)
            self.assertEqual(v.getEntry(), e, "New variable method 'setEntry()' did not set the entry correctly.")
            print("\t\tsetEntry() test passed.")

    # Test for Command class
    def test2(self):
        print("\nTesting Command...")
        # Sub test for constructor with no parameters
        with self.subTest():
            print("\tTesting constructor without parameters...")

            c = Command()

            self.assertEqual(c.getName(), "New Command", "New command method 'getName()' did not return correctly.")
            print("\t\tgetName() test passed.")

            self.assertEqual(c.getCommandRaw(), "command_x", "New command method 'getCommandRaw()' did not return correctly.")
            print("\t\tgetCommandRaw() test passed.")

            self.assertEqual(c.getCommand(), "command_x", "New command method 'getCommand()' did not return correctly.")
            print("\t\tgetCommand() test passed.")

            self.assertIsNone(c.getVariables(), "New command method 'getVariables()' did not return correctly.")
            print("\t\tgetVariables() test passed.")

            self.assertIsNone(c.getVariable(0), "New command method 'getVariable(0)' did not return correctly.")
            print("\t\tgetVariable(0) test passed.")

            self.assertIsNone(c.getVariable('x'), "New command method 'getVariable(\'x\') did not return correctly.'")
            print("\t\tgetVariable('x') test passed.")

            self.assertEqual(c.numVariables(), 0, "New command method 'numVariables()' did not return correctly.")
            print("\t\tnumVariables() test passed.")

            self.assertEqual(c.getDescription(), 'Description', "New command method 'getDescription' did not return correctly.")
            print("\t\tgetDescription() test passed.")

            self.assertIsNone(c.getFrame(), "New command method 'getFrame()' did not return correctly.")
            print("\t\tgetFrame() test passed.")

        # Sub test for new custom command with constructor parameters
        with self.subTest():
            print("\tTesting constructor with parameters...")

            variables = [Variable(symbol='y', low=-1234, high=1234, currentValue=72), Variable('x', -5, 5, -2)]
            c = Command(name="Test Command", command="Com_x_y", variables=variables, description="This is the description")

            self.assertEqual(c.getName(), "Test Command", "Custom command method 'getName()' did not return correctly.")
            print("\t\tgetName() test passed.")

            self.assertEqual(c.getCommandRaw(), "Com_x_y", "Custom command method 'getCommandRaw()' did not return correctly.")
            print("\t\tgetCommandRaw() test passed.")

            self.assertEqual(c.getCommand(), "Com_-2_72", "Custom command method 'getCommandRaw()' did not return correctly.")
            print("\t\tgetCommand() test passed.")

            self.assertListEqual(c.getVariables(), variables, "Custom command method 'getVariables()' did not return correctly.")
            print("\t\tgetVariables() test passed.")

            self.assertIsInstance(c.getVariable(0), Variable, "Custom command method 'getVariable(0)' did not return correctly.")
            print("\t\tgetVariable(0) test passed.")

            self.assertIsInstance(c.getVariable('x'), Variable, "Custom command method 'getVariable(\'x\')' did not return correctly.")
            print("\t\tgetVariable('x') test passed.")

            self.assertEqual(c.numVariables(), 2, "Custom command method 'numVariables()' did not return correctly.")
            print("\t\tnumVariables() test passed.")

            self.assertEqual(c.getDescription(), "This is the description", "Custom command method 'getDescription()' did not return correctly.")
            print("\t\tgetDescription() test passed.")

            self.assertIsNone(c.getFrame(), "Custom command method 'getFrame()' did not return correctly.")
            print("\t\tgetFrame() test passed.")

        # Sub test for setter methods
        with self.subTest():
            print("\tTesting setter methods...")

            c.setName("New Name")
            self.assertEqual(c.getName(), "New Name", "Setter method 'setName(\'New Name\')' did not set the name properly.")
            print("\t\tsetName() test passed.")

            c.setCommand("new_command_x_y")
            self.assertEqual(c.getCommandRaw(), "new_command_x_y", "Setter method 'setCommand(\'new_command_x_y\')' did not set the command correctly.")
            print("\t\tsetCommand() test passed.")

            v = Variable()
            c.setVariables([v])
            self.assertListEqual(c.getVariables(), [v], "Setter method 'setVariables([Variable()])' did not set the variables correctly.")
            print("\t\tsetVariables() test passed.")

    # Test for CommandType class
    def test3(self):
        print("\nTesting CommandType...")

        # Sub Test for constructor without parameters
        with self.subTest():
            print("\tTesting constructor without parameters...")

            t = CommandType()

            self.assertEqual(t.getName(), 'New Type', "New CommandType method 'getName()' did not return correctly.")
            print("\t\tgetName() test passed.")

            self.assertEqual(t.getPath(), '', "New CommandType method 'getPath()' did not return correctly.")
            print("\t\tgetPath() test passed.")

            self.assertIsNone(t.getCommands(), "New CommandType method 'getCommands()' did not return correctly.")
            print("\t\tgetCommands() test passed.")

            self.assertIsNone(t.getCommand(0), "New CommandType method 'getCommand(0)' did not return correctly.")
            print("\t\tgetCommand(0) test passed.")

            self.assertIsNone(t.getCommand('command'), "New CommandType method 'getCommand(\'command\')' did not return correctly.")
            print("\t\tgetCommand(\'command\') test passed.")

            self.assertEqual(t.numCommands(), 0, "New CommandType method 'numCommands()' did not return correctly.")
            print("\t\tnumCommands() test passed.")

        # Sub test for constructor with parameters
        with self.subTest():
            print("\tTesting constructor with parameters...")

            c1 = Command()
            variables = [Variable(symbol='y', low=-1234, high=1234, currentValue=72), Variable('x', -5, 5, -2)]
            c2 = Command(name="Test Command", command="Com_x_y", variables=variables, description="This is the description")
            commands = [c1, c2]
            t = CommandType(name='New CType', path='/path/to/command_type.csv', commands=commands)

            self.assertEqual(t.getName(), 'New CType', "New CommandType method 'getName()' did not return correctly.")
            print("\t\tgetName() test passed.")

            self.assertEqual(t.getPath(), '/path/to/command_type.csv', "New CommandType method 'getPath()' did not return correctly.")
            print("\t\tgetPath() test passed.")

            self.assertListEqual(t.getCommands(), commands, "New CommandType method 'getCommands()' did not return correctly.")
            print("\t\tgetCommands() test passed.")

            self.assertEqual(t.getCommand(0), c1, "New CommandType method 'getCommand(0)' did not return correctly.")
            print("\t\tgetCommand(0) test passed.")

            self.assertEqual(t.getCommand('Test Command'), c2, "New CommandType method 'getCommand(\'command\')' did not return correctly.")
            print("\t\tgetCommand(\'command\') test passed.")

            self.assertEqual(t.numCommands(), 2, "New CommandType method 'numCommands()' did not return correctly.")
            print("\t\tnumCommands() test passed.")

        # Sub test for setter methods
        with self.subTest():
            print("\tTesting setter methods...")

            t.setName('the name')
            self.assertEqual(t.getName(), 'the name', "New CommandType method 'getName()' did not return correctly.")
            print("\t\tgetName() test passed.")

            t.setPath('/the/path/test.csv')
            self.assertEqual(t.getPath(), '/the/path/test.csv', "New CommandType method 'getPath()' did not return correctly.")
            print("\t\tgetPath() test passed.")

            commands = [c2, c1]
            t.setCommands(commands)
            self.assertListEqual(t.getCommands(), commands, "New CommandType method 'getCommands()' did not return correctly.")
            print("\t\tgetCommands() test passed.")

            self.assertEqual(t.getCommand(0), c2, "New CommandType method 'getCommand(0)' did not return correctly.")
            print("\t\tgetCommand(0) test passed.")

            self.assertEqual(t.getCommand('New Command'), c1, "New CommandType method 'getCommand(\'command\')' did not return correctly.")
            print("\t\tgetCommand(\'command\') test passed.")

            self.assertEqual(t.numCommands(), 2, "New CommandType method 'numCommands()' did not return correctly.")
            print("\t\tnumCommands() test passed.")

    # Test for Program class
    def test4(self):
        print("\nTesting Program...")

        # Sub test for constructor without parameters
        with self.subTest():
            print("\tTesting constructor without parameters...")

            p = Program()

            self.assertEqual(p.getNumber(), 0, "New program method 'getNumber()' did not return correctly.")
            print("\t\tgetNumber() test passed.")

            self.assertIsNone(p.getRawCommands(), "New program method 'getRawCommands()' did not return correctly.")
            print("\t\tgetRawCommands() test passed.")

            self.assertEqual(p.getCompiledProgram(), "", "New program method 'getCompiledProgram()' did not return correctly.")
            print("\t\tgetCompiledProgram() test passed.")

        # Sub test for constructor with parameters
        with self.subTest():
            print("\tTesting constructor with parameters (requires app to run)...")

            print("\t\tCreating program...")
            p = Program(master = app.MotorControlApp(tk.Tk(), log=False), number=3, commands=['lmMx(1, 1600)', 'l2M400'])

            self.assertEqual(p.getNumber(), 3, "New program method 'getNumber()' did not return correctly.")
            print("\t\tgetNumber() test passed.")

            self.assertListEqual(p.getRawCommands(), ['E', 'PM-3', 'lmMx(1, 1600)', 'l2M400', 'Q'], "New program method 'getRawCommands()' did not return correctly.")
            print("\t\tgetRawCommands() test passed.")

            self.assertEqual(p.getCompiledProgram(), "E,PM-3,l1M1600,l2M400,Q", "New program method 'getCompiledProgram()' did not return correctly.")
            print("\t\tgetCompiledProgram() test passed.")

        # Sub test for other methods
        with self.subTest():
            print("\tTesting other methods...")

            p.setNumber(2)

            self.assertEqual(p.getNumber(), 2, "Program method 'getNumber()' did not return correctly.")
            print('\t\tsetNumber(2) test passed.')

            p.clear()

            self.assertIsNone(p.getRawCommands(), "Program method 'getRawCommands()' did not return correctly.")
            self.assertEqual(p.getCompiledProgram(), "", "Program method 'getCompiledProgram()' did not return correctly.")
            print("\t\tclear() test passed.")

            p.addCommand('lmMx(2, 800)')
            p.addCommand('l1M2400')

            self.assertListEqual(p.getRawCommands(), ['lmMx(2, 800)', 'l1M2400'], "Program method 'getRawCommands()' did not return correctly.")
            print("\t\taddCommand('lmMx(2, 800)') test passed.")
            print("\t\taddCommand('l1M2400') test passed.")

            print("\t\tCompiling...")
            p.compile()

            self.assertListEqual(p.getRawCommands(), ['E', 'PM-2', 'lmMx(2, 800)', 'l1M2400', 'Q'], "Program method 'getRawCommands()' did not return correctly.")
            self.assertEqual(p.getCompiledProgram(), 'E,PM-2,l2M800,l1M2400,Q', "Program method 'getCompiledProgram()' did not return correctly.")
            print("\t\tcompile() test passed.")

            p.addCommand('L0')

            self.assertListEqual(p.getRawCommands(), ['E', 'PM-2', 'lmMx(2, 800)', 'l1M2400', 'L0'], "Program method 'getRawCommands()' did not return correctly.")
            print("\t\taddCommand('L0') test passed")

            print("\t\tCompiling...")
            p.compile()

            self.assertListEqual(p.getRawCommands(), ['E', 'PM-2', 'lmMx(2, 800)', 'l1M2400', 'L0', 'Q'], "Program method 'getRawCommands()' did not return correctly.")
            self.assertEqual(p.getCompiledProgram(), 'E,PM-2,l2M800,l1M2400,L0,Q', "Program method 'getCompiledProgram()' did not return correctly.")
            print("\t\tcompile() test passed.")

            p.setRawCommands(['foo', 'bar'])

            self.assertListEqual(p.getRawCommands(), ['foo', 'bar'], "Program method 'getRawCommands()' did not return correctly.")
            print("\t\tsetRawCommands() test passed.")

            print("\nAll tests passed successfully!")

if __name__ == '__main__':
    unittest.main()