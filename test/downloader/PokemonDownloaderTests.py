import os
import sys
import unittest
import json
import shutil

from unittest.mock import patch

test_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.abspath(os.path.join(test_dir, "..", ".."))
code_dir = module_dir + "/code/downloader"
sys.path.append(code_dir)

from PokemonDownloader import PokemonDownloader

class PokemonDownloaderTests(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for data
        self.temp_dir = os.path.join(os.path.dirname(__file__), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)

        # Mock web page content
        self.mock_data_with_next = {
            "results": [
                {"id": 1, "name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
                {"id": 2, "name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
                {"id": 4, "name": "charmander", "url": "https://pokeapi.co/api/v2/pokemon/4/"}
            ],
            "next": None  # Include next, ma vuoto
        }

        # Save the mock web page content to a temporary file
        self.mock_file_path_with_next = os.path.join(self.temp_dir, "mock_pokemon_data_with_next.json")
        with open(self.mock_file_path_with_next, "w") as file:
            file.write(json.dumps(self.mock_data_with_next))

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.temp_dir)

    @patch("PokemonDownloader.requests.get")
    def test_download_pokemon_data_with_next(self, mock_requests_get):
        # Mock the response of requests.get to return data with next
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = self.mock_data_with_next

        # Execute the method to download Pokémon data
        pokemon_data = PokemonDownloader.download_pokemon_data()

        # Extract the names and IDs from the mock data
        names_ids = [{"id": str(entry["id"]), "name": entry["name"]} for entry in self.mock_data_with_next["results"]]

        # Verify that the Pokémon data was downloaded correctly
        self.assertEqual(pokemon_data, names_ids)

if __name__ == "__main__":
    unittest.main()
