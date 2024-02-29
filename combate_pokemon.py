import random
from pprint import pprint
from pokeloads import get_all_pokemons

BAR_MULTIPLIER = 10

type_chart = {
    "normal": {"Fuerte contra": [], "Débil contra": ["lucha"]},
    "fuego": {"Fuerte contra": ["planta", "hielo"], "Débil contra": ["agua", "roca"]},
    "agua": {"Fuerte contra": ["fuego", "roca"], "Débil contra": ["planta", "eléctrico"]},
    "planta": {"Fuerte contra": ["agua", "roca"], "Débil contra": ["fuego", "hielo"]},
    "eléctrico": {"Fuerte contra": ["agua"], "Débil contra": ["tierra"]},
    "hielo": {"Fuerte contra": ["planta", "tierra", "volador", "Dragón"], "Débil contra": ["fuego", "lucha", "roca"]},
    "lucha": {"Fuerte contra": ["normal", "hielo", "roca", "acero", "siniestro"], "Débil contra": ["volador",
                                                                                                   "psíquico", "hada"]},
    "roca": {"Fuerte contra": ["fuego", "hielo", "volador", "bicho"], "Débil contra": ["agua", "planta", "lucha",
                                                                                       "tierra"]},
    "tierra": {"Fuerte contra": ["fuego", "eléctrico", "roca", "acero", "veneno"], "Débil contra": ["agua", "hielo",
                                                                                                    "planta"]},
    "volador": {"Fuerte contra": ["planta", "lucha", "bicho"], "Débil contra": ["eléctrico", "hielo", "roca"]},
    "bicho": {"Fuerte contra": ["planta", "psíquico", "siniestro"], "Débil contra": ["fuego", "volador", "roca"]},
    "veneno": {"Fuerte contra": ["planta", "hada"], "Débil contra": ["tierra", "psíquico"]},
    "psíquico": {"Fuerte contra": ["lucha", "venenoso"], "Débil contra": ["bicho", "fantasma", "siniestro"]},
    "fantasma": {"Fuerte contra": ["psíquico", "fantasma"], "Débil contra": ["normal", "siniestro"]},
    "siniestro": {"Fuerte contra": ["psíquico", "fantasma"], "Débil contra": ["lucha", "bicho", "hada"]},
    "acero": {"Fuerte contra": ["roca", "hielo", "hada"], "Débil contra": ["fuego", "lucha", "tierra"]},
}


def calculate_modifier(attack_type, target_type):
    if attack_type in type_chart and target_type in type_chart[attack_type]["Fuerte contra"]:
        return 2.0
    elif attack_type in type_chart and target_type in type_chart[attack_type]["Débil contra"]:
        return 0.5
    else:
        return 1.0


def health_no_below_zero(player_pokemon, enemy_pokemon):
    if player_pokemon["current_health"] < 0:
        player_pokemon["current_health"] = 0
    if enemy_pokemon["current_health"] < 0:
        enemy_pokemon["current_health"] = 0


def get_player_profile(pokemon_list):
    return {
        "player_name": input("Cual es tu nombre?: \n"),
        "pokemon_inventory": [random.choice(pokemon_list) for a in range(3)],
        "combats": 0,
        "pokeballs": 10,
        "health_potion": 10
    }


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def get_pokemon_info(pokemon):
    return "{} | lvl {} | hp {}/{}".format(pokemon["name"],
                                           pokemon["level"],
                                           pokemon["current_health"],
                                           pokemon["base_health"])


def show_health_bars(player_pokemon, enemy_pokemon):
    player_health_percentage = player_pokemon["current_health"] / player_pokemon["base_health"]
    enemy_health_percentage = enemy_pokemon["current_health"] / enemy_pokemon["base_health"]
    print("\n{}: |{}| {}/{} HP".format(player_pokemon["name"],
                                       "#" * int((BAR_MULTIPLIER * player_health_percentage)),
                                       player_pokemon["current_health"], player_pokemon["base_health"]))
    print("{}: |{}| {}/{} HP\n".format(enemy_pokemon["name"],
                                       "#" * int((BAR_MULTIPLIER * enemy_health_percentage)),
                                       enemy_pokemon["current_health"], enemy_pokemon["base_health"]))


def enemy_turn(player_pokemon, enemy_pokemon, player_profile):
    print("Turno de {}".format(enemy_pokemon["name"]))
    available_attacks = [attack for attack in enemy_pokemon["attacks"]
                         if int(attack["min_level"]) <= enemy_pokemon["level"]]
    if available_attacks:
        enemy_action = random.choice(available_attacks)

        modifier = calculate_modifier(enemy_action["type"], player_pokemon["type"])

        if enemy_action["type"] == player_pokemon["type"]:
            modifier *= 1.5

        damage_dealt = int(enemy_action["damage"] * modifier)
        # Print de control
        print("Daño sin modifier {}\n"
              "Modificador {}\n"
              "Daño final {}".format(enemy_action["damage"], modifier, damage_dealt))

        player_pokemon["current_health"] -= damage_dealt

        print("{} usó {} y causo {} puntos de daño...".format(enemy_pokemon["name"], enemy_action["name"],
                                                              damage_dealt))

        health_no_below_zero(player_pokemon, enemy_pokemon)
        show_health_bars(player_pokemon, enemy_pokemon)

        if player_pokemon["current_health"] <= 0:
            print("{} se ha debilitado.".format(player_pokemon["name"]))
            player_pokemon = choose_pokemon(player_profile)
            return False
        else:
            return True
    else:
        print("{} no puede atacar porque no tiene ataques disponibles con su nivel.".format(enemy_pokemon["name"]))


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

        chosen_attack = available_attacks[chosen_attack_idx - 1]
        modifier = calculate_modifier(chosen_attack["type"], enemy_pokemon["type"])

        if chosen_attack["type"] == player_pokemon["type"]:
            modifier *= 1.5

        damage_dealt = int(chosen_attack["damage"] * modifier)
        # Print de control
        print("Daño sin modifier {}\n"
              "Modificador {}\n"
              "Daño final {}".format(chosen_attack["damage"], modifier, damage_dealt))

        enemy_pokemon["current_health"] -= damage_dealt

        print("{} usó {} y causo {} puntos de daño...".format(player_pokemon["name"], chosen_attack["name"],
                                                              damage_dealt))
        health_no_below_zero(player_pokemon, enemy_pokemon)
        show_health_bars(player_pokemon, enemy_pokemon)

        if enemy_pokemon["current_health"] <= 0:
            print("{} se ha debilitado.".format(enemy_pokemon["name"]))
            return False
        else:
            return True
    else:
        print("No dispones de ataques para realizar")


def choose_pokemon(player_profile):
    chosen = None
    while not chosen:
        print("Elige con que pokemon lucharas")
        for index in range(len(player_profile["pokemon_inventory"])):
            print("{} - {}".format(index, get_pokemon_info(player_profile["pokemon_inventory"][index])))
        try:
            return player_profile["pokemon_inventory"][int(input("Cual eliges? "))]
        except (ValueError, IndexError):
            print("Opcion invalida")


def assing_exp(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["current_exp"] += points
        print("Tu {} ha ganado {} de experiencia".format(pokemon["name"], points))
        while pokemon["current_exp"] > 20:
            pokemon["current_exp"] -= 20
            pokemon["level"] += 1
            pokemon["current_health"] = pokemon["base_health"]
            print("Tu pokemon ha subido de nivel\n{}".format(get_pokemon_info(pokemon)))


def capture_with_pokeball(player_profile, enemy_pokemon):
    if player_profile["pokeballs"] > 0:
        player_profile["pokeballs"] -= 1
        enemy_caught_try = random.randint(1, 100)
        if enemy_caught_try >= 15:
            player_profile["pokemon_inventory"].append(enemy_pokemon)
            print("{} atrapado con exito!".format(enemy_pokemon["name"]))
            return False

        else:
            print("Ufff por poco lo logras...\n")
            return True
    else:
        print("No te quedaban pokeballs, pierdes el turno por no estar atento...")
        return True


def cure_pokemon(player_profile, player_pokemon):
    if player_profile["health_potion"] > 0:
        player_pokemon["current_health"] += 50
        if player_pokemon["current_health"] == 100:
            player_pokemon["current_health"] = 100
        player_profile["health_potion"] -= 1
        print("Has usado una pocion!"
              "\nTu {} ha recuperado 50 pts de salud...".format(player_pokemon["name"]))
    else:
        print("No te quedaban pociones, pierdes el turno por no estar atento...")


def fight(player_profile, enemy_pokemon):
    print("--- NUEVO COMBATE ---")

    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    still_in_combat = True
    print("{} VS {}".format(get_pokemon_info(player_pokemon), get_pokemon_info(enemy_pokemon)))
    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:

        # Player Turn:
        action = None
        while action not in ["A", "P", "V", "C"]:
            action = input("Que deseas hacer: [A]tacar, [P]okeball({}), Pocion de [V]ida ({}), [C]ambiar"
                           .format(player_profile["pokeballs"], player_profile["health_potion"]))
            if action.lower() == "a":
                still_in_combat = player_attack(player_pokemon, enemy_pokemon)
                attack_history.append(player_pokemon)
            elif action.lower() == "p":
                still_in_combat = capture_with_pokeball(player_profile, enemy_pokemon)
            elif action.lower() == "v":
                cure_pokemon(player_profile, player_pokemon)
                still_in_combat = True
            elif action.lower() == "c":
                player_pokemon = choose_pokemon(player_profile)
                still_in_combat = True

            if not still_in_combat:
                break

            # Enemys Turn:
            still_in_combat = enemy_turn(player_pokemon, enemy_pokemon, player_profile)

        if not still_in_combat:
            break

        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
            player_pokemon = choose_pokemon(player_profile)

    if enemy_pokemon["current_health"] == 0:
        assing_exp(attack_history)
        item_lotery(player_profile)

    input("Presiona ENTER para continuar...")


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
        print("Has ganado una pokeball")
    elif item == 2:
        player_profile["health_potion"] += 1
        print("Has ganado una pocion")


def main():

    pokemon_list = get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)
    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        enemy_pokemon["level"] = player_pokemon_toplvl(player_profile)
        print("Tu proximo contrincante es {}".format(get_pokemon_info(enemy_pokemon)))
        fight(player_profile, enemy_pokemon)

    print("Has perdido en el combate n{}".format(player_profile["combats"]))


if __name__ == "__main__":
    main()
