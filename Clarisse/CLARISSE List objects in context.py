#creates a variable holding a link to context (not string path as it can't do string ops)
materialContext = ix.get_item("project://env/material")
print materialContext
#creates a blank array in memory using C++ class
shaderArray = ix.api.OfObjectArray()
print shaderArray
#go to the linked context folder, set the filter to type material,and store all items in
#all sub-folders in the previsously created blank array
materialContext.get_objects("Material", shaderArray)
print materialContext.get_all_objects("Material", shaderArray)
#define an empty list
shaderList = []
#for the number of objects in the array append them into a list
for shader in range(shaderArray.get_count()):
    #appends items of array into list
    shaderList.append(shaderArray[shader])

#this will print thier indexed list items memory location
print shaderList
#for loop to print the contents of the indexed list
a=0
for shader in shaderList:
    print shaderList[a]
    a=a+1

        
print "blankTEST"     