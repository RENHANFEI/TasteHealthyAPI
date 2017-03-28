#!/usr/bin/env python
from .. import db
from ..models import *

class WeightControl(object):

	def __init__(self):
		pass


	def set_goal_weight_warning(self, age, gender, race, height, \
		goal_weight, start_weight):

		# get bmi goal tuple
		bmi_goal = db.session.query(BmiGoal).filter(BmiGoal.gender \
			== gender, BmiGoal.race == race, BmiGoal.age_min < age, \
			BmiGoal.age_max >= age).first()

		# get bmi standard
		min_healthy_bmi = float(bmi_goal.min_healthy_bmi)
		max_healthy_bmi = float(bmi_goal.max_healthy_bmi)
		obesity_bmi = bmi_goal.obesity_bmi

		min_healthy_weight = height * height * min_healthy_bmi
		max_healthy_weight = height * height * max_healthy_bmi

		# judge
		if goal_weight < min(start_weight, min_healthy_weight):
			return "LOW"
		elif goal_weight > max(start_weight, max_healthy_weight):
			return "HIGH"
		else:
			return 0

		
	def set_duration(self, start_weight, goal_weight, start_date, \
		end_date, weight_change_speed, duration):
		
		weight_change = goal_weight - start_weight

		# get 2 from 1
		if end_date != None:
			duration = (end_date - start_date).days
			weight_change_speed = abs(weight_change)/duration*7
		elif weight_change_speed != None:
			duration = int(abs(weight_change)/weight_change_speed*7.0)
			end_date = start_date + datetime.timedelta(days = duration)
		else:
			end_date = start_date + datetime.timedelta(days = duration)
			weight_change_speed = abs(weight_change)/duration*7

		# set duration warning
		max_weekly_weight_loss = ConstantsTable.query.filter_by(\
			cons_name = 'max_weekly_weight_loss')
		min_weekly_weight_gain = ConstantsTable.query.filter_by(\
			cons_name = 'max_weekly_weight_gain')

		duration_warning = False

		if weight_change < 0:
			if weight_change_speed > max_weekly_weight_loss:
				duration_warning = True
		else:
			if weight_change_speed > max_weekly_weight_gain:
				duration_warning = True

		result = {}
		result['end_date'] = str(end_date)[0:10]
		result['weight_change_speed'] = weight_change_speed
		result['duration'] = duration
		result['duration_warning'] = duration_warning

		return result



	def get_daily_goal_energy(self, start_weight, goal_weight, duration, 
		energy_expenditure):
		
		calorie_per_kilogram = ConstantsTable.query.filter_by(\
			cons_name = 'calorie_per_kilogram').first().cons_value

		daily_goal_energy = energy_expenditure + (goal_weight - start_weight) * \
			calorie_per_kilogram / duration

		return daily_goal_energy