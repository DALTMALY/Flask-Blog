# "__init__.py" tells to python interpreter that It convert a directory or file in a package
#Folder "flaskblog" inside "__init__.py" there are a function called (create_app)
from flaskblog import create_app

#Saving function and methods in a variable called "app"
app = create_app()

#If run like main file, then run the server
if __name__ == "__main__":
    app.run(debug=True)