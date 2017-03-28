#!/usr/bin/env python

from . import db
import sqlalchemy.types as types


'''Types'''

class Race(types.UserDefinedType):
    race = db.Enum('caucasian', 'asian', 'indian', 'african', 'other', name = 'race')


class Gender(types.UserDefinedType):
    gender = db.Enum('male', 'female', 'other', name='gender')


class BmiCategory(types.UserDefinedType):
    bmi_category = db.Enum('underweight', 'normal', 'overweight', 'obesity', name='bmi_category')


class ActivityLevel(types.UserDefinedType):
    activity_level = db.Enum('sedentary', 'low_active', 'active', 'very_active', name='activity_level')


class LoggingWay(types.UserDefinedType):
    logging_way = db.Enum('image', 'manual', name='logging_way')


class Disease(types.UserDefinedType):
    def __init__(self, diabetes, heart_disease, copd, obesity):
        self.diabetes = diabetes,
        self.heart_disease = heart_disease,
        self.copd = copd,
        self.obesity = obesity


class GeoCoordinate(types.UserDefinedType):
    def __init__(self,latitude,longitude):
        self.latitude = latitude
        self.longitude = longitude

'''Models'''

class BmiGoal(db.Model):
    __tablename__ = 'bmi_goal'

    bmi_goal_id = db.Column(db.Integer, primary_key=True)
    age_min = db.Column(db.SmallInteger)
    age_max = db.Column(db.SmallInteger)
    gender = db.Column(Gender)
    race = db.Column(Race)
    min_healthy_bmi = db.Column(db.Float)
    max_healthy_bmi = db.Column(db.Float)
    obesity_bmi = db.Column(db.Float)


class ConstantsTable(db.Model):
    __tablename__ = 'constants_table'

    cons_name = db.Column(db.String(50), primary_key=True)
    cons_value = db.Column(db.Float)


class EnergyExpenditure(db.Model):
    __tablename__ = 'energy_expenditure'

    energy_expenditure_id = db.Column(db.Integer, primary_key=True)
    age_min = db.Column(db.SmallInteger)
    age_max = db.Column(db.SmallInteger)
    bmi_category = db.Column(BmiCategory)
    disease = db.Column(Disease(db.Boolean,db.Boolean,db.Boolean,db.Boolean))
    gender = db.Column(Gender)
    sedentary = db.Column(db.Float)
    low_active = db.Column(db.Float)
    active = db.Column(db.Float)
    very_active = db.Column(db.Float)
    age_para = db.Column(db.Float)
    weight_para = db.Column(db.Float)
    height_para = db.Column(db.Float)
    cons_para = db.Column(db.Float)


class Food(db.Model):
    __tablename__ = 'food'

    food_id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(50))
    healthy_score = db.Column(db.Float)
    tasty_score = db.Column(db.Float)
    restaurant_id = db.Column(db.ForeignKey('restaurant.restaurant_id'), nullable=False)
    energy = db.Column(db.Float, nullable=False)
    carb = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    alcohol = db.Column(db.Float)
    water = db.Column(db.Float)
    fiber = db.Column(db.Float)
    linoacid = db.Column(db.Float)
    alphalinoacid = db.Column(db.Float)
    calcium = db.Column(db.Float)
    chromium = db.Column(db.Float)
    copper = db.Column(db.Float)
    fluoride = db.Column(db.Float)
    iodine = db.Column(db.Float)
    iron = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    manganese = db.Column(db.Float)
    molybdenum = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    sat_fat = db.Column(db.Float)
    selenium = db.Column(db.Float)
    zinc = db.Column(db.Float)
    potassium = db.Column(db.Float)
    sodium = db.Column(db.Float)
    chloride = db.Column(db.Float)
    vita = db.Column(db.Float)
    vitc = db.Column(db.Float)
    vitd = db.Column(db.Float)
    vite = db.Column(db.Float)
    vitk = db.Column(db.Float)
    thiamin = db.Column(db.Float)
    riboflavin = db.Column(db.Float)
    niacin = db.Column(db.Float)
    vitb6 = db.Column(db.Float)
    vitfolate = db.Column(db.Float)
    vitb12 = db.Column(db.Float)
    panacid = db.Column(db.Float)
    biotin = db.Column(db.Float)
    cholin = db.Column(db.Float)

    restaurant = db.relationship('Restaurant')


class HpbFocosFood(db.Model):
    __tablename__ = 'hpb_focos_food'

    food_id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.Text)
    food_group = db.Column(db.String(50))
    food_subgroup = db.Column(db.String(100))
    serving_unit = db.Column(db.String(20))
    serving_gram = db.Column(db.Float)
    healthy_score = db.Column(db.Float)
    tasty_score = db.Column(db.Float)
    restaurant_id = db.Column(db.ForeignKey('restaurant.restaurant_id'), nullable=False)
    energy = db.Column(db.Float, nullable=False)
    carb = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    alcohol = db.Column(db.Float)
    water = db.Column(db.Float)
    fiber = db.Column(db.Float)
    linoacid = db.Column(db.Float)
    alphalinoacid = db.Column(db.Float)
    calcium = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    chromium = db.Column(db.Float)
    copper = db.Column(db.Float)
    fluoride = db.Column(db.Float)
    iodine = db.Column(db.Float)
    iron = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    manganese = db.Column(db.Float)
    molybdenum = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    sat_fat = db.Column(db.Float)
    selenium = db.Column(db.Float)
    zinc = db.Column(db.Float)
    potassium = db.Column(db.Float)
    sodium = db.Column(db.Float)
    chloride = db.Column(db.Float)
    vita = db.Column(db.Float)
    vitc = db.Column(db.Float)
    vitd = db.Column(db.Float)
    vite = db.Column(db.Float)
    vitk = db.Column(db.Float)
    thiamin = db.Column(db.Float)
    riboflavin = db.Column(db.Float)
    niacin = db.Column(db.Float)
    vitb6 = db.Column(db.Float)
    vitfolate = db.Column(db.Float)
    vitb12 = db.Column(db.Float)
    panacid = db.Column(db.Float)
    biotin = db.Column(db.Float)
    cholin = db.Column(db.Float)

    restaurant = db.relationship('Restaurant')


class FoodAndImage(db.Model):
    __tablename__ = 'food_and_image'

    food_and_image_id = db.Column(db.Integer, primary_key=True)
    intake_id = db.Column(db.ForeignKey('food_intake.intake_id'), nullable=False)
    image_id = db.Column(db.ForeignKey('intake_image.image_id'), nullable=False)

    image = db.relationship('IntakeImage')
    intake = db.relationship('FoodIntake')


class FoodIntake(db.Model):
    __tablename__ = 'food_intake'

    intake_id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.ForeignKey('meal_info.meal_id'), nullable=False)
    food_id = db.Column(db.ForeignKey('food.food_id'), nullable=False)
    food_mass = db.Column(db.Float)
    intake_location = db.Column(GeoCoordinate(db.Numeric(8,5),db.Numeric(8,5)))
    logging_way = db.Column(LoggingWay)
    recom_flag = db.Column(db.Boolean)
    done_flag = db.Column(db.Boolean)

    food = db.relationship('Food')
    meal = db.relationship('MealInfo')


class FoodScoreNutrient(db.Model):
    __tablename__ = 'food_score_nutrient'

    score_nutrient_name = db.Column(db.String(20), primary_key=True)
    nutrient_dv = db.Column(db.Numeric(8, 2))
    recommend = db.Column(db.Boolean)


class GoalNutrient(db.Model):
    __tablename__ = 'goal_nutrient'

    goal_nutrient_id = db.Column(db.Integer, primary_key=True)
    age_min = db.Column(db.SmallInteger)
    age_max = db.Column(db.SmallInteger)
    gender = db.Column(Gender)
    water = db.Column(db.Float)
    fiber = db.Column(db.Float)
    linoacid = db.Column(db.Float)
    alphalinoacid = db.Column(db.Float)
    calcium = db.Column(db.Float)
    chromium = db.Column(db.Float)
    copper = db.Column(db.Float)
    fluoride = db.Column(db.Float)
    iodine = db.Column(db.Float)
    iron = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    manganese = db.Column(db.Float)
    molybdenum = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    selenium = db.Column(db.Float)
    zinc = db.Column(db.Float)
    potassium = db.Column(db.Float)
    sodium = db.Column(db.Float)
    chloride = db.Column(db.Float)
    vita = db.Column(db.Float)
    vitc = db.Column(db.Float)
    vitd = db.Column(db.Float)
    vite = db.Column(db.Float)
    vitk = db.Column(db.Float)
    thiamin = db.Column(db.Float)
    riboflavin = db.Column(db.Float)
    niacin = db.Column(db.Float)
    vitb6 = db.Column(db.Float)
    vitfolate = db.Column(db.Float)
    vitb12 = db.Column(db.Float)
    panacid = db.Column(db.Float)
    biotin = db.Column(db.Float)
    cholin = db.Column(db.Float)
    disease = db.Column(Disease(db.Boolean, db.Boolean, db.Boolean, db.Boolean))


class IntakeImage(db.Model):
    __tablename__ = 'intake_image'

    image_id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.ForeignKey('food.food_id'), nullable=False)
    url = db.Column(db.Text)

    food = db.relationship('Food')
    intakes = db.relationship('FoodIntake', secondary='food_and_image')


class MealInfo(db.Model):
    __tablename__ = 'meal_info'

    meal_id = db.Column(db.Integer, primary_key=True)
    meal_time = db.Column(db.DateTime)
    user_id = db.Column(db.ForeignKey('user_profile.user_id'), nullable=False)
    meal_plan_id = db.Column(db.ForeignKey('meal_plan.meal_plan_id'), nullable=False)
    restaurant_id = db.Column(db.ForeignKey('restaurant.restaurant_id'), nullable=False)

    meal_plan = db.relationship('MealPlan')
    restaurant = db.relationship('Restaurant')
    user = db.relationship('UserProfile')


class MealPlan(db.Model):
    __tablename__ = 'meal_plan'

    meal_plan_id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(50))
    meal_plan_time = db.Column(db.Time)
    meal_reminder = db.Column(db.Boolean)
    user_id = db.Column(db.ForeignKey('user_profile.user_id'), nullable=False)

    user = db.relationship('UserProfile')


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    restaurant_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(GeoCoordinate(db.Numeric(8,5),db.Numeric(8,5)))
    phone_no = db.Column(db.String(20))
    name = db.Column(db.String(50))
    address = db.Column(db.Text)


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    user_id = db.Column(db.Integer, primary_key=True, index=True)
    user_name = db.Column(db.String(20))
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    gender = db.Column(Gender)
    birthday = db.Column(db.Date)
    age = db.Column(db.SmallInteger)
    race = db.Column(Race)
    disease = db.Column(Disease(db.Boolean,db.Boolean,db.Boolean,db.Boolean))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    bmi = db.Column(db.Float)
    bmi_category = db.Column(BmiCategory)
    activity_level = db.Column(ActivityLevel)
    energy_expenditure = db.Column(db.Float)
    start_weight = db.Column(db.Float) 
    goal_weight = db.Column(db.Float)
    weight_change_speed = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    duration = db.Column(db.SmallInteger)
    daily_goal_energy = db.Column(db.Float)
    min_carb_need = db.Column(db.Float)
    max_carb_need = db.Column(db.Float)
    min_protein_need = db.Column(db.Float)
    max_protein_need = db.Column(db.Float)
    min_fat_need = db.Column(db.Float)
    max_fat_need = db.Column(db.Float)
    max_alcohol_need = db.Column(db.Float)
    water = db.Column(db.Float)
    fiber = db.Column(db.Float)
    linoacid = db.Column(db.Float)
    alphalinoacid = db.Column(db.Float)
    calcium = db.Column(db.Float)
    chromium = db.Column(db.Float)
    copper = db.Column(db.Float)
    fluoride = db.Column(db.Float)
    iodine = db.Column(db.Float)
    iron = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    manganese = db.Column(db.Float)
    molybdenum = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    selenium = db.Column(db.Float)
    zinc = db.Column(db.Float)
    potassium = db.Column(db.Float)
    sodium = db.Column(db.Float)
    chloride = db.Column(db.Float)
    vita = db.Column(db.Float)
    vitc = db.Column(db.Float)
    vitd = db.Column(db.Float)
    vite = db.Column(db.Float)
    vitk = db.Column(db.Float)
    thiamin = db.Column(db.Float)
    riboflavin = db.Column(db.Float)
    niacin = db.Column(db.Float)
    vitb6 = db.Column(db.Float)
    vitfolate = db.Column(db.Float)
    vitb12 = db.Column(db.Float)
    panacid = db.Column(db.Float)
    biotin = db.Column(db.Float)
    cholin = db.Column(db.Float)

