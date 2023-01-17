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

#msg11 plays shortly after string cut

'''
message 1: turret_autosearch_1, turretlaunched05
message 2: turret_pickup_2, turretlaunched08, turretlaunched09, sp_sabotage_factory_good_fail04, turretstuckintube09
message 3: turret_pickup_5, turretlightbridgeblock03, sp_sabotage_factory_good_fail03
message 4: turret_pickup_8, turretlightbridgeblock02, turret_search_1, turret_disabled_7
message 5: turret_disabled_5, turret_disabled_6, sp_sabotage_factory_good_fail02, turretstuckintubetakemewith01, turretstuckintubetakemewith02
message 6: turret_collide_4, turretwitnessdeath11, turretstuckintubegoodbye01, turretshotbylaser07, turretshotbylaser08, turret_disabled_8
message 7: turret_retire_5, turretlaunched03, turretlaunched06, turretlaunched07, turret_retire_1
message 8: turret_fizzler_1, turret_tipped_5, sp_sabotage_factory_good_fail05, sp_sabotage_factory_good_fail06, turretlaunched01, turretlaunched02, turretlaunched10, turret_tipped_6
'''