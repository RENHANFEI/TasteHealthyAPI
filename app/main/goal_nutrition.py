#!/usr/bin/env python
from .. import db
from ..models import *

class GoalNutrition(object):

	def __init__(self):
		pass

	def get_macronutrient_goal(self, daily_goal_energy):
		
		# get constants
		calorie_per_carb = ConstantsTable.query.filter_by(cons_name \
			= 'calorie_per_carb').first().cons_value
		calorie_per_protein = ConstantsTable.query.filter_by(cons_name \
			= 'calorie_per_protein').first().cons_value
		calorie_per_fat = ConstantsTable.query.filter_by(cons_name \
			= 'calorie_per_fat').first().cons_value
		gram_per_alcohol_unit = ConstantsTable.query.filter_by(cons_name \
			= 'gram_per_alcohol_unit').first().cons_value
		max_alcohol_unit_weekly = ConstantsTable.query.filter_by(cons_name \
			= 'max_alcohol_unit_weekly').first().cons_value
		min_carb_percentage = ConstantsTable.query.filter_by(cons_name \
			= 'min_carb_percentage').first().cons_value
		max_carb_percentage = ConstantsTable.query.filter_by(cons_name \
			= 'max_carb_percentage').first().cons_value
		min_protein_percentage = ConstantsTable.query.filter_by(cons_name \
			= 'min_protein_percentage').first().cons_value
		max_protein_percentage = ConstantsTable.query.filter_by(cons_name \
			= 'max_protein_percentage').first().cons_value
		min_fat_percentage = ConstantsTable.query.filter_by(cons_name \
			= 'min_fat_percentage').first().cons_value
		max_fat_percentage = ConstantsTable.query.filter_by(cons_name \
			= 'max_fat_percentage').first().cons_value

		# calculate
		min_carb_need = daily_goal_energy * min_carb_percentage / calorie_per_carb
		max_carb_need = daily_goal_energy * max_carb_percentage / calorie_per_carb
		min_protein_need = daily_goal_energy * min_protein_percentage / calorie_per_protein
		max_protein_need = daily_goal_energy * max_protein_percentage / calorie_per_protein
		min_fat_need = daily_goal_energy * min_fat_percentage / calorie_per_fat
		max_fat_need = daily_goal_energy * max_fat_percentage / calorie_per_fat
		max_alcohol_need = max_alcohol_unit_weekly * gram_per_alcohol_unit / 7

		macronutrient_dic = {}

		macronutrient_dic['min_carb_need'] = min_carb_need
		macronutrient_dic['max_carb_need'] = max_carb_need
		macronutrient_dic['min_protein_need'] = min_protein_need
		macronutrient_dic['max_protein_need'] = max_protein_need
		macronutrient_dic['min_fat_need'] = min_fat_need
		macronutrient_dic['max_fat_need'] = max_fat_need
		macronutrient_dic['max_alcohol_need'] = max_alcohol_need

		return macronutrient_dic


	def get_othernutrient_goal(self, age, gender, disease):

		disease = (False,False,False,False)
		
		# get tuple
		othernutrient_goal = db.session.query(GoalNutrient).filter(\
			GoalNutrient.age_min < age, GoalNutrient.age_max >= age, \
			GoalNutrient.gender == gender, GoalNutrient.disease == disease).first()

		# put in dic
		othernutrient_dic = {}
		othernutrient_dic['water'] = othernutrient_goal.water
		othernutrient_dic['fiber'] = othernutrient_goal.fiber
		othernutrient_dic['linoacid'] = othernutrient_goal.linoacid
		othernutrient_dic['alphalinoacid'] = othernutrient_goal.alphalinoacid
		othernutrient_dic['calcium'] = othernutrient_goal.calcium
		othernutrient_dic['chromium'] = othernutrient_goal.chromium
		othernutrient_dic['copper'] = othernutrient_goal.copper
		othernutrient_dic['fluoride'] = othernutrient_goal.fluoride
		othernutrient_dic['iodine'] = othernutrient_goal.iodine
		othernutrient_dic['iron'] = othernutrient_goal.iron
		othernutrient_dic['magnesium'] = othernutrient_goal.magnesium
		othernutrient_dic['manganese'] = othernutrient_goal.manganese
		othernutrient_dic['molybdenum'] = othernutrient_goal.molybdenum
		othernutrient_dic['phosphorus'] = othernutrient_goal.phosphorus
		othernutrient_dic['selenium'] = othernutrient_goal.selenium
		othernutrient_dic['zinc'] = othernutrient_goal.zinc
		othernutrient_dic['potassium'] = othernutrient_goal.potassium
		othernutrient_dic['sodium'] = othernutrient_goal.sodium
		othernutrient_dic['chloride'] = othernutrient_goal.chloride
		othernutrient_dic['vita'] = othernutrient_goal.vita
		othernutrient_dic['vitc'] = othernutrient_goal.vitc
		othernutrient_dic['vitd'] = othernutrient_goal.vitd
		othernutrient_dic['vite'] = othernutrient_goal.vite
		othernutrient_dic['vitk'] = othernutrient_goal.vitk
		othernutrient_dic['thiamin'] = othernutrient_goal.thiamin
		othernutrient_dic['riboflavin'] = othernutrient_goal.riboflavin
		othernutrient_dic['niacin'] = othernutrient_goal.niacin
		othernutrient_dic['vitb6'] = othernutrient_goal.vitb6
		othernutrient_dic['vitfolate'] = othernutrient_goal.vitfolate
		othernutrient_dic['vitb12'] = othernutrient_goal.vitb12
		othernutrient_dic['panacid'] = othernutrient_goal.panacid
		othernutrient_dic['biotin'] = othernutrient_goal.biotin
		othernutrient_dic['cholin'] = othernutrient_goal.cholin

		return othernutrient_dic



