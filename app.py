import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="MN ELA Question Generator", page_icon="📚", layout="centered")

st.title("📚 MN 2020 ELA Question Generator")
st.write("Generate differentiated question sets mapped to Minnesota 2020 ELA Performance Level Descriptors (PLDs).")

# Sidebar Configuration
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
st.sidebar.markdown("[Get a free Gemini API Key](https://aistudio.google.com/app/apikey)")

# Data for standards 4-9
grade = st.selectbox("Select Grade Level:", ["Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8"])

# Multi-select benchmarks
benchmarks = st.multiselect(
    "Select MN 2020 ELA Benchmark(s):",
    [
        "Standard 4: Craft & Structure - Word Meanings & Nuances",
        "Standard 5: Craft & Structure - Text Structure & Organization",
        "Standard 6: Craft & Structure - Author's Point of View / Purpose",
        "Standard 7: Integration of Knowledge - Multimodal Content Analysis",
        "Standard 8: Integration of Knowledge - Evaluating Arguments & Evidence",
        "Standard 9: Integration of Knowledge - Comparative Text Analysis"
    ]
)

passage = st.text_area("Reading Passage / Text:", height=200, placeholder="Paste your passage here...")

if st.button("Generate PLD Question Set", type="primary"):
    if not api_key:
        st.error("Please provide a Gemini API key in the sidebar.")
    elif not benchmarks or not passage:
        st.warning("Please select at least one benchmark and enter a reading passage.")
    else:
        with st.spinner("Generating questions..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are an expert MN ELA teacher. Create a question set for {grade}.
                Selected Benchmarks: {', '.join(benchmarks)}
                Passage Text: {passage}

                Generate questions across three Performance Level Descriptors (PLDs):
                1. Partially Meets Standard (Literal comprehension, basic identification)
                2. Meets Standard (Inferential comprehension, standard analysis)
                3. Exceeds Standard (Complex synthesis, critical analysis)

                For each level include:
                - 2 Multiple Choice Questions (with options A-D and correct answer labeled)
                - 1 Open-Ended Question
                - 2 Discussion Questions
                Include expected student answers / rubrics for each item.
                """
                
                response = model.generate_content(prompt)
                st.success("Successfully generated!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
