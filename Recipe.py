class Recipe:
    def __init__(self, name):
      self.name = name
      self.ingredientList = {}

    def __str__(self):
        return self.name

    def addIngredient(self, ingredient, amount):
        self.ingredientList[ingredient] = amount

    def GetIngredients(self):
        ingredientString = ''
        for x in self.ingredientList:
            ingredientString += "  {}: {}".format(x, self.ingredientList[x]) + "\n"
        return ingredientString