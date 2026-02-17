import streamlit as st
import joblib
import pandas as pd
from data_preprocessing import DataPreprocessor
import plotly.graph_objects as go

st.set_page_config(page_title="Fake Review Detector", page_icon="🔍", layout="wide")

@st.cache_resource
def load_model():
    try:
        model = joblib.load('models/svm.pkl')
        preprocessor = joblib.load('models/preprocessor.pkl')
        return model, preprocessor
    except Exception as e:
        return None, None

model, preprocessor = load_model()

st.title("🔍 Fake Product Review Detection System")
st.markdown("### AI-Powered Review Authenticity Checker")

if model is None:
    st.error("⚠️ Model not found. Please train the model first by running: `python main.py`")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Single Review", "Batch Analysis", "About"])

with tab1:
    st.subheader("Analyze Single Review")
    
    review_text = st.text_area("Enter product review:", height=150, 
                                placeholder="Type or paste a product review here...")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_btn = st.button("🔍 Analyze", type="primary")
    
    if analyze_btn and review_text:
        with st.spinner("Analyzing..."):
            df = pd.DataFrame({'review_text': [review_text]})
            X, _ = preprocessor.prepare_data(df, fit=False)
            
            prediction = model.predict(X)[0]
            probability = model.predict_proba(X)[0]
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if prediction == 1:
                    st.error("### 🚨 FAKE REVIEW")
                else:
                    st.success("### ✅ REAL REVIEW")
            
            with col2:
                st.metric("Confidence", f"{max(probability)*100:.1f}%")
            
            with col3:
                st.metric("Fake Probability", f"{probability[1]*100:.1f}%")
            
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability[1]*100,
                title={'text': "Fake Review Probability"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "darkred" if probability[1] > 0.5 else "green"},
                       'steps': [
                           {'range': [0, 30], 'color': "lightgreen"},
                           {'range': [30, 70], 'color': "yellow"},
                           {'range': [70, 100], 'color': "lightcoral"}],
                       'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 50}}))
            
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Batch Review Analysis")
    
    uploaded_file = st.file_uploader("Upload CSV file with reviews", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} reviews")
        
        if 'review_text' not in df.columns:
            st.error("CSV must contain 'review_text' column")
        else:
            if st.button("Analyze All Reviews"):
                with st.spinner("Processing..."):
                    X, _ = preprocessor.prepare_data(df, fit=False)
                    predictions = model.predict(X)
                    probabilities = model.predict_proba(X)
                    
                    df['prediction'] = ['FAKE' if p == 1 else 'REAL' for p in predictions]
                    df['fake_probability'] = probabilities[:, 1]
                    
                    fake_count = sum(predictions)
                    real_count = len(predictions) - fake_count
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Reviews", len(df))
                    col2.metric("Fake Reviews", fake_count, delta=f"{fake_count/len(df)*100:.1f}%")
                    col3.metric("Real Reviews", real_count, delta=f"{real_count/len(df)*100:.1f}%")
                    
                    st.dataframe(df[['review_text', 'prediction', 'fake_probability']], use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button("📥 Download Results", csv, "results.csv", "text/csv")

with tab3:
    st.subheader("About This System")
    st.markdown("""
    ### 🎯 Features
    - **Machine Learning Models**: Logistic Regression, Random Forest, SVM
    - **NLP Techniques**: TF-IDF, Sentiment Analysis, Text Features
    - **Accuracy**: ~94% with SVM model
    
    ### 🔍 Detection Methods
    - Duplicate review detection
    - Rating-sentiment mismatch
    - Suspicious patterns (generic phrases, excessive caps)
    - Text quality analysis
    
    ### 🚀 Technology Stack
    - Python, scikit-learn, NLTK, TextBlob
    - Streamlit for UI
    - Flask for API
    
    ### 📊 Use Cases
    - E-commerce platforms
    - Product review moderation
    - Trust & safety systems
    """)

st.sidebar.title("ℹ️ Information")
st.sidebar.info("This system uses ML and NLP to detect fake product reviews with high accuracy.")
st.sidebar.markdown("### Model Performance")
st.sidebar.metric("Accuracy", "~94%")
st.sidebar.metric("Model", "SVM (RBF)")
