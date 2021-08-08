#!/usr/bin/env python3

from traceback import format_exc
from requests import get
from colorhex import colorex, BOLD
from datetime import datetime
from sys import exit
from os import system

BLURPLE = '7289da'
GREEN = '43b581'
YELLOW = 'fdcc4b'
RED = 'f04947'

def main():
	system('clear')

	country = input(colorex('Enter a countries name, press enter without typing anything to auto detect your country or e to exit\n -> ', GREEN, BOLD))

	if country == '':
		try:
			auto_country = get('http://www.geoplugin.net/json.gp').json()

		except Exception as exc:
			system('clear')
			print(colorex(f'An error occured while trying to auto detect country. Please try again or enter the countries name and make sure you have internet access\nTraceback: {exc}', RED, BOLD))

			input(colorex('Press enter to go back\n-> ', GREEN, BOLD))

			system('clear')
			main()

		country = auto_country['geoplugin_countryName']

		getcovidstats(country)

	elif country == 'e':
		system('clear')
		exit()

	elif country != '':
		getcovidstats(country)

def getcovidstats(country):
	try:
		resp = get(f'https://disease.sh/v3/covid-19/countries/{country}').json()

	except Exception as exc:
		system('clear')
		print(colorex(f'An error occured while trying to get covid 19 stats. Please try again later and make sure you have internet access\nTraceback: {exc}', RED, BOLD))

		input(colorex('Press enter to go back\n-> ', GREEN, BOLD))

		system('clear')
		main()

	try:
		country_name = resp['country']

	except KeyError as exc:
		system('clear')
		print(colorex(f'Invalid country name, or the country doesnt have stats. Please try again\nTraceback: {format_exc()}', RED, BOLD))

		input(colorex('Press enter to go back\n-> ', GREEN, BOLD))

		system('clear')
		main()

	short_country_name = resp['countryInfo']['iso2']
	country_population = resp['population']
	total_cases = resp['cases']
	cases_today = resp['todayCases']
	total_deaths = resp['deaths']
	deaths_today = resp['todayDeaths']
	total_recovered = resp['recovered']
	today_recovered = resp['todayRecovered']
	continent = resp['continent']
	updated_at = datetime.fromtimestamp(resp['updated'] / 1000.0).strftime('%d %B %Y at %I:%M:%S %p')

	system('clear')

	print(colorex(f'Country: {country_name} ({short_country_name})', BLURPLE, BOLD))
	print(colorex(f'Continent: {continent}', BLURPLE, BOLD))
	print(colorex(f'Population: {country_population}', GREEN, BOLD))
	print(colorex(f'Total cases: {total_cases}, Today: {cases_today}', RED, BOLD))
	print(colorex(f'Total deaths: {total_deaths}, Today: {deaths_today}', RED, BOLD))
	print(colorex(f'Total recovered: {total_recovered}, Today: {today_recovered}', GREEN, BOLD))
	print(colorex(f'Updated at: {updated_at}', YELLOW, BOLD))

	input(colorex('Press enter to go back\n-> ', GREEN, BOLD))

	system('clear')
	main()

main()