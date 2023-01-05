#list of message options
#if altitude is in a certain range, print corropsonding message ONCE

'''
Method 1:
if altitude < value1 and altitude > value2 and previous_message = 0:
    print message
    previous_message = 1
'''

'''
Method 2:
if altitude = value:
    printe message
'''

'''
Method 3:
message1 = ["message", "n"]
if altitude < value1 and altitude > value2 and message1[1] == "n":
    print message1[0]
    message1[1] = "y"
'''