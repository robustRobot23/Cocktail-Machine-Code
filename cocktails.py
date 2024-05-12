import json

class Cocktail():
    def __init__(self,name=None,liquor=None, shots_liquor=None, mixers=[], ml_mixers=[]):
        self.name = name
        self.liquor = liquor
        self.shots_liquor = shots_liquor
        self.mixers = mixers
        self.mixers_ml = ml_mixers

cocktails = []
cocktails_config_filename = "config/cocktails.json"

def load_cocktails():
    print("loading cocktails...")
    with open(cocktails_config_filename, 'r') as f:
        cocktails_json = json.load(f)
        cocktails_json = cocktails_json["Cocktails"]
        for cocktail_json in cocktails_json:
            cocktail = Cocktail()

            cocktail.name = cocktail_json["name"]
            
            cocktail_ingredients = cocktail_json["ingredients"]

            liquor = cocktail_ingredients["liquor"]
            cocktail.liquor = liquor["type"]
            cocktail.shots_liquor = liquor["number_of_shots"]

            mixer = cocktail_ingredients["mixer"]
            cocktail.mixers = mixer["type"]
            cocktail.mixers_ml = mixer["ml"]

            cocktails.append(cocktail)


    print(f"loaded {len(cocktails)} cocktails")
    for cocktail in cocktails:
        print(cocktail.name)

if __name__ == "__main__":
    load_cocktails()