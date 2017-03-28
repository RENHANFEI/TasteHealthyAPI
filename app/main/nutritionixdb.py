#!/usr/bin/env python

from nutritionix import Nutritionix

nix = Nutritionix(app_id="46e19a0a", api_key="b05d85f8570c41a40f5bc4cca2c5d57f")

food_model = \
{u'nf_ingredient_statement': u'statements',
u'nf_serving_weight_grams': 212, 
u'allergen_contains_soybeans': None,
u'brand_name': u"McDonald's",
u'nf_calories_from_fat': 250,
u'nf_calcium_dv': 25,
u'brand_id': u'513fbc1283aa2dc80c000053',
u'allergen_contains_eggs': None,
u'nf_iron_dv': 25,
u'nf_cholesterol': 80,
u'item_description': u'Burgers & Sandwiches - Big Mac',
u'usda_fields': None,
u'nf_monounsaturated_fat': None,
u'nf_dietary_fiber': 3,
u'item_name': u'Big Mac',
u'allergen_contains_tree_nuts': None,
u'allergen_contains_shellfish': None,
u'nf_vitamin_c_dv': 2,
u'nf_polyunsaturated_fat': None,
u'allergen_contains_peanuts': None,
u'nf_sugars': 9,
u'nf_servings_per_container': None,
u'nf_total_fat': 28,
u'nf_total_carbohydrate': 47,
u'leg_loc_id': 114,
u'nf_saturated_fat': 10,
u'allergen_contains_wheat': None,
u'old_api_id': None,
u'updated_at': u'2016-02-10T20:26:34.000Z',
u'allergen_contains_gluten': None,
u'nf_protein': 25,
u'item_id': u'513fc9e73fe3ffd40300109f',
u'nf_calories': 540,
u'nf_water_grams': None,
u'allergen_contains_fish': None,
u'nf_trans_fatty_acid': 1,
u'nf_serving_size_qty': 7.5,
u'allergen_contains_milk': None,
u'nf_vitamin_a_dv': 6,
u'nf_serving_size_unit': u'oz',
u'nf_refuse_pct': None,
u'nf_sodium': 970,
u'food_goup': u'FAST FOOD',
u'food_subgroup': u'All fast food outlets in alphabetical order',
u'restaurant_id': 0,
u'restaurant_name': u'restaurant_name'}


def search_food_name(food_name, result_num = 10): # result_num should <= 50

	if result_num <= 50: 
		try:
			search_result = nix.search(food_name, results = "0:" + \
				str(result_num)).json()
		except: # > total results
			search_num = nix.search(food_name).json()['total_hits']
			search_result = nix.search(food_name, results = "0:" + \
				str(search_num)).json()
	else:
		raise Exception("Result num must <= 50!")

	results = search_result['hits']
	name_results = {}

	for result in results:
		name_results[result[u'fields'][u'item_name']] = result[u'_id']

	return name_results


def search_food_id(food_id):

	try:
		food_entry = nix.item(id = food_id).json()
	except:
		raise Exception("Invalid Food ID")

	food = food_model

	for i in food_entry:
		food[i] = food_entry[i]

	return food


food_name = "cokessss"
# food_id = "513fceb675b8dbbc21001ead"

# x = search_food_id(food_id)

x = search_food_name(food_name)

print x

print len(x)

# print nix.search(food_name, results = "0:2").json()
# print x['nf_serving_weight_grams']



