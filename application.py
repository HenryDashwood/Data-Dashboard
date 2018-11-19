from flask import Flask
from flask import render_template, request, Response, jsonify
import json, plotly
from wrangle_data import return_figures

application = Flask(__name__)

@application.route('/', methods=['POST', 'GET'])
@application.route('/index', methods=['POST', 'GET'])
def index():

	# List of countries for filter
	country_codes = [['Canada','CAN'],['United States','USA'],['Brazil','BRA'],['France','FRA'],['India','IND'],['Italy','ITA'],['Germany','DEU'],['United Kingdom','GBR'],['China','CHN'],['Japan','JPN']]

	# Parse the POST request countries list
	if (request.method == 'POST') and request.form:
		figures = return_figures(request.form)
		countries_selected = []

		for country in request.form.lists():
			countries_selected.append(country[1][0])

	# GET request returns all countries for initial page load
	else:
		figures = return_figures()
		countries_selected = []
		for country in country_codes:
			countries_selected.append(country[1])

	# plot ids for the html id tag
	ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

	# Convert the plotly figures to JSON for javascript in html template
	figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

	return render_template('index.html', ids=ids, figuresJSON=figuresJSON, all_countries=country_codes, countries_selected=countries_selected)

if __name__ == '__main__':
	application.run(host='0.0.0.0')
