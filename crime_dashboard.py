import streamlit as st
import pandas as pd
import plotly.express as px
st.markdown("""
    <style>
    /* Reduce font size of metric label */
    div[data-testid="stMetricValue"] > div {
        font-size: 18px;  /* change this value to whatever you want */
    }
    /* Reduce font size of metric label's label (title) */
    div[data-testid="stMetricLabel"] {
        font-size: 14px;  /* change as needed */
    }
    </style>
    """, unsafe_allow_html=True)

df=pd.read_csv("cleaned_crime_data.csv")
df["REPORTEDDATE"] = pd.to_datetime(df["REPORTEDDATE"], errors="coerce")
st.title("🔍 Steel City Crime Watch") #title
st.markdown("📢 Stay informed about crime in Steel City with our interactive dashboard.")
#sidebars
st.sidebar.title("Refine Your Search:")
months=["All"]+df["REPORTEDMONTH"].unique().tolist()
selected_month=st.sidebar.selectbox("Select Reported Month",months) #1. Reported months
if selected_month != "All":
    filtered_df=df[df["REPORTEDMONTH"]==selected_month]
else:
    filtered_df=df.copy()
offence_cat=["All"]+sorted(filtered_df["NIBRS_OFFENSE_CATEGORY"].unique().tolist())
offence_category=st.sidebar.selectbox("Select Offence Category",offence_cat) #2. Offence category
if offence_category == "All":
    pass
else:
    filtered_df=filtered_df[filtered_df["NIBRS_OFFENSE_CATEGORY"]==offence_category]
against=["All"]+sorted(filtered_df["NIBRS_CRIME_AGAINST"].unique().tolist())
crime_against=st.sidebar.selectbox("Select Crime Against",against) #3. Crime against
if crime_against == "All":
    pass
else:
    filtered_df=filtered_df[filtered_df["NIBRS_CRIME_AGAINST"]==crime_against]
voilation_options=["All"]+sorted(filtered_df["VIOLATION"].unique().tolist())
voilation=st.sidebar.multiselect("Select Violation(s)",voilation_options,default=["All"]) #4. Violation
if "All" in voilation:
    pass
else:
    filtered_df=filtered_df[filtered_df["VIOLATION"].isin(voilation)]
neighbor_option=["All"]+sorted(filtered_df["NEIGHBORHOOD"].unique().tolist())
neighborrhood=st.sidebar.multiselect("Select Neighborhood(s)",neighbor_option,default="All") #5 neighborhood
if "All" in neighborrhood:
    pass
else:
    filtered_df=filtered_df[filtered_df["NEIGHBORHOOD"].isin(neighborrhood)]
#adding KPIs
st.subheader("Key Performance Indicators (KPIs) 🚀")
total_crimes=len(filtered_df)
unique_voilations=filtered_df["VIOLATION"].nunique()
unique_neighbour=filtered_df["NEIGHBORHOOD"].nunique()
unique_offence_cat=filtered_df["NIBRS_OFFENSE_CATEGORY"].nunique()
top_offence=filtered_df["NIBRS_OFFENSE_CATEGORY"].mode()[0] if not filtered_df["NIBRS_OFFENSE_CATEGORY"].mode().empty else "N/A"
top_neighbour=filtered_df["NEIGHBORHOOD"].mode()[0] if not filtered_df["NEIGHBORHOOD"].mode().empty else "N/A"
top_voilation=filtered_df["VIOLATION"].mode()[0] if not filtered_df["VIOLATION"].mode().empty else "N/A"
top_crime_against=filtered_df["NIBRS_CRIME_AGAINST"].mode()[0] if not filtered_df["NIBRS_CRIME_AGAINST"].mode().empty else "N/A"
busiest_month=filtered_df["REPORTEDMONTH"].mode()[0] if not filtered_df["REPORTEDMONTH"].mode().empty else "N/A"
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Crimes",total_crimes)
    st.metric("Unique Violations",unique_voilations)
    st.metric("Unique Neighbourhood",unique_neighbour)
with col2:
    st.metric("Unique Offence Category",unique_offence_cat)
    st.metric("Top Offence",top_offence)
    st.metric("Top Neighbourhood",top_neighbour)
with col3:
    st.metric("Top Violation",top_voilation)
    st.metric("Top Crime Against",top_crime_against)
    st.metric("Busiest Month",busiest_month)
# ================== CHARTS SECTION ==================

st.subheader("📊 Crime Data Visualizations")
# 1. Crimes Reported by Month (Always shown, not affected by filters)
monthly_data = df.groupby("REPORTEDMONTH").size().reset_index(name="Total Incidents")
fig_month = px.line(
    monthly_data,
    x="REPORTEDMONTH",
    y="Total Incidents",
    markers=True,
    title="Crimes Reported by Month",
    line_shape="linear"
)

# Set line color to blue
fig_month.update_traces(line=dict(color='#4A90E2'), marker=dict(color='#4A90E2'))

st.plotly_chart(fig_month, use_container_width=True)
st.caption("📌 Note: This graph displays the total number of crimes reported per month and is not affected by sidebar filters.")


# 2. Top Offense Categories (Shown only when 'All' is selected)
if offence_category == "All":
    category_data = filtered_df["NIBRS_OFFENSE_CATEGORY"].value_counts().nlargest(10).reset_index()
    category_data.columns = ["Offense Category", "Count"]
    
    if not category_data.empty:
        fig_category = px.bar(
            category_data, x="Offense Category", y="Count", text="Count", color="Count",
            title="Top 10 Offense Categories"
        )
        fig_category.update_traces(textposition='outside')
        fig_category.update_layout(xaxis_tickangle=-45, title_font_size=18)
        st.plotly_chart(fig_category, use_container_width=True)
    else:
        st.info("No offense category data available for current filters.")
else:
    st.metric("Selected Offense Category", offence_category)
    st.caption("Chart skipped for specific offense category.")

# 3. Crime Against Type (Shown only when 'All' is selected)
if crime_against == "All":
    crime_against_data = filtered_df["NIBRS_CRIME_AGAINST"].value_counts().reset_index()
    crime_against_data.columns = ["Type", "Count"]

    if not crime_against_data.empty:
        fig_against = px.bar(
            crime_against_data, x="Type", y="Count", text="Count", color="Count",
            title="Crime Against Type"
        )
        fig_against.update_traces(textposition='outside')
        fig_against.update_layout(title_font_size=18)
        st.plotly_chart(fig_against, use_container_width=True)
    else:
        st.info("No crime-against data available for current filters.")
else:
    st.metric("Crime Against", crime_against)
    st.caption("Chart skipped for specific crime type.")

# 4. Top 10 Violations
violation_counts = filtered_df["VIOLATION"].value_counts().nlargest(10).reset_index()
violation_counts.columns = ["Violation", "Count"]

if not violation_counts.empty and len(violation_counts) > 1:
    fig_violations = px.bar(
        violation_counts, x="Count", y="Violation", orientation="h", text="Count", color="Count",
        title="Top 10 Violations", height=400
    )
    fig_violations.update_traces(textposition="outside")
    fig_violations.update_layout(title_font_size=18)
    st.plotly_chart(fig_violations, use_container_width=True)
else:
    st.info("Not enough data to plot top violations.")

# 5. Crime Hotspot Map (Always show if data is available)
st.markdown("### 🗺️ Crime Hotspot Map")

map_df = filtered_df.dropna(subset=['XCOORD', 'YCOORD'])

if not map_df.empty:
    fig_map = px.scatter_mapbox(
        map_df,
        lat="YCOORD",
        lon="XCOORD",
        hover_name="NEIGHBORHOOD",
        hover_data=["VIOLATION", "REPORTEDDATE"],
        zoom=10,
        height=500,
        title="Geographical Distribution of Crimes",
        mapbox_style="open-street-map"
    )
    fig_map.update_layout(title_font_size=18)
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("No geographical data available for the selected filters to display on the map.")
st.subheader("Raw Crime Data Table 📋")
st.markdown("This table displays the original dataset used in this dashboard.")
st.dataframe(df)
st.download_button("Download CSV",data=df.to_csv(index=False,sep=","),file_name="crime_data.csv",mime="text/csv")
