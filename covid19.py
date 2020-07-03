# -*- coding: utf-8 -*-

import pandas as pd
import csv
import urllib.request as request
import matplotlib.pyplot as plt
import numpy as np
import datetime


verbose = False 


def adjust_header(df):
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    return df


r = request.urlopen('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv').read().decode('utf8').split("\n")
reader = csv.reader(r)
confirmed_US = pd.DataFrame(reader)
confirmed_US = adjust_header(confirmed_US)

r = request.urlopen('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv').read().decode('utf8').split("\n")
reader = csv.reader(r)
deaths_US = pd.DataFrame(reader)
deaths_US = adjust_header(deaths_US)

r = request.urlopen('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv').read().decode('utf8').split("\n")
reader = csv.reader(r)
deaths_global = pd.DataFrame(reader)
deaths_global = adjust_header(deaths_global)

r = request.urlopen('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv').read().decode('utf8').split("\n")
reader = csv.reader(r)
confirmed_global = pd.DataFrame(reader)
confirmed_global = adjust_header(confirmed_global)


def sort_by_state(df):
    df = df.groupby("Province_State").sum()
    return df


def sort_by_country(df):
    df = df.groupby("Country/Region").sum()
    return df


confirmed_US = confirmed_US.apply(pd.to_numeric, errors='ignore')
confirmed_US_by_state = sort_by_state(confirmed_US)

deaths_US = deaths_US.apply(pd.to_numeric, errors='ignore')
deaths_US_by_state = sort_by_state(deaths_US)

deaths_global = deaths_global.apply(pd.to_numeric, errors='ignore')
deaths_global_by_country = sort_by_country(deaths_global)

confirmed_global = confirmed_global.apply(pd.to_numeric, errors='ignore')
confirmed_global_by_country = sort_by_country(confirmed_global)

if verbose:
    confirmed_US_by_state.to_csv('confirmed_US_by_state.csv')
    deaths_US_by_state.to_csv('deaths_US_by_state.csv')
    deaths_global_by_country.to_csv("death_global_by_country.csv")
    confirmed_global_by_country.to_csv("confirmed_global_by_country.csv")

population_us = deaths_US_by_state["Population"].to_dict()


def plot_active(df, start_date, path, population={}):

  now = datetime.datetime.now()
  today = now.strftime("%Y_%m_%d")
  # assuming that active cases get "resolved" in 4 weeks
  start_index = df.columns.get_loc(start_date)
  for index, row, in df.iterrows():
    total_cases = row.iloc[start_index:]
    active_cases = []
    dates = []
    contagious_period = 28
    for i in range(contagious_period, len(total_cases)):
      active_cases.append((total_cases[i]-total_cases[i-contagious_period]))
      plot_name = "Number of cases"
      dates.append(total_cases.index[i])

    fig, ax = plt.subplots()
    max_cases = np.nanmax(active_cases)
    if max_cases == 0:
      max_cases = 100
    ax.set(ylim=(0, max_cases * 1.1))
    if index in population.keys():
      ax2 = ax.twinx()
      ax2.set_ylabel("Cases per 1,000 People")
      # The cruise ships have a population of 0, which breaks things
      if population[index] == 0.0:
        plt.close()
        continue
      ax2.set(ylim=(0, max_cases * 1000 / population[index]))

    ax.plot(dates, active_cases)
    ax.set_xticks(np.arange(0, len(active_cases), step=7))
    ax.tick_params(axis='x', rotation=45)
    ax.set_ylabel(plot_name)

    plt.gcf().subplots_adjust(bottom=0.15)
    fig.suptitle(index + ' - New Cases in Last 28 Days - ' + today)
    fig.savefig(path + 'cases_' + index + '.png', bbox_inches='tight', dpi=75)
    plt.close()


confirmed_US_by_state = confirmed_US_by_state.append(confirmed_US_by_state.sum(axis=0).rename("Total"))
plot_active(confirmed_US_by_state, "2/22/20", "plots/us/cases/", population_us)

confirmed_global_by_country = confirmed_global_by_country.append(confirmed_global_by_country.sum(axis=0).rename("Total"))
plot_active(confirmed_global_by_country, "1/22/20", "plots/global/cases/")


def plot_deaths(df, start_date, path, population={}):

  now = datetime.datetime.now()
  today = now.strftime("%Y_%m_%d")

  start_index = df.columns.get_loc(start_date)
  for index, row in df.iterrows():
    new_deaths = []
    deaths = row.iloc[start_index:]
    new_deaths.append(deaths[0])
    for i in range(1, len(deaths)):
      new_deaths.append(deaths[i] - deaths[i-1])

    sma_deaths = []
    sma = 8
    mid = int(sma / 2)
    for i in range(mid, len(new_deaths)-mid):
      sma_deaths.append(np.sum(new_deaths[i-mid:i+mid])/sma)

    fig, ax = plt.subplots()
    max_cases = np.nanmax(sma_deaths)
    if max_cases == 0:
      max_cases = 100
    ax.set(ylim=(0, max_cases * 1.1))
    if index in population.keys():
      ax2 = ax.twinx()
      ax2.set_ylabel("Deaths per 1 Million People")
      # The cruise ships have a population of 0, which breaks things
      if population[index] == 0.0:
        plt.close()
        continue
      ax2.set(ylim=(0, max_cases * 1000000 / population[index]))
    ax.plot(deaths.index[mid:], new_deaths[mid:], color='powderblue')
    ax.plot(deaths.index[mid:len(deaths)-mid], sma_deaths, color='orange')
    ax.set_xticks(np.arange(0, len(sma_deaths), step=7))
    ax.tick_params(axis='x', rotation=45)
    ax.set_ylabel('Deaths')
    fig.suptitle(index + " - Deaths - " + today)
    fig.savefig(path + 'deaths_' + index + '.png', bbox_inches='tight', dpi=75)
    plt.close()


deaths_US_by_state = deaths_US_by_state.append(deaths_US_by_state.sum(axis=0).rename("Total"))
plot_deaths(deaths_US_by_state, "3/17/20", 'plots/us/deaths/',  population_us)

deaths_global_by_country = deaths_global_by_country.append(deaths_global_by_country.sum(axis=0).rename("Total"))
plot_deaths(deaths_global_by_country, "2/16/20", 'plots/global/deaths/')
