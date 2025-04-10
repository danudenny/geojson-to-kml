import streamlit as st
import json
import simplekml
import base64
import io

st.set_page_config(page_title="Farm Data GeoJSON to KML Converter", page_icon="🌎")

st.title("Farm Data GeoJSON to KML Converter")
st.write("Upload your Farm Data GeoJSON file and convert it to KML format")

def convert_farm_geojson_to_kml(data):
    # Create a new KML document
    kml = simplekml.Kml()
    
    # Check if the data has the expected structure
    if "FarmPolygon" in data and "Data" in data["FarmPolygon"]:
        farm_data = data["FarmPolygon"]["Data"]
    else:
        # Try to process as a list directly
        farm_data = data.get("Data", data)
    
    # Process each farm feature
    for farm in farm_data:
        try:
            # Parse the PolyGeoJson string to a JSON object
            poly_geojson = json.loads(farm.get("PolyGeoJson", "{}"))
            
            # Skip if there's no valid geometry
            if not poly_geojson or "coordinates" not in poly_geojson:
                continue
            
            # Create a name from available attributes
            name_parts = []
            if farm.get("EntityName"):
                name_parts.append(farm["EntityName"].strip())
            if farm.get("PlotDisplayID"):
                name_parts.append(f"Plot: {farm['PlotDisplayID']}")
            if farm.get("CommodityName"):
                name_parts.append(farm["CommodityName"])
                
            name = " - ".join(name_parts) if name_parts else "Unnamed Farm"
            
            # Create a polygon in KML
            polygon = kml.newpolygon(name=name)
            
            # Set coordinates (first array is outer boundary in KML)
            if poly_geojson["type"] == "Polygon" and len(poly_geojson["coordinates"]) > 0:
                polygon.outerboundaryis = poly_geojson["coordinates"][0]
                
                # Add inner boundaries (holes) if they exist
                for i in range(1, len(poly_geojson["coordinates"])):
                    polygon.innerboundaryis.append(poly_geojson["coordinates"][i])
            
            # Add farm properties as description
            description = "<table border='1'>"
            for key, value in farm.items():
                # Skip the PolyGeoJson field since it's redundant in the description
                if key != "PolyGeoJson":
                    description += f"<tr><td><b>{key}</b></td><td>{value}</td></tr>"
            description += "</table>"
            polygon.description = description
            
            # Style the polygon
            polygon.style.linestyle.color = simplekml.Color.blue
            polygon.style.linestyle.width = 2
            polygon.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)
            
        except Exception as e:
            st.warning(f"Skipped one record due to error: {str(e)}")
    
    # Save the KML to a string buffer
    kml_output = io.BytesIO()
    kml.savekmz(kml_output)
    return kml_output.getvalue()

def get_download_link(file_content, file_name):
    b64 = base64.b64encode(file_content).decode()
    return f'<a href="data:application/vnd.google-earth.kmz;base64,{b64}" download="{file_name}">Download KMZ file</a>'

# File uploader for GeoJSON
uploaded_file = st.file_uploader("Upload Farm Data GeoJSON file", type=['json', 'geojson'])

if uploaded_file is not None:
    try:
        # Read and parse the GeoJSON file
        geojson_data = json.load(uploaded_file)
        
        # Display a preview of the data structure
        st.subheader("Data Preview")
        st.json(geojson_data, expanded=False)
        
        # Convert button
        if st.button("Convert to KML"):
            with st.spinner("Converting..."):
                # Perform the conversion
                kmz_content = convert_farm_geojson_to_kml(geojson_data)
                
                # Provide a download link for the KMZ file
                file_name = uploaded_file.name.rsplit('.', 1)[0] + '.kmz'
                st.success("Conversion successful!")
                st.markdown(get_download_link(kmz_content, file_name), unsafe_allow_html=True)
                
                # Display success message and instructions
                st.info("Click the link above to download your KMZ file. This can be opened in Google Earth or similar applications.")
                
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    # Sample data section based on the user's example
    with st.expander("Don't have a file ready? Try our sample data"):
        sample_data = {
            "FarmPolygon": {
                "Data": [
                    {
                        "EntityID": "461009554768541155",
                        "PlotDisplayID": "PLT17085841829",
                        "PlotNr": "1",
                        "PlotStatus": "2",
                        "CommodityName": "Sorghum",
                        "EntityDisplayID": "ENT17085841399",
                        "EntityName": " endelina mutabe",
                        "TotalAreaHa": None,
                        "TotalProduction": None,
                        "BusinessUnitName": "Sorghum",
                        "CountryName": "Kenya",
                        "ProvinceName": "Tharaka-Nithi",
                        "DistrictName": "Tharaka South",
                        "SubDistrictName": "-",
                        "VillageName": "-",
                        "RegionLabel": "Tharaka South",
                        "PolyGeoJson": "{\"type\": \"Polygon\", \"coordinates\": [[[37.857618, -0.098945], [37.857937, -0.098403], [37.858208, -0.098556], [37.857851, -0.09915], [37.857611, -0.098961], [37.857618, -0.098945]]]}",
                        "Revision": "0",
                        "HaPolygon": "0.25",
                        "StatusCheck": "new"
                    },
                    {
                        "EntityID": "460875446567504940",
                        "PlotDisplayID": "PLT17072968619",
                        "PlotNr": "3",
                        "PlotStatus": "2",
                        "CommodityName": "Sorghum",
                        "EntityDisplayID": "ENT170729655710",
                        "EntityName": " Nathan.murithi",
                        "TotalAreaHa": None,
                        "TotalProduction": None,
                        "BusinessUnitName": "Sorghum",
                        "CountryName": "Kenya",
                        "ProvinceName": "Tharaka-Nithi",
                        "DistrictName": "Tharaka North",
                        "SubDistrictName": "-",
                        "VillageName": "-",
                        "RegionLabel": "Tharaka North",
                        "PolyGeoJson": "{\"type\": \"Polygon\", \"coordinates\": [[[37.946898, 0.034304], [37.947273, 0.034258], [37.947248, 0.033777], [37.947135, 0.03355], [37.946907, 0.033541], [37.946911, 0.034234], [37.946898, 0.034304]]]}",
                        "Revision": "0",
                        "HaPolygon": "0.3",
                        "StatusCheck": "new"
                    }
                ]
            }
        }
        
        if st.button("Use Sample Data"):
            # Display a preview of the sample data
            st.subheader("Sample Data Preview")
            st.json(sample_data, expanded=False)
            
            # Convert button for sample data
            if st.button("Convert Sample to KML"):
                with st.spinner("Converting..."):
                    # Perform the conversion
                    kmz_content = convert_farm_geojson_to_kml(sample_data)
                    
                    # Provide a download link for the KMZ file
                    st.success("Conversion successful!")
                    st.markdown(get_download_link(kmz_content, "farm_sample.kmz"), unsafe_allow_html=True)
                    
                    # Display success message
                    st.info("Click the link above to download your KMZ file")

# Add explanatory information
st.markdown("---")
st.markdown("""
### About this Farm Data Converter

This tool is specially designed to convert farm polygon data from the provided format to KML format, which can be used in applications like Google Earth, Google Maps, or other GIS software.

#### Features:
- Converts farm polygons stored in the "PolyGeoJson" field
- Includes all farm attributes as properties in the KML description
- Creates nicely styled polygons with custom names based on entity name, plot ID, and commodity
- Outputs as KMZ file (compressed KML) for easier sharing

#### Instructions:
1. Upload your farm data JSON file
2. Click "Convert to KML"
3. Download the resulting KMZ file
4. Open in Google Earth or similar application

#### Data Structure Requirements:
The converter expects a JSON structure with a "FarmPolygon" object containing a "Data" array of farm records, each with a "PolyGeoJson" field.
""")

# Requirements for this app (for reference)
# pip install streamlit simplekml
