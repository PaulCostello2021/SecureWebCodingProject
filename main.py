from website import create_app


app = create_app()

# This will run our application in flask. The debug=True means that when we make a change to our code 
# It will automaticaly rerun the webserver. 

if __name__ == '__main__': 
    app.run(debug=True)
