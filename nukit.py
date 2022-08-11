#####################################################################################################
# IMPORTS                                                                                           #
#####################################################################################################
import click
import os.path
from os import path
import shutil

#####################################################################################################
# CLICK GROUP                                                                                       #
# DESCRIPTION: A group allows application call to branch off to the appropriate function            #
#####################################################################################################

@click.group()
def cli():
    pass

#####################################################################################################
# ERROR DICTIONARY                                                                                  #
# DESCRIPTION: Gives proper errors during runtime                                                   #
#####################################################################################################

ERRLIST = {
    0 : "Generic Error Occured",
    1 : "Filepath Invalid",
    2 : "File/path does not exist",
    3 : "Failed to open nukelist.txt",
    4 : "The nukelist.txt does not exist"
}

def displayError(errorCode):
    print(ERRLIST[errorCode])

#####################################################################################################
# FUNCTIONS                                                                                         #
# DESCRIPTION: Functions with specified arguements and options                                      #
#####################################################################################################

# (1) - Test hello function
@click.command(short_help='Says hello to given name')
@click.option('--count', default=10, help='Number of greetings')
@click.argument('name')
def sayHello(count, name):
    for x in range(count):
        print('Hello,', name)

# (2) - NukeIt main function
@click.command(short_help='Nukes everything in nukelist')
@click.option('--ask', default=True, help='Ask for confirmation')
def nukeIt(ask):
    if ask == True:
        continueNuke = str(input("Confirm Nuking [y/n]: "))
        if continueNuke == 'y' or continueNuke == 'Y':
            with open(getAbsolutePath('nukelist.txt'), 'r', encoding='UTF-8') as file:
                while (line := file.readline().rstrip()):
                    if path.isfile(line):
                        os.remove(line)
                    else:
                        shutil.rmtree(line)
                    print('Nuked:\t',line)
        else:
            print('Aborting...')
    else:
        with open(getAbsolutePath('nukelist.txt'), 'r', encoding='UTF-8') as file:
                while (line := file.readline().rstrip()):
                    if path.isfile(line):
                        os.remove(line)
                    else:
                        shutil.rmtree(line)
                    print('Nuked:\t',line)
        

# (3) - Print the contents of nukelist.txt file
@click.command(short_help='Display the nukelist file contents')
@click.option('--lines', default=10, help='number of lines to print')
def printNukeList(lines):
    f = open(getAbsolutePath('nukelist.txt'), 'r')
    for x in range(0, lines):
        aLine = f.readline()
        if aLine != '':
            print(x,'-',aLine)
    f.close()

# (4) - Function to add given path to the nukelist.txt file
@click.command(short_help='Adds path to nukelist.txt function')
@click.argument('givenpath', type=click.STRING)
def addNukePath(givenpath):
    if checkPath(givenpath) == True:
        toAdd = getAbsolutePath(givenpath)
        f = open(getAbsolutePath('nukelist.txt'), 'a')
        f.write(str(toAdd) + '\n')
        f.close()
    else:
        displayError(2)


# (7) - Checks if file path exists
def checkPath(p):
    return path.exists(p)

# (8) - Print the contents of nukelist.txt file
def getAbsolutePath(p):
    if checkPath(p) == True:
        return os.path.abspath(p)
    else:
        displayError(2)
        return p


#####################################################################################################
# CLICK GROUP ADD                                                                                   #
# DESCRIPTION: Adding functions to the click group so they are callable through python application  #
#####################################################################################################

# 1. Test
cli.add_command(sayHello)           # (1)

# 2. Core
cli.add_command(nukeIt)             # (2)

# 3. Utility
cli.add_command(printNukeList)      # (3)
cli.add_command(addNukePath)        # (4)
#cli.add_command(removeNukePath)     # (5)
#cli.add_command(openEditor)         # (6)

# 4. Helping
#cli.add_command(checkPath)          # (7)
#cli.add_command(getAbsolutePath)    # (8)

#####################################################################################################
# MAIN FUNCTION                                                                                     #
# DESCRIPTION: Entry point of the python application that calls the click cli() function            #
#####################################################################################################

# Starting main function
if __name__ == '__main__':
    # The click group is called
    cli()