import requests
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_info() function
    poke_info = get_pokemon_info("Rockruff")
    download_pokemon_artwork("Pikachu", r"C:\Users\Admin\Documents\Lab 10 Script Templates")
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    pokemon = str(pokemon).strip().lower()

    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def get_pokemon_nameslist(max_pokemonlimit):
    """Gets a list of Pokémon names from the PokeAPI.

    Args:
        max_pokemonlimit (int): The maximum number of Pokémon to retrieve.

    Returns:
        list: List of Pokémon names.
    """
    api_url = f"https://pokeapi.co/api/v2/pokemon?limit={max_pokemonlimit}"
    api_response = requests.get(api_url)
    response_data = api_response.json()
    pokemon_names = [pokemon['name'] for pokemon in response_data['results']]
    return pokemon_names

def download_pokemon_artwork(pokemon_name, save_directory):
    """Downloads and saves the artwork for the specified Pokémon.

    Args:
        pokemon_name (str): The name of the Pokémon.
        save_directory (str): The directory where the artwork should be saved.

    Returns:
        str: The file path where the artwork is saved, or None if failed.
    """
    pokemon_data = get_pokemon_info(pokemon_name)
    if not pokemon_data:
        print(f"Failed to get data for {pokemon_name}")
        return None

    artwork_url = pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
    
    if not artwork_url:
        print(f"No artwork available for {pokemon_name}")
        return None

    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        print(f"Directory does not exist: {save_directory}")
        return None

    file_path = os.path.join(save_directory, f"{pokemon_name.capitalize()}.jpg")

    # Download and save the artwork
    response = requests.get(artwork_url)
    if response.status_code == requests.codes.ok:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Artwork saved to {file_path}")
        return file_path
    else:
        print(f"Failed to download artwork: {response.status_code}")
        return None

if __name__ == '__main__':
    main()
