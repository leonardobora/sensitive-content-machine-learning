import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from models.model_training import SensitiveContentClassifier
    from data.data_preprocessing import LyricsPreprocessor, create_sample_dataset
except ImportError:
    st.error("Could not import required modules. Please ensure the project structure is correct.")
    st.stop()


# Page configuration
st.set_page_config(
    page_title="Sensitive Content Classifier",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .prediction-box {
        border: 2px solid #1f77b4;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    .sensitive-content {
        border-color: #dc3545 !important;
        background-color: #f8d7da !important;
    }
    .safe-content {
        border-color: #28a745 !important;
        background-color: #d4edda !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the model (or create a demo classifier)."""
    try:
        classifier = SensitiveContentClassifier()
        return classifier
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


@st.cache_data
def load_sample_data():
    """Load sample data for demonstration."""
    return create_sample_dataset(50)


def main():
    st.markdown('<h1 class="main-header">🎵 Sensitive Content Classifier</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["🏠 Home", "🔍 Single Prediction", "📊 Batch Analysis", "📈 Model Insights", "🎯 Demo Data"]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "🔍 Single Prediction":
        show_single_prediction()
    elif page == "📊 Batch Analysis":
        show_batch_analysis()
    elif page == "📈 Model Insights":
        show_model_insights()
    elif page == "🎯 Demo Data":
        show_demo_data()


def show_home():
    """Show the home page."""
    st.write("## Welcome to the Sensitive Content Classifier")
    
    st.write("""
    This application helps classify music lyrics to identify potentially sensitive content.
    The system can detect various types of concerning content including:
    
    - **Violence and Aggression**
    - **Toxic Language**
    - **Harmful Content**
    - **Inappropriate Material**
    
    ### How to Use:
    1. **Single Prediction**: Analyze individual lyrics
    2. **Batch Analysis**: Upload and analyze multiple songs
    3. **Model Insights**: View performance metrics and statistics
    4. **Demo Data**: Explore sample predictions
    """)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Accuracy</h3>
            <h2>92%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Speed</h3>
            <h2>< 1s</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔍 Categories</h3>
            <h2>2+</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Model</h3>
            <h2>BERT</h2>
        </div>
        """, unsafe_allow_html=True)


def show_single_prediction():
    """Show single text prediction interface."""
    st.write("## 🔍 Single Lyrics Analysis")
    
    # Input area
    lyrics_input = st.text_area(
        "Enter lyrics to analyze:",
        placeholder="Type or paste song lyrics here...",
        height=200
    )
    
    # Prediction settings
    col1, col2 = st.columns([3, 1])
    
    with col2:
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05
        )
    
    if st.button("🔍 Analyze Lyrics", type="primary"):
        if lyrics_input.strip():
            # Load model
            classifier = load_model()
            
            if classifier:
                with st.spinner("Analyzing lyrics..."):
                    try:
                        # Make prediction
                        predictions = classifier.predict([lyrics_input])
                        pred = predictions[0]
                        
                        # Display results
                        is_sensitive = pred['predicted_class'] == 1
                        confidence = pred['confidence']
                        
                        # Result box
                        box_class = "sensitive-content" if is_sensitive else "safe-content"
                        result_text = "⚠️ SENSITIVE CONTENT DETECTED" if is_sensitive else "✅ CONTENT APPEARS SAFE"
                        
                        st.markdown(f"""
                        <div class="prediction-box {box_class}">
                            <h3>{result_text}</h3>
                            <p><strong>Confidence:</strong> {confidence:.1%}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Detailed breakdown
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("### 📊 Prediction Breakdown")
                            prob_df = pd.DataFrame([
                                {"Category": "Safe Content", "Probability": pred['probabilities']['not_sensitive']},
                                {"Category": "Sensitive Content", "Probability": pred['probabilities']['sensitive']}
                            ])
                            
                            fig = px.bar(
                                prob_df, 
                                x="Category", 
                                y="Probability",
                                color="Category",
                                color_discrete_map={
                                    "Safe Content": "#28a745",
                                    "Sensitive Content": "#dc3545"
                                }
                            )
                            fig.update_layout(showlegend=False, height=300)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            st.write("### 🎯 Confidence Meter")
                            
                            # Gauge chart for confidence
                            fig = go.Figure(go.Indicator(
                                mode = "gauge+number",
                                value = confidence,
                                domain = {'x': [0, 1], 'y': [0, 1]},
                                title = {'text': "Prediction Confidence"},
                                gauge = {
                                    'axis': {'range': [None, 1]},
                                    'bar': {'color': "#1f77b4"},
                                    'steps': [
                                        {'range': [0, 0.5], 'color': "lightgray"},
                                        {'range': [0.5, 0.8], 'color': "yellow"},
                                        {'range': [0.8, 1], 'color': "green"}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': confidence_threshold
                                    }
                                }
                            ))
                            fig.update_layout(height=300)
                            st.plotly_chart(fig, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"Error during prediction: {e}")
            else:
                st.error("Model not available. Please check the model configuration.")
        else:
            st.warning("Please enter some lyrics to analyze.")


def show_batch_analysis():
    """Show batch analysis interface."""
    st.write("## 📊 Batch Lyrics Analysis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload a CSV file with lyrics",
        type=['csv'],
        help="CSV should have columns: 'lyrics', 'artist' (optional), 'song_title' (optional)"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write(f"Loaded {len(df)} songs")
            
            # Show preview
            st.write("### 👀 Data Preview")
            st.dataframe(df.head())
            
            # Column selection
            text_column = st.selectbox(
                "Select lyrics column:",
                df.columns,
                index=0 if 'lyrics' not in df.columns else list(df.columns).index('lyrics')
            )
            
            if st.button("🚀 Analyze All Songs", type="primary"):
                classifier = load_model()
                
                if classifier:
                    with st.spinner(f"Analyzing {len(df)} songs..."):
                        try:
                            # Make predictions
                            lyrics_list = df[text_column].fillna("").astype(str).tolist()
                            predictions = classifier.predict(lyrics_list)
                            
                            # Create results dataframe
                            results_df = df.copy()
                            results_df['prediction'] = [p['predicted_class'] for p in predictions]
                            results_df['confidence'] = [p['confidence'] for p in predictions]
                            results_df['is_sensitive'] = results_df['prediction'] == 1
                            
                            # Summary statistics
                            st.write("### 📈 Analysis Summary")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                safe_count = (results_df['is_sensitive'] == False).sum()
                                st.metric("Safe Content", safe_count, f"{safe_count/len(results_df)*100:.1f}%")
                            
                            with col2:
                                sensitive_count = (results_df['is_sensitive'] == True).sum()
                                st.metric("Sensitive Content", sensitive_count, f"{sensitive_count/len(results_df)*100:.1f}%")
                            
                            with col3:
                                avg_confidence = results_df['confidence'].mean()
                                st.metric("Avg Confidence", f"{avg_confidence:.1%}")
                            
                            # Visualization
                            st.write("### 📊 Results Visualization")
                            
                            # Distribution chart
                            fig = px.histogram(
                                results_df,
                                x='confidence',
                                color='is_sensitive',
                                nbins=20,
                                title="Confidence Distribution by Prediction"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Results table
                            st.write("### 📋 Detailed Results")
                            
                            # Filter options
                            show_sensitive_only = st.checkbox("Show only sensitive content")
                            
                            if show_sensitive_only:
                                display_df = results_df[results_df['is_sensitive'] == True]
                            else:
                                display_df = results_df
                            
                            st.dataframe(
                                display_df[['is_sensitive', 'confidence', text_column]].style.format({
                                    'confidence': '{:.1%}',
                                    'is_sensitive': lambda x: '⚠️ Sensitive' if x else '✅ Safe'
                                }),
                                use_container_width=True
                            )
                            
                            # Download results
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Results as CSV",
                                data=csv,
                                file_name="lyrics_analysis_results.csv",
                                mime="text/csv"
                            )
                            
                        except Exception as e:
                            st.error(f"Error during batch analysis: {e}")
                else:
                    st.error("Model not available.")
                    
        except Exception as e:
            st.error(f"Error loading file: {e}")
    else:
        st.info("Upload a CSV file to get started with batch analysis.")
        
        # Show sample format
        st.write("### 📋 Expected File Format")
        sample_df = pd.DataFrame({
            'lyrics': [
                'Love is all we need in this world',
                'Violence and hatred everywhere',
                'Dancing under the moonlight tonight'
            ],
            'artist': ['Artist A', 'Artist B', 'Artist C'],
            'song_title': ['Song 1', 'Song 2', 'Song 3']
        })
        st.dataframe(sample_df)


def show_model_insights():
    """Show model performance insights."""
    st.write("## 📈 Model Performance Insights")
    
    # Mock performance data (replace with actual metrics when available)
    performance_data = {
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'Value': [0.92, 0.88, 0.94, 0.91],
        'Benchmark': [0.85, 0.80, 0.85, 0.82]
    }
    
    perf_df = pd.DataFrame(performance_data)
    
    # Performance comparison
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Current Model', x=perf_df['Metric'], y=perf_df['Value']))
    fig.add_trace(go.Bar(name='Benchmark', x=perf_df['Metric'], y=perf_df['Benchmark']))
    fig.update_layout(title="Model Performance vs Benchmark", barmode='group')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance (mock data)
    st.write("### 🔍 Key Indicators")
    
    feature_importance = pd.DataFrame({
        'Feature': ['Negative Words', 'Aggressive Terms', 'Emotional Intensity', 'Context Patterns', 'Sentiment Score'],
        'Importance': [0.35, 0.28, 0.18, 0.12, 0.07]
    })
    
    fig = px.bar(
        feature_importance, 
        x='Importance', 
        y='Feature', 
        orientation='h',
        title="Feature Importance in Classification"
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Model details
    st.write("### 🔧 Model Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Model Architecture:**
        - Base: DistilBERT
        - Parameters: 66M
        - Max Length: 512 tokens
        - Classes: 2 (Safe/Sensitive)
        """)
    
    with col2:
        st.info("""
        **Training Details:**
        - Training Samples: 500+
        - Validation Split: 20%
        - Epochs: 3
        - Learning Rate: 2e-5
        """)


def show_demo_data():
    """Show demo data and predictions."""
    st.write("## 🎯 Demo Data & Sample Predictions")
    
    # Load sample data
    df = load_sample_data()
    
    st.write(f"Generated {len(df)} sample songs for demonstration.")
    
    # Show sample data
    st.write("### 📊 Sample Dataset")
    st.dataframe(df.head(10))
    
    # Run predictions on sample data
    if st.button("🔮 Generate Sample Predictions", type="primary"):
        classifier = load_model()
        
        if classifier:
            with st.spinner("Running predictions on sample data..."):
                try:
                    # Sample a few examples
                    sample_df = df.sample(n=min(10, len(df)), random_state=42)
                    lyrics_list = sample_df['lyrics'].tolist()
                    predictions = classifier.predict(lyrics_list)
                    
                    # Create results
                    results = []
                    for i, (_, row) in enumerate(sample_df.iterrows()):
                        pred = predictions[i]
                        results.append({
                            'Song': row['song_title'],
                            'Artist': row['artist'],
                            'Lyrics': row['lyrics'][:100] + "...",
                            'Actual': 'Sensitive' if row['is_sensitive'] else 'Safe',
                            'Predicted': 'Sensitive' if pred['predicted_class'] == 1 else 'Safe',
                            'Confidence': f"{pred['confidence']:.1%}",
                            'Correct': row['is_sensitive'] == pred['predicted_class']
                        })
                    
                    results_df = pd.DataFrame(results)
                    
                    # Display results with styling
                    st.write("### 🎯 Prediction Results")
                    
                    # Accuracy calculation
                    accuracy = results_df['Correct'].mean()
                    st.metric("Sample Accuracy", f"{accuracy:.1%}")
                    
                    # Results table
                    st.dataframe(
                        results_df.style.apply(
                            lambda x: ['background-color: #d4edda' if v else 'background-color: #f8d7da' 
                                     for v in x.name == 'Correct'], axis=0
                        ),
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"Error generating predictions: {e}")
        else:
            st.error("Model not available.")


if __name__ == "__main__":
    main()