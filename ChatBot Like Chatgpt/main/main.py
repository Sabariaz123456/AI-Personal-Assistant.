import streamlit as st
import wikipedia
import requests
import datetime

# --------------- Weather Function ------------------

def get_weather(city):
    api_key = "e36fe9eaffd36b46448ac109694cd436"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return "❌ City not found."

    try:
        name = response['name']
        country = response['sys']['country']
        temp = response['main']['temp']
        feels_like = response['main']['feels_like']
        desc = response['weather'][0]['description'].capitalize()
        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']

        explanation = f"""
        📍 **Location**: {name}, {country}  
        🌡️ **Temperature**: {temp}°C (Feels like {feels_like}°C)  
        🌤️ **Condition**: {desc}  
        💨 **Wind Speed**: {wind_speed} m/s  
        💧 **Humidity**: {humidity}%  
        """

        return explanation
    except Exception:
        return "⚠️ Error fetching weather details."

# --------------- Wikipedia Function ------------------

def wikipedia_search(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        return "❌ Topic not found."

def greet():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "🌅 Good Morning!"
    elif 12 <= hour < 18:
        return "☀️ Good Afternoon!"
    else:
        return "🌙 Good Evening!"

# --------------- Page Setup ------------------

st.set_page_config(page_title="AI Personal Assistant", page_icon="🤖", layout="centered")

# --------------- Dark Theme Friendly Custom CSS ------------------

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }

    .title {
        text-align: center;
        font-size: 2.2em;
        font-weight: bold;
        margin-bottom: 10px;
        color: var(--text-color);
    }

    .box {
        background-color: var(--background-secondary);
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 0 15px rgba(100, 100, 100, 0.15);
        margin-top: 15px;
        color: var(--text-color);
    }

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        background-color: var(--background-secondary);
        color: var(--text-color);
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------- Header ------------------

st.markdown('<div class="title">🤖 AI Personal Assistant</div>', unsafe_allow_html=True)
st.markdown(f"<div class='box'><h4>{greet()}</h4></div>", unsafe_allow_html=True)

# --------------- Instructions ------------------

with st.expander("📘 How to use this Assistant?"):
    st.markdown("""
    - Select a feature from below
    - Use **Weather**, **Wikipedia**, **To-Do**, **Notes**, or **Time** tools
    - Clean & minimal design works in dark and light modes
    """)

# --------------- Task Selector ------------------

task = st.selectbox("🧠 What would you like to do?", [
    "Select",
    "🌤️ Get Weather",
    "📘 Search Wikipedia",
    "📝 To-Do List",
    "📌 Quick Notes",
    "🕒 Date & Time"
])

# --------------- Features ------------------

if task == "🌤️ Get Weather":
    city = st.text_input("🏙️ Enter city name:")
    if city:
        result = get_weather(city)
        st.markdown(f"<div class='box'>{result}</div>", unsafe_allow_html=True)

elif task == "📘 Search Wikipedia":
    topic = st.text_input("🔎 Enter a topic:")
    if topic:
        result = wikipedia_search(topic)
        st.markdown(f"<div class='box'>📄 {result}</div>", unsafe_allow_html=True)

elif task == "📝 To-Do List":
    st.markdown("**📋 Your Tasks**")
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    new_task = st.text_input("➕ Add a new task:")
    if st.button("Add Task"):
        if new_task:
            st.session_state.tasks.append(new_task)
            st.success("Task added!")

    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            if st.checkbox(task, key=f"task_{i}"):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()

elif task == "📌 Quick Notes":
    st.markdown("**📝 Write a note:**")
    note = st.text_area("Type here:", height=120)
    if st.button("💾 Save Note"):
        st.session_state.saved_note = note
        st.success("Note saved!")

    if "saved_note" in st.session_state:
        st.markdown(f"<div class='box'><b>📎 Your Note:</b><br>{st.session_state.saved_note}</div>", unsafe_allow_html=True)

elif task == "🕒 Date & Time":
    now = datetime.datetime.now()
    st.markdown(f"""
    <div class='box'>
    📅 <b>Date:</b> {now.strftime('%A, %d %B %Y')}  
    ⏰ <b>Time:</b> {now.strftime('%I:%M %p')}
    </div>
    """, unsafe_allow_html=True)

# --------------- Footer ------------------

st.markdown("---")
st.caption("🛠️ Made by Saba Muhammad Riaz❤️ with Streamlit, and OpenAI")

