class HasBattleSystem:
    def __init__(self, health, strength):
        self.health = health
        self.strength = strength

    def damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0
