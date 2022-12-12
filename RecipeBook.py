# https://tkdocs.com/tutorial/index.html
from tkinter import *
from tkinter import ttk
from Recipe import Recipe
import pickle

class RecipeBook:

    def __init__(self, root, recipeList):
        # root is main application window
        # set title of main application window
        root.title("Recipe Book")
        self.recipeList = recipeList

        # Create a content frame widget
        # configure to stretch to size of window
        noteBook = ttk.Notebook(root)
        noteBook.grid(column=0, row=0, sticky=(N, W, E, S))
        mainFrame = ttk.Frame(noteBook, borderwidth=5, relief="ridge", padding="3 3 12 12")
        mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        noteBook.add(mainFrame, text="Shopping List")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Shopping List tab widgets
        self.listVar = StringVar(value=self.recipeList)
        self.recipeListBox = Listbox(mainFrame, listvariable=self.listVar, height=15, 
                selectmode=MULTIPLE)
        self.recipeListBox.grid(column=1, row=0, sticky=(N, W))
        scrollBar = ttk.Scrollbar(mainFrame, orient=VERTICAL, command=self.recipeListBox.yview)
        scrollBar.grid(column=0, row=0, sticky=(N,S))
        self.recipeListBox['yscrollcommand'] = scrollBar.set
        ttk.Button(mainFrame, text="Create Shopping List", command=self.CreateShoppingList).grid(
                column=1, row=2, sticky=W)
        self.shoppingListVar = StringVar()
        self.shoppingListBox = Listbox(mainFrame, listvariable=self.shoppingListVar, height=15,
                width=35)
        self.shoppingListBox.grid(column=5, row=0, sticky=(E))
        self.shoppingListBox.configure(state=DISABLED)
        scrollBar2 = ttk.Scrollbar(mainFrame, orient=VERTICAL, command=self.shoppingListBox.yview)
        scrollBar2.grid(column=4, row=0, sticky=(N,S))
        self.shoppingListBox['yscrollcommand'] = scrollBar2.set


        # Add Recipes tab widgets
        addFrame = ttk.Frame(noteBook, padding="3 3 12 12", borderwidth=5, relief="ridge")
        addFrame.grid(column=0, row=1, sticky=(N, W, E, S))
        noteBook.add(addFrame, text="Add Recipes")
        # Recipe list again
        self.addList = StringVar(value=self.recipeList)
        self.editListBox = Listbox(addFrame, listvariable=self.addList, height=15)
        self.editListBox.grid(column=1, row=0, rowspan=3, sticky=(N, W))
        self.editListBox.bind("<<ListboxSelect>>", self.DisplayIngredients)
        scrollBar3 = ttk.Scrollbar(addFrame, orient=VERTICAL, command=self.editListBox.yview)
        scrollBar3.grid(column=0, row=0, rowspan=3, sticky=(N,S))
        self.editListBox['yscrollcommand'] = scrollBar3.set
        self.listSelection = StringVar()
        self.listSelection.set("Ingredient List:")
        ttk.Label(addFrame, textvariable=self.listSelection).grid(column=4, row=0, rowspan=2, sticky=(N, E))
        # Recipe Name
        ttk.Label(addFrame, text="Recipe Name:").grid(column=2, row=0, sticky=(S, W))
        self.recipeName = StringVar()
        self.recipeEntry = ttk.Entry(addFrame, width=30, textvariable=self.recipeName)
        self.recipeEntry.grid(column=2, row=1, sticky=(N, W))
        ttk.Button(addFrame, text="Add Recipe", command=self.AddRecipe).grid(column=3, row=1,
                sticky=(N, W))
        # Edit Recipe Name
        ttk.Label(addFrame, text="Edit Recipe Name:").grid(column=2, row=1, sticky=(S, W))
        self.editName = StringVar()
        self.editEntry = ttk.Entry(addFrame, width=30, textvariable=self.editName)
        self.editEntry.grid(column=2, row=2, sticky=(N, W))
        ttk.Button(addFrame, text="Update Recipe Name", command=self.EditRecipeName).grid(column=3, row=2,
                sticky=(N, W))
        # Edit ingredient list
        ttk.Label(addFrame, text="Edit Recipe: Enter ingredient name and amount (grams or units)").grid(
                column=2, row=3, columnspan=2, sticky=(S, W))
        self.ingredientName = StringVar()
        self.ingredientAmount = StringVar()
        self.ingredientEntry = ttk.Entry(addFrame, width=30,  textvariable=self.ingredientName).grid(
                column=2, row=4, sticky=(N, W))
        self.ingAmountEntry = ttk.Entry(addFrame, width=15,  textvariable=self.ingredientAmount).grid(
                column=3, row=4, sticky=(N, W))
        ttk.Button(addFrame, text="Update Ingredient", command=self.EditRecipeIngredients).grid(column=4, row=4,
                sticky=(N, W))
        # Remove recipe
        ttk.Button(addFrame, text="Remove Recipe", command=self.RemoveRecipe).grid(column=1, row=4,
                sticky=(N, W))
        # Save recipe book
        ttk.Button(addFrame, text="Save Recipe Book", command=self.SaveRecipeBook).grid(column=1, row=5,
                sticky=(N, W))

        # add padding to child widgets
        for child in mainFrame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
        for child in addFrame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
    def DisplayIngredients(self, *args):
        if len(self.editListBox.curselection()) == 1:
            currentValue = self.editListBox.curselection()[0]
            tempString = "Ingredient List:\n"
            tempString += self.recipeList[currentValue].GetIngredients()
            self.listSelection.set(tempString)
        elif len(self.editListBox.curselection()) > 1:
            tempString = "Ingredient List:\n"
            tempString += "  Multiple recipes selected"
            self.listSelection.set(tempString)
        elif len(self.editListBox.curselection()) == 0:
            tempString = "Ingredient List:\n"
            self.listSelection.set(tempString)
    
    def CreateShoppingList(self, *args):
        selectedList = []
        for x in self.recipeListBox.curselection():
            selectedList.append(self.recipeList[x])
        shoppingDict = {}
        for x in selectedList:
            for y in x.ingredientList:
                shoppingDict[y] = shoppingDict.get(y, 0) + x.ingredientList[y]
        returnList = []
        for x in shoppingDict:
            tempString = "{}: {}".format(x, shoppingDict[x])
            returnList.append(tempString)
        self.shoppingListVar.set(returnList)
    
    def AddRecipe(self, *args):
        recipeName = self.recipeName.get()
        tempRec = Recipe(recipeName)
        self.recipeList.append(tempRec)
        # Update list boxes
        self.listVar.set(self.recipeList)
        self.addList.set(self.recipeList)
        self.recipeName.set('')
    
    def RemoveRecipe(self, *args):
        if len(self.editListBox.curselection()) == 1:
            index = self.editListBox.curselection()[0]
        if len(self.recipeList) >= index:
            self.recipeList.pop(index)
        # Update list boxes
        self.listVar.set(self.recipeList)
        self.addList.set(self.recipeList)
    
    def EditRecipeName(self, *args):
        if len(self.editListBox.curselection()) == 1:
            index = self.editListBox.curselection()[0]
        currentRecipe = self.recipeList[index]
        value = self.editName.get()
        currentRecipe.name = value
        # Update list boxes
        self.listVar.set(self.recipeList)
        self.addList.set(self.recipeList)
        self.editName.set('')

    def EditRecipeIngredients(self, *args):
        if len(self.editListBox.curselection()) == 1:
            index = self.editListBox.curselection()[0]
        currentRecipe = self.recipeList[index]
        ingredientName = self.ingredientName.get()
        amount = self.ingredientAmount.get()
        if ingredientName and amount:
            currentRecipe.addIngredient(ingredientName, float(amount))
        elif ingredientName:
            currentRecipe.ingredientList.pop(ingredientName, 0)
        self.ingredientName.set('')
        self.ingredientAmount.set('')
        self.DisplayIngredients()
    
    def SaveRecipeBook(self, *args):
        with open('recipe_book.pkl', 'wb') as f:
            pickle.dump(self.recipeList, f, pickle.HIGHEST_PROTOCOL)