# Shoe-Size-Predictor

* Simple App to predict shoe size based on height and gender. Try it out: https://shoe-size-predictor.herokuapp.com/
* Data used can be found here: https://osf.io/ja9dw/
* I used a simple linear regression to predict the shoe size based on height and gender.
* After every prediction or feedback (in case prediction was wrong), the user input is stored in a Postgresql database. I could have used an easier method of storing user input (e.g. insert user input into a google spreadsheet with gspread package) but i wanted to learn to deploy a heroku app with a database.
* The stored user inputs will be used to improve the prediction model.

