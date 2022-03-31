"""
HiddenHID by BrightShard
Explanation & documentation in the README on my GitHub page:
https://github.com/Bright-Shard/HiddenHID
"""

# For the invisible GUI
from tkinter import Tk, Entry, Menu
# Run commands in a shell
from subprocess import run as shell
# For enabling debug
from sys import argv
# Get host OS
from platform import system as os


class App(Tk):
    """
    The invisible app that runs terminal commands
    """
    def __init__(self):
        # Store host OS
        self.os = os()

        # macOS stuff
        if self.os == "Darwin":
            # Make the terminal invisible
            if "vis" not in argv and "visible" not in argv:
                shell(
                    'osascript -e \'tell application "Finder"\nset visible of process "Terminal" to false\nend tell\'',
                    shell=True, check=False)

        # Actually set up Tkinter
        super().__init__()

        # Shortcut commands
        # Shell functions
        def revShell(*args):
            return
        self.shortcuts = {
            'Darwin': {
                'wallpaper': 'curl -o "/tmp/wallpaper" "{args[0]}"; osascript -e \'tell application\
                     "Finder" to set the desktop picture to POSIX file "/tmp/wallpaper"\'; rm\
                     /tmp/wallpaper',
                'volume': 'osascript -e \'set Volume {args[0]}\'',
                'mute': 'osascript -e \'set Volume 0\'',
                'shell': revShell
            }
        }

        # If 'visible' is not passed as an argument, make the window invisible
        if "vis" not in argv and "visible" not in argv:
            self.attributes('-alpha', 0)

        # Commands are typed into the entry box
        self.entry = Entry(self)
        # Add it to the window
        self.entry.pack()
        # Focus the entry box so the keyboard types into it
        self.entry.focus()
        # Bind the enter key to run the command
        self.entry.bind('<Enter>', self.run_command)
        # It's the return key on some devices, so bind that too
        self.entry.bind('<Return>', self.run_command)

        # If debug is passed as an argument, enable debug mode, otherwise disable it
        if "debug" in argv:
            # Show debug mode is enabled
            print("Debug mode enabled")
            # Enable debug mode
            self.debug = True
        else:
            # Disable debug mode
            self.debug = False

        # On macOS, toolbars still show for invisible apps
        # This clones the toolbar from Finder, so it looks like Finder is open
        # Just make sure the file is named "Finder" so that's what is displayed as the app name
        if self.os == "Darwin":
            # The app toolbar
            menu = Menu(self)
            # Blank menu for each toolbar item
            # Programming in each toolbar action is just too much effort lol
            submenu = Menu(menu, tearoff=0)
            # Each of the toolbar menus in Finder, cloned here
            menu.add_cascade(label="File", menu=submenu)
            menu.add_cascade(label="Edit", menu=submenu)
            menu.add_cascade(label="View", menu=submenu)
            menu.add_cascade(label="Go", menu=submenu)
            menu.add_cascade(label="Window", menu=submenu)
            menu.add_cascade(label="Help", menu=submenu)
            self.config(menu=menu)

    def run_command(self, *args, **kwargs):
        """
        When 'enter' is pressed, run the command in Subprocess
        The command is taken from the entry widget's text, then the entry widget is cleared
        """
        # Get the text box contents to get the command
        command = self.entry.get()

        # If it's blank, don't even process the command
        if command == '':
            return

        # Debug
        if self.debug:
            print(f"Running command '{command}'")

        # Exit if the command is 'exit'
        if command == "exit":
            self.quit()

        # Split the command up to get the arguments
        splitCommand = self.entry.get().split(' ')

        # If the command is a shortcut, run the shortcut
        if splitCommand[0] in self.shortcuts:
            # The shortcut
            shortcut = self.shortcuts[splitCommand[0]]
            # Print that a shortcut was detected
            if self.debug:
                print('-> Shortcut detected! Converting the command to shortcut...')
            # If the shortcut is a string, run it as a shell script
            if type(shortcut) == str:
                shell(shortcut.format(args=splitCommand[1:]))
            # If the shortcut is a function, run the python code
            elif callable(shortcut):
                shortcut(splitCommand[1:])
            return

        # Run the command
        shell(command, shell=True, check=False)

        # Clear the command input
        self.entry.delete(0, len(self.entry.get()))
        # Print a new line for a separator between command outputs
        print('')

    def quit(self):
        """
        Quit the app and close any open terminals
        """
        print("-> Goodbye")
        # macOS stuff
        if self.os == 'Darwin':
            # Kill all terminals
            shell('killall Terminal', shell=True)


App().mainloop()