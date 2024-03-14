import streamlit as st

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
    layout="wide"
)

# Header of the page
st.markdown("<h1 style='text-align: center;'>Welcome to Legal Pathfinder</h1>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center;'>In this website we can provide the following support</div>
""", unsafe_allow_html=True)

st.sidebar.success("Please select your legal service")

# Create two columns for the Legal Assistant and Legal Revisor sections
col1, col2 = st.columns(2)

# Legal Assistant Section
with col1:
    st.header("Legal Assistant")
    st.write("Lorem ipsum dolor sit amet. Est laudantium doloribus non voluptatum quae et accusamus fuga quo molestiae cumque id provident consequatur qui esse eveniet id perspiciatis iusto. Vel blanditiis esse est nihil facere qui galisum tenetur. Ea necessitatibus laborum a facere iste nam enim rerum rem provident.Quis ut laudantium dignissimos et similique ullam et velite nobis?")

# Legal Revisor Section
with col2:
    st.header("Legal Revisor")
    st.write("Lorem ipsum dolor sit amet. Est laudantium doloribus non voluptatum quae et accusamus fuga quo molestiae cumque id provident consequatur qui esse eveniet id perspiciatis iusto. Vel blanditiis esse est nihil facere qui galisum tenetur. Ea necessitatibus laborum a facere iste nam enim rerum rem provident.Quis ut laudantium dignissimos et similique ullam et velite nobis?")
