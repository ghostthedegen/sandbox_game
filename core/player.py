class Player:
    def __init__(self, name):
        self.name = name
        self.money = 500
        self.dirty_money = 0
        self.reputation = 0
        self.inventory = {}
        self.owned_properties = []
        self.owned_nightclubs = []
        self.owned_arcades = []
        self.alive = True
        self.owned_cars = {}
        self.last_arcade_collection_day = 0
        self.last_club_collection_day = 0
