import requests
import time
import random

def pokemonRequest(pokemonToSearch):
    pokemonUrl = f"https://pokeapi.co/api/v2/pokemon/{pokemonToSearch}"
    pokemonResponse = requests.get(pokemonUrl)
    return pokemonResponse

def pokemonEncounterRequest(pokemonToSearch):
    encounterURL = f"https://pokeapi.co/api/v2/pokemon/{pokemonToSearch}/encounters"
    encounterResponse = requests.get(encounterURL)
    return encounterResponse

def print_pokemon_info(pokemon):
    print("Name:", pokemon["name"])
    print("Nª pokedex: #", pokemon["id"])
    print("\nTypes:")
    for type_info in pokemon["types"]:
        print(type_info["type"]["name"], end=" ")
    print("\nAbilities:")
    for ability_info in pokemon["abilities"]:
        print(ability_info["ability"]["name"], end=" ")

def search_pokemon(pokemonToSearch):
    pokemon_response = pokemonRequest(pokemonToSearch)

    if pokemon_response.status_code != 200:
        print("ERROR - Pokemon not found!")
        exit()

    pokemon = pokemon_response.json()
    print_pokemon_info(pokemon)

    encounter_response = pokemonEncounterRequest(pokemonToSearch)

    if encounter_response.status_code != 200:
        print("ERROR - Pokemon not found!")
        exit()

    encounters = encounter_response.json()
    print("\n\nEncounters:")
    for encounter in encounters:
        print(encounter["location_area"]["name"], end=" - ")
        games = encounter["version_details"]
        for game in games:
            print("Pokémon", game["version"]["name"], end=" ")
        print()

def random_pokemon():
    random_pokemon_id = random.randint(1, 1010)
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon_id}"
    pokemon_response = requests.get(pokemon_url)

    if pokemon_response.status_code != 200:
        print("ERROR - Pokemon not found!")
        exit()

    pokemon = pokemon_response.json()
    print("Name:", pokemon["name"])

    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{random_pokemon_id}"
    species_response = requests.get(species_url)

    if species_response.status_code != 200:
        print("ERROR - Pokemon not found!")
        exit()

    specie = species_response.json()
    print("Descriptions:")
    for entry in specie["flavor_text_entries"]:
        lang = entry["language"]["name"]
        if lang == "en":
            print("- " + entry["flavor_text"], end=" - ")
            print(entry["version"]["name"])

def export_pokemon(pokemonToSearch):
    pokemon_response = pokemonRequest(pokemonToSearch)

    if pokemon_response.status_code != 200:
        print("ERROR - Pokemon not found!")
        exit()

    pokemon = pokemon_response.json()
    file_name = f"{pokemon['name']}.txt"

    with open(file_name, "w") as file:
        file.write(f"Name: {pokemon['name']}")
        file.write(f"\nNª pokedex: #{pokemon['id']}")
        file.write("\n\nTypes: ")
        for type_info in pokemon["types"]:
            file.write(type_info["type"]["name"])
        file.write("\nAbilities: ")
        for ability_info in pokemon["abilities"]:
            file.write(ability_info["ability"]["name"])

        encounter_response = pokemonEncounterRequest(pokemonToSearch)

        if encounter_response.status_code != 200:
            print("ERROR - Pokemon not found!")
            return

        encounters = encounter_response.json()
        file.write("\n\nEncounters: ")
        for encounter in encounters:
            file.write(encounter["location_area"]["name"] + " - ")
            games = encounter["version_details"]
            for game in games:
                file.write("Pokémon " + game["version"]["name"] + " ")
    return f"You have exported the file \"{file_name}\""

def import_and_read_file(file_to_read):
    try:
        with open(f"{file_to_read}.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                print(line, end="")
            print()
    except FileNotFoundError:
        print("The file does not exist.\n")

# Menú principal
while True:
    print("------------------------------------")
    print("---         PokeAPI MENU         ---")
    print("------------------------------------")
    print("- Options: ")
    print("1. Search Pokémon")
    print("2. See description of a random pokemon")
    print("3. Import and read pokemon file (\"*.txt\")")
    print("4. Exit")
    option = input("Select an option: ")
    if option == "1":
        pokemonToSearch = input("Search pokemon info: ")
        search_pokemon(pokemonToSearch)
        while True:
            otherSearch = input("Do you want to find another pokemon (y/N)? ").lower()
            if otherSearch == "y":
                pokemonToSearch = input("Search pokemon info: ")
                search_pokemon(pokemonToSearch)
            elif otherSearch == "n":
                while True:
                    otherSearch = input("Do you want to export the information in a \".txt\" file? (y/N)? ").lower()
                    if otherSearch == "y":
                        print(export_pokemon(pokemonToSearch))
                        break
                    elif otherSearch == "n":
                        print("Return to the menu")
                        break
                    else:
                        print("ERROR - This option does not exist")
                break
            else:
                print("ERROR - This option does not exist")
        time.sleep(2)
    elif option == "2":
        random_pokemon()
        while True:
            otherSearch = input("Do you want to see another pokemon (y/N)? ").lower()
            if otherSearch == "y":
                random_pokemon()
            elif otherSearch == "n":
                print("Return to the menu")
                break
            else:
                print("This option does not exist")
        time.sleep(2)
    elif option == "3":
        fileToRead = input("Write the name of the file you want to read (only \".txt\" format, no need to write): ")
        import_and_read_file(fileToRead)
        time.sleep(2)
    elif option == "4":
        print("You have successfully exited!")
        break
    else:
        print("ERROR - This option does not exist")
