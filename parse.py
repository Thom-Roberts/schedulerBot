#I want to write and read to an xml file
#I'm writing to bot.xml
#If the second argument is write, you write to the file. If its read, read from it
import sys
import xml.etree.cElementTree as ET

#how you get arguments
"""print ("This is the name of the script: ", sys.argv[0])
print ("Number of arguments: ", len(sys.argv))
print ("The arguments are: " , str(sys.argv))"""

action = sys.argv[1]
tree = ET.parse('bot.xml')
root = tree.getroot()
if action == 'write':
    #if there is something to write
    if len(sys.argv) == 3:
        ET.SubElement(root, "item").text = sys.argv[2]
        tree = ET.ElementTree(root)
        tree.write('bot.xml')
    else:
        print("Too few arguments. Please provide a value to write")
elif action == 'read':
    for item in root:
        print(item.text)
else:
    print("Command not recognized")
