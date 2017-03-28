#!/usr/bin/env python

class UserOperation(object):

	def __init__(self):
		pass

	def sql_update_user(user_id):
		
		'''get tuple'''
		user = UserProfile.query.filter_by(user_id = user_id).first()

		'''basic info'''
		f = False # for converting disease

		gender = user.gender
		birthday = user.birthday
		race = user.race
		disease = eval(str(user.disease))
		weight = user.weight
		height = user.height
		activity_level = user.activity_level

		'''update physical info'''
		age = get_age(birthday)
		bmi = get_bmi(weight, height)
		bmi_category = get_bmi_category(age, gender, race, bmi)
		energy_expenditure = get_energy_expenditure(age, bmi_category, \
			disease, gender, weight, height, activity_level)
		disease = set_obesity(bmi_category, disease)

		'''goal info'''
		start_weight = user.start_weight
		goal_weight = user.goal_weight
		start_date = user.start_date

		goal_weight_warning = set_goal_weight_warning(age, \
			gender, race, height, goal_weight, start_weight)

		# dependent on each other, auto generate 2 from 1
		end_date = user.end_date
		weight_change_speed = user.weight_change_speed
		duration = user.duration

		end_date, weight_change_speed, duration, duration_warning = \
			set_duration(start_weight, goal_weight, start_date, \
				end_date, weight_change_speed, duration)

		# set daily goal energy
		daily_goal_energy = get_daily_goal_energy(start_weight, goal_weight, \
			duration, energy_expenditure)

		# get macronutrient goal
		min_carb_need, max_carb_need, min_protein_need, max_protein_need, \
		min_fat_need, max_fat_need, max_alcohol_need = get_macronutrient_goal(\
			daily_goal_energy)

		# get micronutrient goal
		othernutrient_dic = get_othernutrient_goal(age, gender, disease)

		# update user
		user.age = age
		user.disease = disease
		user.bmi = bmi
		user.bmi_category = bmi_category
		user.energy_expenditure = energy_expenditure
		user.weight_change_speed = weight_change_speed
		user.end_date = end_date
		user.duration = duration
		user.daily_goal_energy = daily_goal_energy
		user.min_carb_need = min_carb_need
		user.max_carb_need = max_carb_need
		user.min_protein_need = min_protein_need
		user.max_protein_need = max_protein_need
		user.min_fat_need = min_fat_need
		user.max_fat_need = max_fat_need
		user.max_alcohol_need = max_alcohol_need

		# update user's other nutrient goal
		for nutrient in othernutrient_dic:
			exec('user.' + nutrient + '=' + str(othernutrient_dic[nutrient]))

		db.session.add(user)
		db.session.commit()

		return user, goal_weight_warning, duration_warning