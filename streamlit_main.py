import streamlit as st
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai

# Load .env locally
load_dotenv()

# Get API Key from Streamlit secrets or .env
# Try secrets first, fallback to .env
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in st.secrets or .env")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
client = genai.GenerativeModel("gemini-2.5-flash")

# Gemini query function
def askAI(prompt):
    response = client.generate_content(prompt)
    return response.text.strip()

# Meal Plan Generator
def meal_plan_generator(user_profile):
    prompt = f"""
    You are a nutrition expert. Provide customized and complete meal plans (breakfast, lunch, dinner, snacks) 
    per day for a week with macronutrient breakdowns based on the given user profile below:

    user profile: {user_profile}
    In user profile, age is in years, weight in kgs, height in cms.
    """
    return askAI(prompt)

# Fitness Plan Generator
def fitness_plan_generator(user_profile):
    prompt = f"""
    You are a fitness planning expert. Provide a tailored and detailed fitness plan 
    (with warm-up, main routine, and cool-down) per day for a week based on the user profile:

    user profile: {user_profile}
    In user profile, age is in years, weight in kgs, height in cms.
    """
    return askAI(prompt)

# Weekly Health Plan Generator
def weekly_health_plan_generator(meal_plan, fitness_plan):
    prompt = f"""
    You are an expert plans integrator. Provide a comprehensive weekly health plan by combining the meal plan and fitness plan given below.
    Also add consistency and motivation tips for each day into the daily plans.

    meal plan: {meal_plan}
    fitness plan: {fitness_plan}
    """
    return askAI(prompt)

# Run all agents in parallel
def runner_fn(user_profile):
    agent_functions = [meal_plan_generator, fitness_plan_generator]
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda fn: fn(user_profile), agent_functions))
    return weekly_health_plan_generator(results[0], results[1])

# Streamlit UI
st.set_page_config(page_title="Weekly Health Plan", layout="centered")
st.title("🌱 Health Mate")

with st.sidebar:
    st.header("🧑‍⚕️ User Profile")

    age = st.number_input("Age (years)", min_value=10, max_value=100, value=30)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=50)
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=150)

    activity_level = st.selectbox("Activity Level", 
                                  ["sedentary", "moderately active", "very active"])
    diet_preference = st.selectbox("Diet Preference", 
                                   ["vegetarian", "vegan", "protein", "low-carb", "keto", "kosher", "halal"])
    fitness_goals = st.selectbox("Fitness Goal", 
                                 ["balanced diet", "weight loss", "increase muscle mass", "increase endurance or strength","increase flexibility"])
    
    generate = st.button("🚀 Generate Plan")

if generate:
    user_profile = {
        "age": age,
        "weight": weight,
        "height": height,
        "activity_level": activity_level,
        "diet_preference": diet_preference,
        "fitness_goals": fitness_goals
    }

    with st.spinner("Generating personalized health plan... please wait ⏳"):
        weekly_plan = runner_fn(user_profile)

    st.success("✅ Your Weekly Health Plan is Ready!")
    st.markdown("### 📋 Weekly Health Plan")
    st.markdown(weekly_plan)
