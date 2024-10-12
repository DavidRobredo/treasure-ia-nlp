import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

"""
Processor of the commands in Natural Language
"""
class CommandProcessor:
    def __init__(self):
        # All possible commands (we define a couple of alternative commands in case they use the wrong word)
        self.tools_keywords = {
            1: ["shears", "1", "wool", "scissors"],
            2: ["shovel", "2", "dirt", "grass"],
            3: ["axe", "3", "wood", "tree"],
            4: ["pickaxe", "4", "stone", "cobblestone", "rock"]
        }
        self.move_keywords = {
            "up": ["up", "north"],
            "down": ["down", "south"],
            "left": ["left", "west"],
            "right": ["right", "east"]
        }
        self.keep_keywords = set(["down", "up", "left", "right", "help", "answer", "path"])

    def process_command(self, command, player, grid, inventory, highlighted_path, notification_system, user_path_cost, win_screen):
        command = command.lower()
        tokens = command.split()
        tokens = [token for token in tokens if token.isalnum()]

        stop_words = set(stopwords.words('english'))

        # Extracting the keywords in the command
        filtered_tokens = [
            token for token in tokens 
            if token not in stop_words or token in self.keep_keywords
        ]

        # If the command contains a direction command, we trigger the player movement
        for direction, keywords in self.move_keywords.items():
            if any(keyword in filtered_tokens for keyword in keywords):
                player.move(direction, grid, notification_system, user_path_cost, win_screen)

        # If the command contains a tool command, we trigger the tool change
        for token in filtered_tokens:
            for tool_number, keywords in self.tools_keywords.items():
                if token in keywords:
                    player.change_tool(tool_number, user_path_cost)
                    inventory.update(tool_number)


        # If the users asks for helps, we trigger the path highlighting
        if any(token in ["answer", "help", "path"] for token in filtered_tokens):
            grid.highlight_path(highlighted_path)
            notification_system.add_notification("Now we can get to the end, captain!")

        # In case there is not valid keyword
        # notification_system.add_notification("I didn't understand the order, captain!")
        
