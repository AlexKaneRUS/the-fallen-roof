from abc import abstractmethod


class HasBattleSystem:
    def __init__(self, health, strength, experience_from_killing=0):
        self.health = health
        self.strength = strength

        self.experience = 0
        self.level = 1

        self.experience_from_killing = experience_from_killing

    def damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

    def attack(self, other):
        pass

    def add_experience(self, n):
        self.experience += n

        self.level_up()

    @abstractmethod
    def level_up(self):
        pass

