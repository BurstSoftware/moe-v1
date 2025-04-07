import streamlit as st
import google.generativeai as genai
import time

# Define a class for an SEO Expert
class Expert:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def process(self, prompt, api_key):
        # Configure the Google AI Studio API
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')  # Use an available model name
        except Exception as e:
            return (f"{self.name} encountered an error: Failed to configure API - {str(e)}",
                    "", "", "")
        
        # Each expert processes the prompt in their own way
        thought = f"{self.name} is thinking: Analyzing the prompt '{prompt}'..."
        reasoning = f"{self.name} reasons: I will break down the prompt into key components and consult the AI for SEO insights."
        action = f"{self.name} acts: Sending prompt to Google AI Studio API..."

        # Call the Google AI Studio API
        try:
            response = model.generate_content(prompt)
            ai_response = response.text
        except Exception as e:
            ai_response = f"Error: Failed to get a response from the API - {str(e)}"
        
        return thought, reasoning, action, ai_response

# Define a list of SEO experts with descriptions
experts_list = [
    Expert("Technical SEO Expert", "Specializes in optimizing the technical aspects of a website, such as site speed, crawlability, and structured data."),
    Expert("On-Page SEO Expert", "Focuses on optimizing individual web pages through keyword research, meta tags, and internal linking."),
    Expert("Off-Page SEO Expert", "Specializes in building website authority through backlinks, guest posting, and influencer outreach."),
    Expert("Content SEO Expert", "Focuses on creating and optimizing content that aligns with user intent and search engine algorithms."),
    Expert("Local SEO Expert", "Specializes in optimizing for local search results, including Google Business Profile and local citations."),
    Expert("E-Commerce SEO Expert", "Focuses on optimizing online stores to drive traffic and conversions."),
    Expert("International SEO Expert", "Specializes in optimizing websites for multiple regions and languages."),
    Expert("Voice Search SEO Expert", "Focuses on optimizing for voice search queries with conversational language."),
    Expert("SEO Analytics Expert", "Specializes in tracking and analyzing SEO performance using tools like Google Analytics."),
    Expert("AI and SEO Expert", "Focuses on leveraging AI tools and understanding AI-driven search trends for optimization."),
    Expert("Shared SEO Expert", "A generalist that combines knowledge from all SEO domains to provide holistic solutions.")
]

# Streamlit App
st.title("SEO Mixture of Experts System")

# Step 1: Input Google AI Studio API Key
st.header("Step 1: Enter Your Google AI Studio API Key")
api_key = st.text_input("API Key", type="password")
if not api_key:
    st.warning("Please enter your Google AI Studio API key to proceed.")
    st.stop()

# Step 2: Select SEO Experts
st.header("Step 2: Select SEO Experts to Work on Your Prompt")
expert_names = [expert.name for expert in experts_list]
selected_experts = st.multiselect("Choose SEO Experts", expert_names)

# Display descriptions of selected experts
if selected_experts:
    st.subheader("Selected SEO Experts and Their Descriptions")
    for expert_name in selected_experts:
        expert = next(e for e in experts_list if e.name == expert_name)
        st.write(f"**{expert.name}**: {expert.description}")

# Step 3: Input Prompt
st.header("Step 3: Enter Your SEO Prompt")
user_prompt = st.text_area("Your Prompt", "Type your SEO-related prompt here (e.g., 'How can I improve my website’s ranking on Google?')...")

# Step 4: Process with Experts
if st.button("Process Prompt with SEO Experts"):
    if not selected_experts:
        st.error("Please select at least one SEO expert to proceed.")
    elif not user_prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
        st.header("Step 4: SEO Experts' Processing Steps")
        # Create an expander for each expert's thought process
        for expert_name in selected_experts:
            expert = next(e for e in experts_list if e.name == expert_name)
            with st.expander(f"{expert.name}'s Processing"):
                thought, reasoning, action, ai_response = expert.process(user_prompt, api_key)
                st.write(f"**Thought**: {thought}")
                st.write(f"**Reasoning**: {reasoning}")
                st.write(f"**Action**: {action}")
                st.write(f"**AI Response**: {ai_response}")
