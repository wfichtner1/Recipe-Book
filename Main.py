import pickle
from Recipe import Recipe
from RecipeBook import RecipeBook
from FeetToMeters import FeetToMeters
from tkinter import *

myRecipes = []

try:
    with open('recipe_book.pkl', 'rb') as f:
        myRecipes = pickle.load(f)
except:
    myRecipes = []

root = Tk()
root.geometry("800x450")
RecipeBook(root, myRecipes)
#FeetToMeters(root)
root.mainloop()