# COVID19 by state
The project website is available here:

https://covid19bystateusa.com

This project displays the number of COVID19 cases and deaths in each US state and territory, as well as each country. Cases are displayed as a running total, with cases 28 days old or older removed from the total. This essentially gives us an estimate of the number of people who are currently sick with COVID19 in a given state, territory, or country. 

# Usage
This project uses a Python 3.7.x environment.

In the command line, run
```terminal 
python3 -m venv ./env
source ./env/bin/activate
pip3 install -e .

# run the project locally with the command 
covid_update

# when you're done, exit the venv with
deactivate
```

# Data Source
Data is taken from the Johns Hopkins University COVID19 GitHub repo:

https://github.com/CSSEGISandData/COVID-19

I also use global population data from here:

https://data.worldbank.org/indicator/SP.POP.TOTL
