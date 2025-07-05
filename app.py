import streamlit as st
from datetime import date
from src.workflow import workflow
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Smart Trip Planner", layout="centered")

st.title("🧳 Smart Trip Planner")

with st.form("trip_form"):
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", min_value=date.today())
    with col2:
        end_date = st.date_input("End Date", min_value=start_date)
    
    col3, col4 = st.columns(2)
    with col3:
        source = st.text_input("Source", placeholder="e.g., Madurai")
    with col4:
        destination = st.text_input("Destination", placeholder="e.g., Coimbatore")
    
    commute_mode = st.radio(
        "Preferred Mode of Commutation",
        ["Airplane", "Train", "Car"],
        horizontal=True
    )

    lodging_required = st.checkbox("Need lodging arrangements?", value=True)

    submitted = st.form_submit_button("Submit")

# ---- On Submit ----
if submitted:
    with st.spinner("🛠️ Planning your trip..."):
        # Combine inputs into a user-style prompt
        user_question = (
            f"Suggest me an itinerary from {start_date.strftime('%B %d')} to "
            f"{end_date.strftime('%B %d')} for a trip to {destination} from {source}. "
            f"I prefer to travel by {commute_mode.lower()}. "
            f"{'I need' if lodging_required else 'I do not need'} lodging arrangements."
        )
        print(f"app.py - user_question: {user_question}")
        app = workflow()
        message = [HumanMessage(content=user_question)]
        response = app.invoke({"messages":message})
        #print(f"app.py - response: {response["messages"][-1]}")
        
        final_output = response["messages"][-1].content
        st.success("✅ Trip plan ready!")
        try:
            import json
            parsed = json.loads(final_output)
            
            st.markdown("### 📌 Tourist Attractions & Activities")
            st.write(parsed.get("attactions_activities", "Not available"))

            st.markdown("### 🏨 Lodging Options")
            st.write(parsed.get("lodging_choices", "Not available"))

            st.markdown("### 🚕 Local Transportation")
            st.write(parsed.get("local_transport", "Not available"))

            st.markdown("### 🌤️ Temperature-Based Suggestion")
            st.info(parsed.get("weather_details", "No weather comment available"))
            
            st.markdown("### 🌤️ Itenary")
            st.info(parsed.get("itenary", "Not available"))

        except Exception as e:
            st.error(f"❌ Failed to parse response. Check the format.\n\nError: {e}")
            st.code(final_output)

