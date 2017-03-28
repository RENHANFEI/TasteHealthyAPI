#!/usr/bin/env python
from .. import db
from ..models import *

import datetime

class HealthMetrics(object):

	def __init__ (self):
		pass

	def get_energy_expenditure(self, age, race, gender, weight, 
		height, activity_level):

		bmi_category = self.get_bmi_category(age, gender, race, weight, height)

		if bmi_category == "underweight":
			bmi_category = "normal"
		
		# query
		energy_expenditure = db.session.query(EnergyExpenditure).filter(\
			EnergyExpenditure.age_min < age, \
			EnergyExpenditure.age_max >= age, \
			EnergyExpenditure.bmi_category == bmi_category, \
			EnergyExpenditure.gender == gender).first()
		db.session.close()

		# get parameters for equation
		al_para = eval('energy_expenditure.' + activity_level)
		age_para = energy_expenditure.age_para
		weight_para = energy_expenditure.weight_para
		height_para = energy_expenditure.height_para
		cons_para = energy_expenditure.cons_para

		# calculate energy expenditure
		ee = age_para * age + al_para * (weight_para * weight + \
			height_para * height) + cons_para

		return ee


	def get_bmi(self, weight, height):
		return weight / height ** 2


	def get_bmi_category(self, age, gender, race, weight, height):

		bmi = weight / height ** 2

		# get tuple
		bmi_goal = db.session.query(BmiGoal).filter(BmiGoal.gender \
			== gender, BmiGoal.race == race, BmiGoal.age_min < age, \
			BmiGoal.age_max >= age).first()

		# get bmi standard
		min_healthy_bmi = bmi_goal.min_healthy_bmi
		max_healthy_bmi = bmi_goal.max_healthy_bmi
		obesity_bmi = bmi_goal.obesity_bmi

		# judge
		if bmi < min_healthy_bmi:
			return 'underweight'
		elif bmi < max_healthy_bmi:
			return 'normal'
		elif bmi < obesity_bmi:
			return 'overweight'
		else:
			return 'obesity'


	def get_age(self, birthday):

		today = datetime.date.today()
		age = today.year - birthday.year

		try:
			birthday = birthday.replace(year = today.year)
		except ValueError:
			# raised when birth date is February 29 
			# and the current year is not a leap year
			birthday = born.replace(year = today.year, day = birthday.day - 1)

		if birthday > today:
			return age
		else:
			return age - 1


	def set_obesity(self, bmi_category, disease):
		if bmi_category == 'obesity':
			disease[3] = True
		return disease


