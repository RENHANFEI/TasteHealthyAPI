#!/usr/bin/env python
from nutritionix import Nutritionix

from .. import db
from ..models import *


class FoodNutrition(object):

    def __init__(self, nutritionix_id = "46e19a0a", \
        nutritionix_key = "b05d85f8570c41a40f5bc4cca2c5d57f"):

        self.nix = Nutritionix(app_id = nutritionix_id, api_key = nutritionix_key)

        self.food_model = \
        {u'nf_ingredient_statement': u'',
        u'nf_serving_weight_grams': 0, 
        u'allergen_contains_soybeans': None,
        u'brand_name': u"",
        u'nf_calories_from_fat': 0,
        u'nf_calcium_dv': 0,
        u'brand_id': u'',
        u'allergen_contains_eggs': None,
        u'nf_iron_dv': 0,
        u'nf_cholesterol': 0,
        u'item_description': u'',
        u'usda_fields': None,
        u'nf_monounsaturated_fat': None,
        u'nf_dietary_fiber': 0,
        u'item_name': u'',
        u'allergen_contains_tree_nuts': None,
        u'allergen_contains_shellfish': None,
        u'nf_vitamin_c_dv': 0,
        u'nf_polyunsaturated_fat': None,
        u'allergen_contains_peanuts': None,
        u'nf_sugars': 0,
        u'nf_servings_per_container': None,
        u'nf_total_fat': 0,
        u'nf_total_carbohydrate': 0,
        u'leg_loc_id': 0,
        u'nf_saturated_fat': 0,
        u'allergen_contains_wheat': None,
        u'old_api_id': None,
        u'updated_at': u'',
        u'allergen_contains_gluten': None,
        u'nf_protein': 0,
        u'item_id': u'',
        u'nf_calories': 0,
        u'nf_water_grams': None,
        u'allergen_contains_fish': None,
        u'nf_trans_fatty_acid': 0,
        u'nf_serving_size_qty': 0,
        u'allergen_contains_milk': None,
        u'nf_vitamin_a_dv': 0,
        u'nf_serving_size_unit': u'',
        u'nf_refuse_pct': None,
        u'nf_sodium': 0,
        u'food_group': u'',
        u'food_subgroup': u'',
        u'restaurant_id': u'',
        u'restaurant_name': u''}


    def get_food_healthy_score(self, food_id):

        # traverse scored nutrients
        score = 0
        score_nutrients = FoodScoreNutrient.query.all()

        # get food tuple
        food = Food.query.filter_by(food_id = food_id).first()
        food_energy = food.energy

        for score_nutrient in score_nutrients:

            # get scored nutrient info
            score_nutrient_name = score_nutrient.score_nutrient_name
            nutrient_dv = float(score_nutrient.nutrient_dv)
            if score_nutrient.recommend:
                recom_flag = 1;
            else:
                recom_flag = -1

            # get corresponding food nutrient
            try:
                food_nutrient = float(eval('food.' + score_nutrient_name))
            except:
                food_nutrient = 0

            # calculate
            score += recom_flag * (food_nutrient/nutrient_dv)/food_energy

        # update food healthy score
        food.healthy_score = score
        db.session.add(food)
        db.session.commit()

        return score


    def search_food_name(self, food_name, result_num = 10, prior_search = "hpb_focos"):
        
        if prior_search == "hpb_focos":

            name_results = self.hpb_focos_search_food_name(food_name, result_num)

            search_num = len(name_results) 

            if search_num < result_num:
                name_results_2 = self.nutritionix_search_food_name(food_name, \
                    result_num - search_num)

                search_num += len(name_results_2)

                name_results.update(name_results_2)

                if search_num < result_num:
                    print "Only get " + str(search_num) + " results!"

        elif prior_search == "nutritionix":

            name_results = self.nutritionix_search_food_name(food_name, result_num)

            search_num = len(name_results) 

            if search_num < result_num:
                name_results_2 = self.hpb_focos_search_food_name(food_name, \
                    result_num - search_num)

                search_num += len(name_results_2)

                name_results.update(name_results_2)

                if search_num < result_num:
                    print "Only get " + str(search_num) + " results!"

        else:
            raise Exception("prior_search must be hpb_focos or nutritionix!")

        return name_results


    def search_food_id(self, food_id):
        
        if food_id[0:8] == 'hpbfocos':

            food_id = food_id[8:]
            food = self.hpb_focos_search_food_id(food_id)

        else:

            food = self.nutritionix_search_food_id(food_id)

        return food
        

    def nutritionix_search_food_name(self, food_name, result_num = 5): 
    # result_num should <= 50

        if result_num <= 50: 
            try:
                search_result = self.nix.search(food_name, results = "0:" + \
                    str(result_num)).json()
            except: # > total results
                search_num = self.nix.search(food_name).json()['total_hits']
                search_result = nix.search(food_name, results = "0:" + \
                    str(search_num)).json()
        else:
            raise Exception("Result num must <= 50!")

        results = search_result['hits']
        name_results = {}

        for result in results:
            name_results[result[u'fields'][u'item_name']] = result[u'_id']

        return name_results


    def nutritionix_search_food_id(self, food_id):

        try:
            food_entry = self.nix.item(id = food_id).json()
        except:
            raise Exception("Invalid Food ID")

        return food_entry


    def hpb_focos_search_food_name(self, food_name, result_num = 5):
    
        results = db.session.query(HpbFocosFood).filter(HpbFocosFood.\
            food_name.like('%%' + food_name + '%%')).all()

        search_num = len(results)

        if result_num <= search_num:
            results = results[0:result_num]
        else:
            print "Only get " + str(search_num) + " search results!"

        name_results = {}

        for result in results:
            name_results[result.food_name] = u'hpbfocos' + str(result.food_id)

        return name_results


    def hpb_focos_search_food_id(self, food_id):
            
        hpb_food = HpbFocosFood.query.filter_by(food_id = food_id).first()

        food = {}

        food[u'nf_serving_weight_grams'] = hpb_food.serving_gram
        # food[u'nf_calcium_dv'] = 0,
        # u'nf_iron_dv': 0,
        food[u'nf_cholesterol'] = hpb_food.cholesterol
        food[u'nf_dietary_fiber'] = hpb_food.fiber
        food[u'item_name'] = hpb_food.food_name
        # u'nf_vitamin_c_dv': 0,
        food[u'nf_total_fat'] = hpb_food.fat
        food[u'nf_total_carbohydrate'] = hpb_food.carb
        food[u'nf_saturated_fat'] = hpb_food.sat_fat
        food[u'nf_protein'] = hpb_food.protein
        food[u'item_id'] = u'hpbfocos' + str(hpb_food.food_id)
        food[u'nf_calories'] = hpb_food.energy
        #u'nf_vitamin_a_dv': 0,
        food[u'nf_serving_size_unit'] = hpb_food.serving_unit
        food[u'nf_sodium'] = hpb_food.sodium
        food[u'food_group'] = hpb_food.food_group
        food[u'food_subgroup'] = hpb_food.food_subgroup

        return food


