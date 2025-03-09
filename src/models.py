


class Shop:
    """A shop that sells goods to customers"""
    def __init__(self, name):
        self.name = name

class Item:
    """Something that can be sold by shops to customers"""
    def __init__(self, name):
        self.name = name

class Customer:
    """A customer that can buy goods from one or more shops"""
    def __init__(self, name):
        self.name = name