import os
import requests
import pickle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PokemonDownloader:
    @staticmethod
    def download_pokemon_data():
        try:
            url = "https://pokeapi.co/api/v2/pokemon"
            pokemon_data = []
            while url:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    for pokemon in data["results"]:
                        pokemon_id = pokemon["url"].split("/")[-2]
                        pokemon_data.append({"id": pokemon_id, "name": pokemon["name"]})
                    url = data["next"]
                else:
                    logger.error("Error while downloading Pokémon data.")
                    return None
            return pokemon_data
        except Exception as e:
            logger.error("Error while downloading Pokémon data:", exc_info=True)
            return None

    @staticmethod
    def save_pokemon_data(pokemon_data, filename):
        with open(filename, "wb") as file:
            pickle.dump(pokemon_data, file)
        logger.info("Pokémon data saved successfully.")

    @staticmethod
    def load_pokemon_data(filename):
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                return pickle.load(file)
        else:
            return None

    @staticmethod
    def download_pokemon_image(image_url, filename):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                logger.info(f"Image downloaded: {filename}")
            else:
                logger.error(f"Failed to download image from {image_url}")
        except Exception as e:
            logger.error(f"Error while downloading image from {image_url}: {e}", exc_info=True)

def HandleData():
    # Path to store downloaded data
    db_folder = os.path.join(os.path.dirname(__file__), "../../db")
    os.makedirs(db_folder, exist_ok=True)
    pickle_path = os.path.join(db_folder, "pokemon_data.pickle")

    # Download Pokémon data if not already downloaded
    pokemon_data = PokemonDownloader.load_pokemon_data(pickle_path)
    if pokemon_data is None:
        pokemon_data = PokemonDownloader.download_pokemon_data()
        if pokemon_data:
            PokemonDownloader.save_pokemon_data(pokemon_data, pickle_path)
        else:
            logger.error("Cannot proceed without Pokémon data. Please check your internet connection and try again.")
            return

    # Path to store downloaded images
    image_folder = os.path.join(os.path.dirname(__file__), "../../images")
    os.makedirs(image_folder, exist_ok=True)

    # Download Pokémon images
    for pokemon in pokemon_data:
        pokemon_id = pokemon["id"]
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
        image_filename = os.path.join(image_folder, f"{pokemon_id}.png")
        PokemonDownloader.download_pokemon_image(image_url, image_filename)

if __name__ == "__main__":
    HandleData()
