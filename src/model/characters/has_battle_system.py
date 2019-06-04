class HasBattleSystem:
    """
    Object that inherits this class has battle system. Such objects
    can fight in the game.
    """

    def __init__(self, health, strength):
        """
        :param health: Amount of health that object has.
        :param strength: Amount of damage that object can deal.
        """

        self.health = health
        self.strength = strength

    def damage(self, damage):
        """
        Damages this object by given amount of damage.

        :param damage: Amount of damage that is dealt to this object.
        :return: None.
        """

        self.health -= damage

    def is_alive(self):
        """
        Checks whether this object is alive or not.

        :return: True if object is alive. False otherwise.
        """

        return self.health > 0
