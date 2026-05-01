"""
This project done by:
Aws Hyasat
Zaid Hamdan
Basel Alquoqa
"""
import json

# colors (for printing)
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def load_data(filename):
    """
    Loading the data from json file
    """
    try:
        # Open the file and load the JSON data
        with open(filename) as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"{RED}No existing database found.{RESET} Starting fresh!")
        return {} # Return an empty

def save_data(data_dictionary, filename):
    """
    Saves the game database dictionary into a JSON file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data_dictionary, f, indent=4)
            print(f"{GREEN}Database successfully saved!{RESET}")

    except IOError:
        print(f"{RED}Error: Could not save the database.{RESET}")

def calculate_jaccard(tags1, tags2):
    """
    Calculates the Jaccard Similarity between two lists of tags
    """
    # Convert lists to sets to easily find overlapping and unique tags
    set1 = set(tags1)
    set2 = set(tags2)

    # Calculate intersection (shared tags) and union (total unique tags)
    intersection = len(set1 & set2)
    union = len(set1 | set2)

    # Prevent division by zero if neither game has any tags listed
    if union == 0:
        return 0.0

    # Formula: (Shared tags) / (Total unique tags)
    return intersection / union

def get_score(item):
    """
    Helper function to return the similarity score for sorting.
    """
    # The score is the second item (index 1) in the (game_name, score) tuple
    return item[1]

def recommend_games(games_database):
    """
    Recommends the top 3 games based on Jaccard Similarity.
    """

    # Get and validate target game
    while True:
        user_input = input("Enter the name of the game you like(enter \"return\" to back to menu): ").strip()

        if user_input.lower() == "return":
            return

        target_game = None
        for game in games_database:
            if game.lower() == user_input.lower():
                target_game = game
                break

        if target_game is None:
            print(f"{RED}Game not found in the database.{RESET}")

        else:
            break

    # Retrieve tags for the target game (default to empty list if missing)
    target_genres = games_database[target_game].get("Genres", [])
    similar_games = []

    # Calculate similarity scores against all other games
    for game, details in games_database.items():
        # Skip comparing the target game to itself
        if game == target_game:
            continue

        genres = details.get("Genres", [])
        similarity = calculate_jaccard(target_genres, genres)

        # Store the result as a tuple: (game_name, score)
        similar_games.append((game, similarity))

    # Sort the list of tuples using the named helper function (highest score first)
    similar_games.sort(key=get_score, reverse=True)

    # Display the top 3 recommendations
    print(f"Because you enjoyed '{target_game}', we recommend these top 3 games:")

    counter = 1
    for game, score in similar_games[:3]:
        print(f"{counter}. {game} (Similarity Score: {score:.2f})")
        counter += 1

def data_filter(data):
    """
    Filters the game database based on user-defined criteria.
    The user can choose to filter by a minimum Metacritic score or a maximum price.
    """
    userPref = "-1"
    while userPref != "1" and userPref != "2":
        userPref = input("1) filter by Minimum Metacritic Score\n2) filter by Maximum Price\nChoose filter option(1 or 2 or enter \"return\" to back to menu): ").strip()

        if userPref.lower() == "return":
            return

        if userPref == "1":
            while True:
                min_score = input("Enter the minimum Metacritic score you are looking for: ").strip()

                if min_score.isdigit():
                    print("--- Filter Results ---")

                    found = False
                    for g, i in data.items():
                        if i["Metacritic"] != "N/A" and i["Metacritic"] >= int(min_score):
                            print(f"{g} | Metacritic: {i['Metacritic']}")
                            found = True

                    if not found:
                        print(f"{RED}No games matched your filter{RESET}")
                    break

                else:
                    print(f"{RED}wrong score.{RESET} Please try again")

        elif userPref == "2":
            while True:
                try:
                    max_price = float(input("Enter the maximum price you are willing to pay in dollars: "))
                    if max_price >= 0:
                        print("--- Filter Results ---")

                        found = False
                        for g, i in data.items():
                            if i["Price"] != "Unknown" and i["Price"] <= max_price:
                                print(f"{g} | Price: {i['Price']}")
                                found = True

                        if not found:
                            print(f"{RED}No games matched your filter{RESET}")
                        break

                    else:
                        print(f"{RED}wrong price.{RESET} Please try again.")

                except ValueError:
                    print(f"{RED}wrong price.{RESET} Please try again")

        else:
            print(f"{RED}wrong input.{RESET} Please try again")

def find_game(games_database):
    """
    Searches the database for a specific game by substring
    """
    while True:
        search_term = input("Enter a word or phrase to search for(enter \"return\" to back to menu): ").strip().lower()
        found = False

        if search_term.lower() == "return":
            break

        if search_term == "":
            print(f"{RED}Search term cannot be empty.{RESET}")
            continue
        print(f"---Search Results---")
        for title, details in games_database.items():
            if search_term in title.lower():
                found = True
                dev = details.get("Developer", "Unknown")
                year = details.get("Year", "Unknown")
                score = details.get("Metacritic", "N/A")

                # Format output cleanly
                print(f"Title: {title} | Developer: {dev} | Year: {year} | Metacritic: {score}")

        if not found:
            print(f"{RED}No titles matched your search.{RESET}")

def insert_game(games_database):
    """
    Inserts a new game into the database with user_provided details
    """
    while True:
        title = input("Enter the title of the game to add(enter \"return\" to back to menu): ").strip()

        if title.lower() == "return":
            return

        if title == "":
            print(f"{RED}Game title cannot be empty.{RESET} Please provide a valid title.")
            continue

        exists = False
        for game in games_database:
            if game.lower() == title.lower():
                exists = True
                break

        if exists:
            print(f"{RED}This game already exists in the database.{RESET}")
            continue
        break

    developer = input("Enter the developer's name (Enter None if data is unavailable): ").strip()
    if developer.lower() == "none":
        developer = "Unknown"

    while True:
        try:
            year = input("Enter the release year (Enter None if data is unavailable): ").strip()
            if year.lower() == "none":
                year = "Unknown"
                break

            year = int(year)
            break

        except ValueError:
            print(f"{RED}Invalid input for release year.{RESET} Please enter a valid year.")

    while True:
        try:
            meta_score = input("Metacritic Score (Enter None if data is unavailable): ").strip()
            if meta_score.lower() == "none":
                meta_score = "N/A"
                break

            meta_score = int(meta_score)

            if 0 <= meta_score <= 100:
                break
            else:
                print(f"{RED}Metacritic Score must be between 0 and 100.{RESET}")

        except ValueError:
            print(f"{RED}Invalid input for Metacritic Score.{RESET} Please enter a valid Metacritic Score.")

    print("Enter genres (Enter None if data is unavailable or to stop)")
    c = 1
    genres_list = []
    while True:
        g = input(f"{c}) ")
        c += 1

        if g.lower() == "none":
            break
        g = g.strip()

        if g == "":
            print(f"{RED}Genre cannot be empty.{RESET}")
            continue
        try:
            int(g)
            print(f"{RED}Genres cannot be numbers!{RESET}")
            continue

        except ValueError:
            # add g to genres_list
            genres_list.append(g)

    while True:
        try:
            price = input("Enter the price (Enter None if data is unavailable): ").strip()
            if price.lower() == "none":
                price = "Unknown"
                break
            price = float(price)
            if price >= 0:
                break
            else:
                print(f"{RED}Price cannot be negative.{RESET}")

        except ValueError:
            print(f"{RED}Invalid input for price.{RESET} Please enter a valid price.")

    # Add the new game to the database
    games_database[title] = {
        "Developer": developer,
        "Year": year,
        "Metacritic": meta_score,
        "Genres": genres_list,
        "Price": price
    }

    # save database
    save_data(games_database, "games_database.json")
    print(f"{GREEN}Game added successfully!{RESET}")

# Main Menu Loop

# get data from database
data = load_data("games_database.json")
print(f"{'='*45}\n🎮 Welcome to the Video Game Recommender 🎮")
while True:
    # Display the main menu options
    print(f"{'='*45}\n1) Recommend a Game\n2) Find a Game\n3) Filter Database\n4) Add New Game\n5) Exit")
    print("="*45)
    userChoice = input("Please select an option (1-5): ").strip() # Prompt user for their choice

    # Execute the corresponding function based on user input
    if userChoice == "1":
        recommend_games(data)

    elif userChoice == "2":
        find_game(data)

    elif userChoice == "3":
        data_filter(data)

    elif userChoice == "4":
        insert_game(data)

    elif userChoice == "5":
        # Exit the loop
        print(f"{GREEN}Exiting the program.{RESET}\nThank you for using the Recommender System! Goodbye 👋")
        break

    else:
        print(f"{RED}Invalid choice.{RESET} Please enter a number between 1 and 5.") # Handle invalid input and prompt again
