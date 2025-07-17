from dotenv import load_dotenv
import os
#Storing api key in .env and calling it
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

#Gemini ai client setup
import google.generativeai as genai
genai.configure(api_key=api_key)
client = genai.GenerativeModel("gemini-2.5-flash")

#Taking inputs from user
age=int(input("Enter age in years: "))
weight=int(input("Enter weight in kgs: "))
height=int(input("Enter height in cms: "))
activity_level=input("Enter activity level: [sedentary or moderately active or very active]: ")
diet_preference=input("Enter diet preference: [vegetarian or vegan or protein or low-carb or keto or kosher or halal]: ") 
fitness_goals=input("Enter your fitness goal: [balanced diet or weight loss or increase muscle mass or increase endurance/strength or increase flexibility]: ")

#Dictionary storing user data
user_profile={"age":age,"weight":weight,"height":height,"activity_level":activity_level,
              "diet_preference":diet_preference,"fitness_goals":fitness_goals}

#GPT calling function
def askAI(prompt):
    response = client.generate_content(prompt)
    return response.text.strip()

#Meal plan generating function
def meal_plan_generator(user_profile):
    prompt=f"""You are a nutrition expert. Provide customized and complete meal plans (breakfast, lunch, dinner, snacks) 
    per day for a week with macronutrient breakdowns based on the given user profile below:

    user profile: {user_profile}
    In user profile, age is in years, weight is in kgs and height is in cms
    """
    result=askAI(prompt)
    print(f"\nMeal Plan is \n{result}")
    return result

#Fitness plan generating function
def fitness_plan_generator(user_profile):
    prompt=f"""You are a fitness planning expert. Provide a tailored and detailed fitness plan 
    (with warm-up, main routine, and cool-down) per day for a week based on the user profile given below:


    user profile: {user_profile}
    In user profile, age is in years, weight is in kgs and height is in cms
    """
    result=askAI(prompt)
    print(f"\n\nFitness Plan is \n{result}")
    return result

#Combined weekly health plan generating function
def weekly_health_plan_generator(meal_plan,fitness_plan):
    prompt=f"""You are an expert plans integrator. Provide a comprehensive weekly health plan by combining the meal plan and fitness plan given below.
    Also add consistency and motivation tips for each day into the daily plans.
    meal plan: {meal_plan}
    fitness plan: {fitness_plan}
    """
    result=askAI(prompt)
    return result

#Runner function of all above functions
from concurrent.futures import ThreadPoolExecutor
def runner_fn(user_profile):
    agent_funcions=[meal_plan_generator,fitness_plan_generator]
    plans=[]
    with ThreadPoolExecutor() as executor:
        results=executor.map(lambda fn:fn(user_profile),agent_funcions)
    for result in results:
        plans.append(result)
    #meal_plan=meal_plan_generator(user_profile)
    #fitness_plan=fitness_plan_generator(user_profile)
    weekly_health_plan=weekly_health_plan_generator(plans[0],plans[1])
    return weekly_health_plan

final_weekly_health_plan=runner_fn(user_profile)
print(f"\n\nCombined Weekly Plan is\n{final_weekly_health_plan}")