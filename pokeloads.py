import pickle
from pprint import pprint
from time import sleep

from requests_html import HTMLSession

# Base
base_health = 100
pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": None,
    "current_exp": 0,
    "attacks": None
}

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="

# Extraer datos pokemon


def get_pokemon(index):
    # Url y session
    url = "{}{}". format(URL_BASE, index)
    session = HTMLSession()
    pokemon_page = session.get(url)

    new_pokemon = pokemon_base.copy()

    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text.split("\n")[0]
    new_pokemon["type"] = []

    for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        new_pokemon["type"].append(img.attrs["alt"])

    new_pokemon["attacks"] = []

    for attack_item in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        if int(attack_item.find("td")[3].text.replace("--", "0")) != 0:
            if len(attack_item.find("th")[1].text) > 0:
                attack = {
                    "name": attack_item.find("td", first=True).find("a", first=True).text,
                    "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
                    "min_level": attack_item.find("th")[1].text,
                    "damage": int(attack_item.find("td")[3].text.replace("--", "0"))
                }
                new_pokemon["attacks"].append(attack)
            else:
                attack = {
                    "name": attack_item.find("td", first=True).find("a", first=True).text,
                    "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
                    "min_level": 1,
                    "damage": int(attack_item.find("td")[3].text.replace("--", "0"))
                }
                new_pokemon["attacks"].append(attack)
    return new_pokemon

# Leer o generar archivo con los datos  de todos los pokemones


def get_all_pokemons():
    try:
        print("Cargando el Pokefile..")
        with open("pokefile.pkl", "rb") as pokefile:
            all_pokemons = pickle.load(pokefile)
            sleep(3)
    except FileNotFoundError:
        print("Archivo no encontrado! Generando Pokefile nuevo.")
        all_pokemons = []
        for index in range(151):
            all_pokemons.append(get_pokemon(index+1))
            print("{} ha sido encontrado!".format(get_pokemon(index+1)["name"]))
        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemons, pokefile)
            print("\nTodos los pokemons han sido descargados!")
    print("Lista de Pokemons cargada")
    return all_pokemons

# Main


def main():
    pokemons = get_all_pokemons()
    pprint(pokemons)


if __name__ == "__main__":
    main()
