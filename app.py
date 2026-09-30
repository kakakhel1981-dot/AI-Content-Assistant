import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts for any social platform in seconds using Groq API.")

# Sidebar for API Key configuration
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
st.sidebar.markdown("[Get a free Groq API Key](https://console.groq.com/keys)")

# User Selection Inputs
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Twitter / X", "Instagram", "Facebook", "Blog Post"]
    )
    content_type = st.selectbox(
        "Content Type",
        ["Educational", "Promotional", "Storytelling", "Announcement", "Thought Leadership"]
    )

with col2:
    tone = st.selectbox(
        "Tone of Voice",
        ["Professional", "Casual & Friendly", "Witty & Humorous", "Inspirational", "Urgent & Direct"]
    )
    target_audience = st.text_input("Target Audience", placeholder="e.g., Tech Founders, College Students")

topic = st.text_area("Topic / Main Idea", placeholder="e.g., Why learning Python in 2026 is still the best decision for beginners.")

# Generate Content Button
if st.button("🚀 Generate Post", type="primary", use_container_width=True):
    # Validation checks
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=api_key)

            # Construct system and user prompts
            system_prompt = (
                "You are an expert social media strategist and content creator. "
                "Your goal is to write high-engaging, well-formatted content tailored specifically "
                "for the given platform, target audience, and tone."
            )

            user_prompt = f"""
Create a complete post with the following specifications:
- **Platform:** {platform}
- **Content Type:** {content_type}
- **Tone:** {tone}
- **Target Audience:** {target_audience}
- **Topic:** {topic}

**Instructions:**
1. Write a compelling headline/hook tailored for {platform}.
2. Provide the main caption body with appropriate spacing, emojis, and structure suitable for {platform}.
3. End with a strong Call-To-Action (CTA).
4. Include 5-10 relevant and trending hashtags at the end.
"""

            with st.spinner("Generating content via Groq..."):
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                )

                generated_text = response.choices[0].message.content

            # Display Output
            st.success("Post Generated Successfully!")
            st.markdown("### 📝 Generated Post")
            st.markdown(generated_text)

            # Copy/Download capability
            st.download_button(
                label="📥 Download Content as Text",
                data=generated_text,
                file_name="generated_post.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")