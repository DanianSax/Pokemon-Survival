import random
from os import system
from time import sleep

from pokeloads import get_all_pokemons
CHILLING_TIME = 1
BAR_MULTIPLIER = 20

# Tabla de Evoluciones
evolution_chart = {
    "Bulbasaur": {"evolution": "Ivysaur", "evolution_level": 16},
    "Ivysaur": {"evolution": "Venusaur", "evolution_level": 32},
    "Charmander": {"evolution": "Charmeleon", "evolution_level": 16},
    "Charmeleon": {"evolution": "Charizard", "evolution_level": 36},
    "Squirtle": {"evolution": "Wartortle", "evolution_level": 16},
    "Wartortle": {"evolution": "Blastoise", "evolution_level": 36},
    "Caterpie": {"evolution": "Metapod", "evolution_level": 7},
    "Metapod": {"evolution": "Butterfree", "evolution_level": 10},
    "Weedle": {"evolution": "Kakuna", "evolution_level": 7},
    "Kakuna": {"evolution": "Beedrill", "evolution_level": 10},
    "Pidgey": {"evolution": "Pidgeotto", "evolution_level": 18},
    "Pidgeotto": {"evolution": "Pidgeot", "evolution_level": 36},
    "Rattata": {"evolution": "Raticate", "evolution_level": 20},
    "Spearow": {"evolution": "Fearow", "evolution_level": 20},
    "Ekans": {"evolution": "Arbok", "evolution_level": 22},
    "Pikachu": {"evolution": "Raichu", "evolution_level": 25},
    "Sandshrew": {"evolution": "Sandslash", "evolution_level": 22},
    "Nidoran♀": {"evolution": "Nidorina", "evolution_level": 16},
    "Nidorina": {"evolution": "Nidoqueen", "evolution_level": 32},
    "Nidoran♂": {"evolution": "Nidorino", "evolution_level": 16},
    "Nidorino": {"evolution": "Nidoking", "evolution_level": 32},
    "Clefairy": {"evolution": "Clefable", "evolution_level": 25},
    "Vulpix": {"evolution": "Ninetales", "evolution_level": 25},
    "Jigglypuff": {"evolution": "Wigglytuff", "evolution_level": 25},
    "Zubat": {"evolution": "Golbat", "evolution_level": 22},
    "Oddish": {"evolution": "Gloom", "evolution_level": 21},
    "Gloom": {"evolution": "Vileplume", "evolution_level": 35},
    "Paras": {"evolution": "Parasect", "evolution_level": 24},
    "Venonat": {"evolution": "Venomoth", "evolution_level": 31},
    "Diglett": {"evolution": "Dugtrio", "evolution_level": 26},
    "Meowth": {"evolution": "Persian", "evolution_level": 28},
    "Psyduck": {"evolution": "Golduck", "evolution_level": 33},
    "Mankey": {"evolution": "Primeape", "evolution_level": 28},
    "Growlithe": {"evolution": "Arcanine", "evolution_level": 25},
    "Poliwag": {"evolution": "Poliwhirl", "evolution_level": 25},
    "Poliwhirl": {"evolution": "Poliwrath", "evolution_level": 35},
    "Abra": {"evolution": "Kadabra", "evolution_level": 16},
    "Kadabra": {"evolution": "Alakazam", "evolution_level": 32},
    "Machop": {"evolution": "Machoke", "evolution_level": 28},
    "Machoke": {"evolution": "Machamp", "evolution_level": 40},
    "Bellsprout": {"evolution": "Weepinbell", "evolution_level": 21},
    "Weepinbell": {"evolution": "Victreebel", "evolution_level": 35},
    "Tentacool": {"evolution": "Tentacruel", "evolution_level": 30},
    "Geodude": {"evolution": "Graveler", "evolution_level": 25},
    "Graveler": {"evolution": "Golem", "evolution_level": 35},
    "Ponyta": {"evolution": "Rapidash", "evolution_level": 40},
    "Slowpoke": {"evolution": "Slowbro", "evolution_level": 37},
    "Magnemite": {"evolution": "Magneton", "evolution_level": 30},
    "Doduo": {"evolution": "Dodrio", "evolution_level": 31},
    "Seel": {"evolution": "Dewgong", "evolution_level": 34},
    "Grimer": {"evolution": "Muk", "evolution_level": 38},
    "Shellder": {"evolution": "Cloyster", "evolution_level": 25},
    "Gastly": {"evolution": "Haunter", "evolution_level": 25},
    "Haunter": {"evolution": "Gengar", "evolution_level": 35},
    "Drowzee": {"evolution": "Hypno", "evolution_level": 26},
    "Krabby": {"evolution": "Kingler", "evolution_level": 28},
    "Voltorb": {"evolution": "Electrode", "evolution_level": 30},
    "Exeggcute": {"evolution": "Exeggutor", "evolution_level": 30},
    "Cubone": {"evolution": "Marowak", "evolution_level": 28},
    "Koffing": {"evolution": "Weezing", "evolution_level": 35},
    "Rhyhorn": {"evolution": "Rhydon", "evolution_level": 42},
    "Horsea": {"evolution": "Seadra", "evolution_level": 32},
    "Goldeen": {"evolution": "Seaking", "evolution_level": 33},
    "Staryu": {"evolution": "Starmie", "evolution_level": 25},
    "Magikarp": {"evolution": "Gyarados", "evolution_level": 20},
    "Eevee": {"evolution": ["Vaporeon", "Jolteon", "Flareon"], "evolution_level": 20},
    "Omanyte": {"evolution": "Omastar", "evolution_level": 40},
    "Kabuto": {"evolution": "Kabutops", "evolution_level": 40},
    "Dratini": {"evolution": "Dragonair", "evolution_level": 30},
    "Dragonair": {"evolution": "Dragonite", "evolution_level": 55}
}

# Tabla de tipos
type_chart = {
    "normal": {"Fuerte contra": [], "Débil contra": ["lucha"]},
    "fuego": {"Fuerte contra": ["planta", "hielo"], "Débil contra": ["agua", "roca"]},
    "agua": {"Fuerte contra": ["fuego", "roca"], "Débil contra": ["planta", "electrico"]},
    "planta": {"Fuerte contra": ["agua", "roca"], "Débil contra": ["fuego", "hielo"]},
    "electrico": {"Fuerte contra": ["agua", "volador"], "Débil contra": ["tierra"]},
    "hielo": {"Fuerte contra": ["planta", "tierra", "volador", "Dragón"], "Débil contra": ["fuego", "lucha", "roca"]},
    "lucha": {"Fuerte contra": ["normal", "hielo", "roca", "acero", "siniestro"], "Débil contra": ["volador",
                                                                                                   "psíquico", "hada"]},
    "roca": {"Fuerte contra": ["fuego", "hielo", "volador", "bicho"], "Débil contra": ["agua", "planta", "lucha",
                                                                                       "tierra"]},
    "tierra": {"Fuerte contra": ["fuego", "electrico", "roca", "acero", "veneno"], "Débil contra": ["agua", "hielo",
                                                                                                    "planta"]},
    "volador": {"Fuerte contra": ["planta", "lucha", "bicho"], "Débil contra": ["electrico", "hielo", "roca"]},
    "bicho": {"Fuerte contra": ["planta", "psíquico", "siniestro"], "Débil contra": ["fuego", "volador", "roca"]},
    "veneno": {"Fuerte contra": ["planta", "hada"], "Débil contra": ["tierra", "psíquico"]},
    "psíquico": {"Fuerte contra": ["lucha", "venenoso"], "Débil contra": ["bicho", "fantasma", "siniestro"]},
    "fantasma": {"Fuerte contra": ["psíquico", "fantasma"], "Débil contra": ["normal", "siniestro"]},
    "siniestro": {"Fuerte contra": ["psíquico", "fantasma"], "Débil contra": ["lucha", "bicho", "hada"]},
    "acero": {"Fuerte contra": ["roca", "hielo", "hada"], "Débil contra": ["fuego", "lucha", "tierra"]},
}


def get_player_profile(pokemon_list):
    return {
        "player_name": input("\nCual es tu nombre?: \n"),
        "pokemon_inventory": [dict(random.choice(pokemon_list)) for a in range(3)],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0
    }


def get_pokemon_info(pokemon):
    return "{} | lvl {} | HP {}/{} | XP {}/20".format(pokemon["name"],
                                                      pokemon["level"],
                                                      pokemon["current_health"],
                                                      pokemon["base_health"],
                                                      pokemon["current_exp"])


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def enemy_match_player(enemy_pokemon, player_profile):
    enemy_pokemon["level"] = player_pokemon_toplvl(player_profile)
    enemy_pokemon["base_health"] += 20 * (enemy_pokemon["level"] - 1)
    enemy_pokemon["current_health"] = enemy_pokemon["base_health"]


def fight(player_profile, enemy_pokemon, pokemon_list):
    print("\n--- NUEVO COMBATE ---")
    sleep(CHILLING_TIME)
    print("Combates realizado: {}\n".format(player_profile["combats"]))
    sleep(CHILLING_TIME)
    attack_history = []
    print("Proximo contrincante:\n{}\n".format(get_pokemon_info(enemy_pokemon)))
    sleep(CHILLING_TIME)
    player_pokemon = change_pokemon(player_profile)
    still_in_combat = True
    print("\n{} VS {}\n".format(get_pokemon_info(player_pokemon), get_pokemon_info(enemy_pokemon)))
    sleep(CHILLING_TIME)
    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        if not still_in_combat:
            break
        # Player Turn:
        action = None
        while action not in ["A", "P", "V", "C"]:
            action = input("Que deseas hacer: [A]tacar, [P]okeball({}), Pocion de [V]ida ({}), [C]ambiar\n"
                           .format(player_profile["pokeballs"], player_profile["health_potion"]))
            if action.lower() == "a":
                still_in_combat = player_attack(player_pokemon, enemy_pokemon)
                attack_history.append(player_pokemon)
            elif action.lower() == "p":
                still_in_combat = capture_with_pokeball(player_profile, enemy_pokemon)
            elif action.lower() == "v":
                cure_pokemon(player_profile)
                still_in_combat = True
            elif action.lower() == "c":
                player_pokemon = change_pokemon(player_profile)
                still_in_combat = True

            if not still_in_combat:
                break

            # Enemys Turn:
            still_in_combat = enemy_turn(player_pokemon, enemy_pokemon)

            if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
                player_pokemon = change_pokemon(player_profile)
                still_in_combat = True

            if not still_in_combat:
                break

    if enemy_pokemon["current_health"] == 0:
        assing_exp(attack_history, player_profile, pokemon_list)
        item_lotery(player_profile)
        player_profile["combats"] += 1

    if player_profile["health_potion"] > 0 and any_player_pokemon_lives(player_profile):
        cure = input("\nQuieres curar algun pokemon antes de la siguiente ronda? [S/N]\n")
        if cure.lower() == "s":
            cure_pokemon(player_profile)
    input("[ENTER] para continuar...")
    system("cls")


def change_pokemon(player_profile):
    while True:
        print("Elige con que pokemon lucharas")
        sleep(CHILLING_TIME)
        chosen_pokemon = choose_pokemon(player_profile)
        if chosen_pokemon["current_health"] > 0:
            return chosen_pokemon
        else:
            print("No puedes elegir un pokemon con 0 de vida! Elige otro.")
            sleep(CHILLING_TIME)


def player_attack(player_pokemon, enemy_pokemon):
    available_attacks = [attack for attack in player_pokemon["attacks"]
                         if attack["min_level"] and int(attack["min_level"]) <= player_pokemon["level"]]
    if len(available_attacks) > 0:
        for idx, attack in enumerate(available_attacks):
            print("{}. {} - {} (Dmg: {})".format(idx + 1, attack["name"], attack["type"], attack["damage"]))

        chosen_attack_idx = None
        while chosen_attack_idx not in range(1, len(available_attacks) + 1):
            try:
                chosen_attack_idx = int(input("Elige el numero del ataque: "))
            except ValueError:
                print("Opcion no valida. Ingresa un numero valido.")
                sleep(CHILLING_TIME)

        chosen_attack = available_attacks[chosen_attack_idx - 1]
        modifier = calculate_final_modifier(chosen_attack["type"], enemy_pokemon["type"], player_pokemon["type"])

        damage_dealt = int(chosen_attack["damage"] * modifier)

        enemy_pokemon["current_health"] -= damage_dealt

        print("{} usó {} y causo {} puntos de daño...".format(player_pokemon["name"], chosen_attack["name"],
                                                              damage_dealt))
        sleep(CHILLING_TIME)
        health_no_below_zero(player_pokemon, enemy_pokemon)
        show_health_bars(player_pokemon, enemy_pokemon)

        if enemy_pokemon["current_health"] <= 0:
            print("{} se ha debilitado.".format(enemy_pokemon["name"]))
            sleep(CHILLING_TIME)
            return False
        else:
            return True
    else:
        print("No dispones de ataques para realizar")
        sleep(CHILLING_TIME)
        return True


def calculate_modifier(attack_type, target_type):
    if attack_type in type_chart:
        for t in target_type:
            if t in type_chart[attack_type]["Fuerte contra"]:
                return 2.0
            if t in type_chart[attack_type]["Débil contra"]:
                return 0.5
        else:
            return 1.0


def calculate_stab_modifier(attack_type, pokemon_type):
    if attack_type in pokemon_type:
        return 1.5
    else:
        return 1.0


def calculate_final_modifier(attack_type, target_type, pokemon_type):
    type_modifier = calculate_modifier(attack_type, target_type)
    stab_modifier = calculate_stab_modifier(attack_type, pokemon_type)
    if type_modifier is None:
        type_modifier = 1
    if stab_modifier is None:
        stab_modifier = 1
    return type_modifier * stab_modifier


def health_no_below_zero(player_pokemon, enemy_pokemon):
    if player_pokemon["current_health"] < 0:
        player_pokemon["current_health"] = 0
    if enemy_pokemon["current_health"] < 0:
        enemy_pokemon["current_health"] = 0


def show_health_bars(player_pokemon, enemy_pokemon):
    player_health_percentage = player_pokemon["current_health"] / player_pokemon["base_health"]
    enemy_health_percentage = enemy_pokemon["current_health"] / enemy_pokemon["base_health"]
    print("\n{}: |{}| {}/{} HP".format(player_pokemon["name"],
                                       "#" * int((BAR_MULTIPLIER * player_health_percentage)),
                                       player_pokemon["current_health"], player_pokemon["base_health"]))
    print("{}: |{}| {}/{} HP\n".format(enemy_pokemon["name"],
                                       "#" * int((BAR_MULTIPLIER * enemy_health_percentage)),
                                       enemy_pokemon["current_health"], enemy_pokemon["base_health"]))
    sleep(CHILLING_TIME)


def all_player_pokemon_full_health(player_profile):
    return (sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]])
            == sum([pokemon["base_health"] for pokemon in player_profile["pokemon_inventory"]]))


def enemy_turn(player_pokemon, enemy_pokemon):
    print("Turno de {}\n".format(enemy_pokemon["name"]))
    sleep(CHILLING_TIME)
    available_attacks = [attack for attack in enemy_pokemon["attacks"]
                         if int(attack["min_level"]) <= enemy_pokemon["level"]]
    if available_attacks:
        enemy_action = random.choice(available_attacks)

        modifier = calculate_final_modifier(enemy_action["type"], player_pokemon["type"], enemy_pokemon["type"])

        damage_dealt = int(enemy_action["damage"] * modifier)

        player_pokemon["current_health"] -= damage_dealt

        print("{} usó {} y causo {} puntos de daño.".format(enemy_pokemon["name"], enemy_action["name"],
                                                            damage_dealt))
        sleep(CHILLING_TIME)

        health_no_below_zero(player_pokemon, enemy_pokemon)
        show_health_bars(player_pokemon, enemy_pokemon)

        if player_pokemon["current_health"] <= 0:
            print("\n{} se ha debilitado.\n".format(player_pokemon["name"]))
            sleep(CHILLING_TIME)
            return False
        else:
            return True
    else:
        print("\n{} no puede atacar porque no tiene ataques disponibles con su nivel.\n".format(enemy_pokemon["name"]))
        sleep(CHILLING_TIME)
        return True


def choose_pokemon(player_profile):
    for index in range(len(player_profile["pokemon_inventory"])):
        print("{} - {}".format(index, get_pokemon_info(player_profile["pokemon_inventory"][index])))
    while True:
        try:
            chosen_pokemon = player_profile["pokemon_inventory"][int(input("Cual eliges? "))]
            return chosen_pokemon
        except (ValueError, IndexError, TypeError):
            print("Opcion invalida")
            sleep(CHILLING_TIME)


def pokemon_level_up(pokemon, player_profile, pokemon_list):
    pokemon["current_exp"] -= 20
    pokemon["level"] += 1
    pokemon["base_health"] += 5
    pokemon["current_health"] = pokemon["base_health"]
    print("{} ha subido de nivel".format(pokemon["name"]))
    evolve_pokemon(player_profile, pokemon, pokemon_list)


def evolve_pokemon(player_profile, pokemon, pokemon_list):
    sleep(CHILLING_TIME)
    evolved_pokemon = pokemon
    if pokemon["name"] in evolution_chart:
        evolution_info = evolution_chart[pokemon["name"]]
        if pokemon["level"] >= evolution_info["evolution_level"]:
            print("Anda, parece que tu {} quiere evolucionar...".format(pokemon["name"]))
            sleep(CHILLING_TIME)
            if pokemon["name"] != "Eevee":
                for a in pokemon_list:
                    if a["name"] == evolution_info["evolution"]:
                        print("Felicidades! Tu {} ha evolucionado a un {}...".format(pokemon["name"], a["name"]))
                        sleep(CHILLING_TIME)
                        evolved_pokemon = dict(a)
                        evolved_pokemon["level"] = pokemon["level"]
                        evolved_pokemon["current_exp"] = pokemon["current_exp"]
                        evolved_pokemon["base_health"] = pokemon["base_health"]
                        evolved_pokemon["current_health"] = pokemon["current_health"]
            else:
                wich_eevee_evol = random.choice(evolution_info["evolution"])
                for a in pokemon_list:
                    if a["name"] == wich_eevee_evol:
                        print("Felicidades! Tu {} ha evolucionado a un {}...".format(pokemon, a))
                        sleep(CHILLING_TIME)
                        evolved_pokemon = dict(a)
                        evolved_pokemon["level"] = pokemon["level"]
                        evolved_pokemon["current_exp"] = pokemon["current_exp"]
                        evolved_pokemon["base_health"] = pokemon["base_health"]
                        evolved_pokemon["current_health"] = pokemon["current_health"]

        index = player_profile["pokemon_inventory"].index(pokemon)
        player_profile["pokemon_inventory"][index] = evolved_pokemon


def assing_exp(attack_history, player_profile, pokemon_list):
    for pokemon in attack_history:
        if pokemon["current_health"] > 0:
            points = random.randint(1, 5)
            pokemon["current_exp"] += points
            print("Tu {} ha ganado {} de xp".format(pokemon["name"], points))
    points = random.randint(10, 20)
    for pokemon in player_profile["pokemon_inventory"]:
        if pokemon["current_health"] > 0:
            pokemon["current_exp"] += points
            print("Tu {} ha ganado {} del repartir xp".format(pokemon["name"], points))
            while pokemon["current_exp"] >= 20:
                pokemon_level_up(pokemon, player_profile, pokemon_list)


def capture_with_pokeball(player_profile, enemy_pokemon):
    if player_profile["pokeballs"] > 0:
        player_profile["pokeballs"] -= 1
        capture_change = 40 + (enemy_pokemon["current_health"] / enemy_pokemon["base_health"]) * 60
        enemy_caught_try = random.randint(1, 100)
        if enemy_caught_try >= capture_change:
            player_profile["pokemon_inventory"].append(enemy_pokemon)
            print("{} atrapado con exito!".format(enemy_pokemon["name"]))
            sleep(CHILLING_TIME)
            return False
        else:
            print("Ufff por poco lo logras...\n")
            sleep(CHILLING_TIME)
            return True
    else:
        print("No te quedaban pokeballs, pierdes el turno por no estar atento...")
        sleep(CHILLING_TIME)
        return True


def cure_pokemon(player_profile):
    if player_profile["health_potion"] > 0:
        if not all_player_pokemon_full_health(player_profile):
            while True:
                print("Elige que pokemon quieres curar:")
                sleep(CHILLING_TIME)
                chosen_pokemon = choose_pokemon(player_profile)
                if chosen_pokemon["current_health"] < chosen_pokemon["base_health"]:
                    chosen_pokemon["current_health"] += 50
                    if chosen_pokemon["current_health"] > chosen_pokemon["base_health"]:
                        chosen_pokemon["current_health"] = chosen_pokemon["base_health"]
                    player_profile["health_potion"] -= 1
                    print("Has usado una pocion!"
                          "\nTu {} ha recuperado 50 pts de salud...".format(chosen_pokemon["name"]))
                    sleep(CHILLING_TIME)
                    break
                else:
                    print("Tu {} no esta herido. Elige otro pokemon.".format(chosen_pokemon["name"]))
                    sleep(CHILLING_TIME)
                    if all_player_pokemon_full_health(player_profile):
                        break
        else:
            print("No tienes ningun pokemon herido...")
            sleep(CHILLING_TIME)
            return
    else:
        print("No te quedaban pociones, pierdes el turno por no estar atento...")
        sleep(CHILLING_TIME)
        return


def next_round_timer(time):
    print("\nContinuamos con la siguiente ronda en...")
    for i in range(time, 0, -1):
        print("{}...".format(i))
        sleep(CHILLING_TIME)


def player_pokemon_toplvl(player_profile):
    top_lvl = player_profile["pokemon_inventory"][0]["level"]
    for pokemon in player_profile["pokemon_inventory"]:
        if int(pokemon["level"]) > int(top_lvl):
            top_lvl = pokemon["level"]
    return top_lvl


def item_lotery(player_profile):
    item = random.randint(1, 2)
    if item == 1:
        player_profile["pokeballs"] += 1
        print("\n-Has ganado una pokeball-\n")
        sleep(CHILLING_TIME)
    elif item == 2:
        player_profile["health_potion"] += 1
        print("\n-Has ganado una pocion-\n")
        sleep(CHILLING_TIME)


def main():
    system("cls")
    print("""
 ____   ___   __  _    ___  ___ ___   ___   ____        _____ __ __  ____  __ __  ____  __ __   ___   ____  
|    \ /   \ |  |/ ]  /  _]|   |   | /   \ |    \      / ___/|  |  ||    \|  |  ||    ||  |  | /   \ |    \ 
|  o  )     ||  ' /  /  [_ | _   _ ||     ||  _  |    (   \_ |  |  ||  D  )  |  | |  | |  |  ||     ||  D  )
|   _/|  O  ||    \ |    _]|  \_/  ||  O  ||  |  |     \__  ||  |  ||    /|  |  | |  | |  |  ||  O  ||    / 
|  |  |     ||     \|   [_ |   |   ||     ||  |  |     /  \ ||  :  ||    \|  :  | |  | |  :  ||     ||    \ 
|  |  |     ||  .  ||     ||   |   ||     ||  |  |     \    ||     ||  .  \\\\   /  |  |  \   / |     ||  .  \\
|__|   \___/ |__|\_||_____||___|___| \___/ |__|__|      \___| \__,_||__|\_| \_/  |____|  \_/   \___/ |__|\_|
    """)
    pokemon_list = get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)
    print("Bienvenido {}!\n"
          "Veamos que tal lejos llegas...\n"
          "Estos seran tus pokemons para la partida:".format(player_profile["player_name"]))
    for a in player_profile["pokemon_inventory"]:
        print("- {}".format(get_pokemon_info(a)))
    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = dict(random.choice(pokemon_list))
        enemy_match_player(enemy_pokemon, player_profile)
        fight(player_profile, enemy_pokemon, pokemon_list)

    print("\nFelicidades {}!\nHas perdido en el combate #{}".format(player_profile["player_name"],
                                                                    player_profile["combats"]))
    input("[ENTER] para finalizar...")


if __name__ == "__main__":
    main()
