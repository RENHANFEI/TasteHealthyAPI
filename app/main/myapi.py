from flask import Flask, request
from flask_restplus import Resource, Api

import datetime

from . import main
from .. import api

from food_nutrition import FoodNutrition
from health_metrics import HealthMetrics
from weight_control import WeightControl
from goal_nutrition import GoalNutrition


'''
FOOD NUTRITION
Get Food Nutrition Data from HPB_FOCOS & NUTRITIONIX
'''

'''Search Food items'''
fn = FoodNutrition()

@main.route('/go')
def go():
	return "hello"

@api.route('/food-nutrition/search')
@api.doc(params={'food_name':'food name','result_num': 'num of results', \
	'prior_search': 'hpb_focos(default)/nutritionix'})
class FoodSearch(Resource):
    def get(self):
    	food_name = request.args.get('food_name')
    	result_num = request.args.get('result_num')
    	prior_search = request.args.get('prior_search')
    	if prior_search == None:
    		if result_num == None:
        		return fn.search_food_name(food_name)
        	else:
        		return fn.search_food_name(food_name, int(result_num))
        else:
        	return fn.search_food_name(food_name, int(result_num), prior_search)

'''Get Food Items'''
@api.route('/food-nutrition/item/<string:food_id>')
class Fooditem(Resource):
	def get(self,food_id):
		return fn. search_food_id(food_id)


'''
HEALTH METRICS
Reference Krauseas Food & the Nutrition Care Process
'''
hm = HealthMetrics()

'''Calculate BMI'''
@api.route('/health-metrics/bmi/calculation')
@api.doc(params={'weight': 'kg', 'height':'m'})
class BmiCalculation(Resource):
	def get(self):
		weight = request.args.get('weight') # kg
		height = request.args.get('height') # m
		return hm.get_bmi(float(weight), float(height))

'''Get BMI Category'''
@api.route('/health-metrics/bmi/category')
@api.doc(params={'age':'year','weight': 'kg', 'height':'m','gender':'male/female', \
	'race':'asian/african/caucasian/indian/other'})
class BmiCategory(Resource):
	def get(self):
		age = request.args.get('age')
		gender = request.args.get('gender') # male/female
		race = request.args.get('race')
		weight = request.args.get('weight') # kg
		height = request.args.get('height') # m
		return hm.get_bmi_category(age, gender, race, float(weight), float(height))

'''Get Energy Expenditure'''
@api.route('/health-metrics/energy-expenditure')
@api.doc(params={'age':'year','weight': 'kg', 'height':'m','gender':'male/female', \
	'race':'asian/african/caucasian/indian/other', \
	'activity_level':'sedentary/low_active/active/very_active'})
class EnergyExpenditure(Resource):
	def get(self):
		age = request.args.get('age')
		gender = request.args.get('gender') # male/female
		race = request.args.get('race')
		weight = request.args.get('weight') # kg
		height = request.args.get('height') # m
		activity_level = request.args.get('activity_level') 
		return hm.get_energy_expenditure(int(age), race, gender, float(weight), \
			float(height), activity_level)


'''
WRIGHT CONTROL
Reference Krauseas Food & the Nutrition Care Process
'''
wc = WeightControl()


'''Get Goal Weight Warning'''
@api.route('/weight-control/goal-weight')
@api.doc(params={'age':'year','height':'m','gender':'male/female', 'start_weight':'kg', \
	'goal_weight':'kg', 'race':'asian/african/caucasian/indian/other'})
class GoalWeight(Resource):
	def get(self):
		age = request.args.get('age')
		gender = request.args.get('gender')
		race = request.args.get('race')
		height = request.args.get('height')
		start_weight = request.args.get('start_weight')
		goal_weight = request.args.get('goal_weight')
		return wc.set_goal_weight_warning(int(age), gender, race, float(height), \
			float(goal_weight), float(start_weight))

'''Set Duration & Get Duration Warning'''
@api.route('/weight-control/duration')
@api.doc(params={'start_weight':'kg', 'goal_weight':'kg', 'start_date':'YY-MM-DD', \
	'end_date':'YY-MM-DD(can be None)', 'weight_change_speed':'kg/week(can be None)',\
	'duration':'day(can be None)'})
class Duration(Resource):
	def get(self):
		start_weight = request.args.get('start_weight')
		goal_weight = request.args.get('goal_weight')
		start_date = datetime.datetime.strptime(request.args.get('start_date'), "%Y-%m-%d")
		end_date = request.args.get('end_date')
		weight_change_speed = request.args.get('weight_change_speed')
		duration = request.args.get('duration')
		try:
			end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
		except:
			pass
		try:
			weight_change_speed = float(weight_change_speed) # unit: kg/week
		except:
			pass
		try:
			duration = int(duration)
		except:
			pass
		return wc.set_duration(float(start_weight), float(goal_weight), start_date, \
			end_date, weight_change_speed, duration)


'''Get Daily Goal Energy'''
@api.route('/weight-control/daily-goal-energy')
@api.doc(params={'start_weight':'kg', 'goal_weight':'kg', 'duration':'day',\
	'energy_expenditure':'kcal/day',})
class DailyGoalEnergy(Resource):
	def get(self):
		start_weight = request.args.get('start_weight')
		goal_weight = request.args.get('goal_weight')
		duration = request.args.get('duration')
		energy_expenditure = request.args.get('energy_expenditure')
		if energy_expenditure == None:
			age = request.args.get('age')
			gender = request.args.get('gender') # male/female
			race = request.args.get('race')
			weight = request.args.get('weight') # kg
			height = request.args.get('height') # m
			activity_level = request.args.get('activity_level') 
			energy_expenditure = get_energy_expenditure(int(age), race, gender, float(weight), \
				float(height), activity_level)

		return wc.get_daily_goal_energy(float(start_weight), float(goal_weight), \
			int(duration), float(energy_expenditure))


'''
GOAL NUTRIENT
Reference Krauseas Food & the Nutrition Care Process
'''
gn = GoalNutrition()

@api.route('/goal-nutrient/macronutrient')
@api.doc(params={'daily_goal_energy':'kcal/day'})
class Macronutrient(Resource):
	def get(self):
		daily_goal_energy = request.args.get('daily_goal_energy')
		return gn.get_macronutrient_goal(float(daily_goal_energy))

@api.route('/goal-nutrient/othernutrient')
@api.doc(params={'age':'year','gender':'male/female', \
	'disease':'{True/False(diabetes), True/False(heart_disease), True/False(copd), True/False(obesity)}'})
class Othernutrient(Resource):
	def get(self):
		age = request.args.get('age')
		gender = request.args.get('gender')
		disease = request.args.get('disease')
		return gn.get_othernutrient_goal(int(age), gender, disease)


# if __name__ == '__main__':
#     app.run(debug=True)



