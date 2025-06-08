import streamlit as st
from outfit_analysis import encode_image, analyze_outfit_with_gpt4o

# Initialize session state
if "history" not in st.session_state:
    st.session_state["history"] = []
if "current_analysis" not in st.session_state:
    st.session_state["current_analysis"] = None
if "current_image_bytes" not in st.session_state:
    st.session_state["current_image_bytes"] = None
if "current_caption" not in st.session_state:
    st.session_state["current_caption"] = None

st.set_page_config(page_title="AI Stylist", layout="centered")
st.title("🧠 AI Stylist")
st.write("Upload an outfit photo and get real-time style feedback using GPT-4o Vision.")

uploaded_file = st.file_uploader("Upload your outfit photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Your uploaded outfit", use_container_width=True)
    if st.button("Analyze Outfit"):
        with st.spinner("Analyzing your outfit..."):
            try:
                base64_image = encode_image(uploaded_file)
                result = analyze_outfit_with_gpt4o(base64_image)
                # If there is a current analysis, save it to history before overwriting
                if st.session_state["current_analysis"] is not None:
                    st.session_state["history"].append({
                        "image_bytes": st.session_state["current_image_bytes"],
                        "caption": st.session_state["current_caption"],
                        "feedback": st.session_state["current_analysis"]
                    })
                # Update current analysis
                st.session_state["current_analysis"] = result
                st.session_state["current_image_bytes"] = uploaded_file.getvalue()
                st.session_state["current_caption"] = uploaded_file.name
            except Exception as e:
                st.error(f"Error: {e}")

# Show current analysis if it exists
if st.session_state["current_analysis"]:
    st.subheader("✨ Style Feedback")
    st.markdown(st.session_state["current_analysis"])

# Show previous analyses
if st.session_state["history"]:
    st.markdown("---")
    st.subheader("🕑 Previous Analyses")
    for entry in reversed(st.session_state["history"]):
        st.image(entry["image_bytes"], caption=entry["caption"], use_container_width=True)
        st.markdown(entry["feedback"])
        st.markdown("---")
