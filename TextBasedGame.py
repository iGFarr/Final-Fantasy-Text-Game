# Created by Isaac Farr
# On May 23, 2022
#
# I chose to randomize some elements of this game to keep things fresh. In order to keep things simple, I made
# the villain a value for one of the directional commands in one of the rooms. The villain position is static.

import random


# All of my global variables are here
rooms = {}
room_names = []
not_complete = True
end_game_message = ""
items = ['Dagger', 'Broad Sword', 'Steel Helmet', 'Potion', 'Chainmail', 'Phoenix Down', 'Remedy']

# This function both randomizes the item placement and resets some variables at the end of the game.
def shuffle_rooms():
    random.shuffle(items)  # Randomizes items before assignment in the following dict
    global rooms, room_names, not_complete, end_game_message
    rooms = {
        'Squall\'s Room': {'West': 'Commons Area',
                           'Item': items[0]},
        'Commons Area': {'East': 'Squall\'s Room',
                         'South': 'Main Hall',
                         'Item': items[1]},
        'Main Hall': {'North': 'Commons Area',
                      'South': 'Cafeteria',
                      'East': 'Medic\'s Tent',
                      'West': 'Training Room',
                      'Item': items[2]},
        'Training Room': {'East': 'Main Hall',
                          'Item': items[3]},
        'Cafeteria': {'North': 'Main Hall',
                      'East': 'Parking Lot',
                      'Item': items[4]},
        'Parking Lot': {'West': 'Cafeteria',
                        'Item': items[5]},
        'Medic\'s Tent': {'West': 'Main Hall',
                          'North': 'Sephiroth',
                          'Item': items[6]}
    }
    room_names = list(rooms.keys())  # I found that dict_keys type is non-iterable, so the easy solution was to
    not_complete = True                   # explicitly put them into a list.
    end_game_message = ""


class Player:

    def __init__(self):
        self.current_items = []
        self.isFirstPrint = True  # Simplifies the print_menu function. Certain text is only printed the first time.
        self.room_name = ""
        self.room = rooms[room_names[random.randint(0, len(room_names) - 1)]]  # The character is put in a random room
        for name in rooms:                                                     # at initialization.
            if self.room is rooms[name]:  # If the instance of Player classes room object is the same as rooms[name],
                self.room_name = name     # assigns the key to room_name

    # This function appends the current rooms item to current_items, and changes the current rooms item to an empty
    # string. It includes a safety check to avoid adding empty strings, and also prints that the item was added.
    def add_to_inventory(self):
        item_name = self.room['Item']
        if item_name not in self.current_items and item_name != "":
            self.current_items.append(item_name)
            print(f"Added {item_name} to inventory.")
            rooms[self.room_name]['Item'] = ""

    # This function reassigns the player's current room depending on the input. It also contains logic for if the
    # game should end.
    def change_rooms(self, command):
        self.room_name = self.room[command]
        if self.room_name == 'Sephiroth':
            global not_complete, end_game_message  # Provides access to global variables instead of declaring in local
            not_complete = False                   # scope. 'not_complete = False' ends the game.

            # There is actually an item in every room, but I felt if the parameter for requirement was 1 less than the
            # total number of items, the game would be more enjoyable, so I made 7 items, but only 6 are needed.
            if len(self.current_items) >= (len(rooms) - 1):
                end_game_message = "CONGRATULATIONS! You have defeated Sephiroth!"
            else:
                end_game_message = "You have failed...you should have prepared better."
            print()
        if self.room_name != 'Sephiroth':  # If the game doesn't end, change the room.
            self.room = rooms[self.room_name]

    def print_menu(self):
        item = self.room['Item']
        if self.isFirstPrint:
            print("Final Fantasy Text Game\n"
                  f"Collect at least {len(items) - 1} items before facing Sephiroth, or he will surely defeat you!\n")
        self.isFirstPrint = False
        print("Move Commands: go [North, South, East, West]\n"
              f"Add item to inventory: {f'get {item}' if item != '' else 'There are no items here.'}\n")
        print(f"You are currently in the {self.room_name}")
        print("Inventory:", ", ".join(self.current_items))
        print()


def main():
    shuffle_rooms()

    def play_game():
        while not_complete:
            current_player.print_menu()
            command = input()
            command_formatted = command.split()
            general_command = command_formatted[0].lower()  # Some input forgiveness for the first part of the command
            possible_commands = current_player.room  # All the keys for the current room

            # This block is a safety check to prevent keyErrors in case the user enters only 1 word or forgets a space.
            # It also puts everything after the first space as the specific command
            if len(command_formatted) <= 1:
                print("Please enter a valid command.")
                continue
            else:
                specific_command = " ".join(command_formatted[1:])

            if general_command not in acceptable_commands:
                print("Please enter a valid command.")  # More input validation.
                continue
            elif general_command == "go":
                if specific_command in possible_commands:
                    print(f"You go {specific_command}")
                    current_player.change_rooms(specific_command)
                elif specific_command not in ['North', 'South', 'East', 'West']:
                    print('Please enter a valid command.')  # In case a player doesn't enter a cardinal direction after 'go'
                    continue
                else:
                    print(f"You try to go {specific_command}...")
                    print("The way is blocked.")
            elif general_command == "get" and specific_command == possible_commands['Item']:
                current_player.add_to_inventory()
            elif general_command == "get" and specific_command not in possible_commands:
                print("Please enter a valid command.")  # More input validation.
                continue
        print(end_game_message)  # GG.

    while True:  # The while loop that comprises the game will end with the global variable
        current_player = Player()  # Instantiate a new Player object
        acceptable_commands = ["go", "get"]
        play_game()
        play_again = input("Do you want to play again?(Y/N)")
        if play_again == "Y":
            random.shuffle(items)
            shuffle_rooms()
            global rooms
            rooms = rooms
        if play_again == "N":
            break


if __name__ == "__main__":
    main()
