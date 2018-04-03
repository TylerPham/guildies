import json
import pytest
from app import app

# unfortunately I could not get pytest working with my implementation, 
# if I were to get pytest running, these are the test that I would write.


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

# create_player 
# adding valid player (nice)
# adding a player without nickname
# adding a player without email
# adding a player without skillpoints
# adding player with non unique nickname
# adding player with non unique email
# adding a player with non alphanumeric nickname
# adding a player with invalid email
# adding a player with non integer skillpoints

# update_player
# update a valid player (nice)
# update player that doesn't exist
# update valid player with non unique nickname
# update valid player with non unique email
# update valid player with non integer skillpoints
# update valid player with partial parameters
# update valid player with empty parameters
# update valid player with non alphanumeric nickname
# update valid player with invalid email
# update valid player with non integer skillpoints

# delete_player
# delete a valid player (nice)
# delete player that doesn't exist
# delete a player with non integer id

# create_guild
# create a valid guild with country code
# create a valid guild without country code
# create a guild with non alphanumeric name
# create a guild with invalid country code

# update_guild
# update a guild with valid name and country code (nice)
# update a guild with invalid name and country code
# update a guild with invalid name and invalid country code
# update a guild with valid name and invalid country code
# update a guild that doesn't exist

# delete_guild
# delete a guild that exists
# delete a guild that doesn't exist
# delete a guild with non integer id

# create_item
# create a valid item
# create an item with invalid skillpoints

# update_item
# update a valid item
# update an item that doesn't exist
# update a valid item with invalid skillpoints

# delete_item
# delete valid item
# delete item that doesn't exist
# delete item with invalid id

# add_player_to_guild
# add player not in guild to valid guild
# add player in valid guild to another valid guild
# add player to non existent guild
# add player to same guild

# delete_player_from_guild
# delete player in a valid guild from valid guild
# delete player in a guild from non affiliated guild
# delete player not in a guild from a valid guild
# delete non existant player from valid guild
# delete player from non existant guild

# add_item_to_player
# add valid item to player (nice) 
#     check ownership and skillpoints
# add item that doesn't exist to player
# add valid item to player that doesn't exist
# add item to multiple valid players in unique guilds
#     check ownership and skillpoint
# add item to multiple valid players in same guild
#     check ownership and skillpoint
# add item to multiple valid players in differing and same guild
#     check ownership and skillpoint

# get_guild_total_skillpoints
# check skill points of members



