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
    # print("loading cocktails...")
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
            
            mixers = cocktail_ingredients["mixers"]
            for mixer in mixers:
                cocktail.mixers.append(mixer["type"])
                cocktail.mixers_ml.append(mixer["ml"])

            cocktails.append(cocktail)


    # print(f"loaded {len(cocktails)} cocktails")
    # for cocktail in cocktails:
    #     print(cocktail.name)

def get_possible_cocktails(liquor, possible_mixers):
    possible_cocktails = []
    for cocktail in cocktails:
        liquor_matches = True
        if cocktail.liquor is not 'None':
            # print(f"Liquors: {cocktail.liquor}")
            liquor_matches = cocktail.liquor == liquor
        mixers_match = True
        if not cocktail.mixers == ['None']:
            # print(f"Mixer: {cocktail.mixers}")
            for mixer in cocktail.mixers:
                if mixer not in possible_mixers:
                    mixers_match = False
                    break         
        if liquor_matches and mixers_match:
            # print(f"Cocktail: {cocktail.name} in machine")
            possible_cocktails.append(cocktail)
        
    return possible_cocktails

load_cocktails()      
if __name__ == "__main__":
    
    liquor = "Gin"
    m1 = "Tonic"
    m2 = "Lemonade"
    possible_cocktails = get_possible_cocktails(liquor, [m1, m2])
    print("Possible Cocktails:")
    for possible_cocktail in possible_cocktails:
        print(possible_cocktail.name)