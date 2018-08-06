import cmd
import sys

class Console(cmd.Cmd):
    def do_EOF(self,line):
        return True
    def do_foo(self,line):
        print ("In foo")
    def do_bar(self,line):
        print ("In bar")
    def cmdloop_with_keyboard_interrupt(self):
        doQuit = False
        while doQuit != True:
            try:
                self.cmdloop()
                doQuit = True
            except KeyboardInterrupt:
                sys.stdout.write('\n')

console = Console()
console.cmdloop_with_keyboard_interrupt()

print ('Done!')
