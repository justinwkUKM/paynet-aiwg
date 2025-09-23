from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from dotenv import load_dotenv
from src.auth import SimpleTokenVerifier
import requests, os


# -------------------------
# INTIALIZATION
# -------------------------
# Load Environment Variables
load_dotenv()

# Simple MCP server
mcp = FastMCP(
    "Weather MCP Server",
)

# MCP Server with Auth 
# mcp = FastMCP(
#     "Weather MCP Server",
#     token_verifier = SimpleTokenVerifier(),
#     auth = AuthSettings(
#         issuer_url = AnyHttpUrl("https://auth.example.com"),  
#         resource_server_url = AnyHttpUrl("http://localhost:3001"), 
#         required_scopes=["user"],
#     ),
# )

# -------------------------
# TOOLS DEFINITION
# -------------------------
@mcp.tool()
def get_temperature(city: str) -> dict:
    """
    Fetch the current temperature for a specified city.

    Args:
        city (str): Name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """        
    try:
        result_city = requests.get(url='https://geocoding-api.open-meteo.com/v1/search?name=' + city)
        location = result_city.json()
    
        longitude = str(location['results'][0]['longitude'])
        latitude = str(location['results'][0]['latitude'])

        result = requests.get(url="https://api.open-meteo.com/v1/forecast?latitude=" + latitude + "&longitude=" + longitude + "&current=temperature_2m")
        data = result.json()
        temperature = str(data['current']['temperature_2m'])
        units = str(data['current_units']['temperature_2m'])
        
        return {
            "status": "success",
            "report": f"The temperature in {city} is {temperature}{units}" 
        }
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Sorry, I don't have weather information for '{city}'.\nError Details: " + str(e)
        }


@mcp.tool()
def get_windspeed(city: str) -> dict:
    """
    Fetch the current windspeed for a specified city.

    Args:
        city (str): Name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """        
    try:
        result_city = requests.get(url='https://geocoding-api.open-meteo.com/v1/search?name=' + city)
        location = result_city.json()
    
        longitude = str(location['results'][0]['longitude'])
        latitude = str(location['results'][0]['latitude'])

        result = requests.get(url="https://api.open-meteo.com/v1/forecast?latitude=" + latitude + "&longitude=" + longitude + "&current=wind_speed_10m")
        data = result.json()
        windspeed = str(data['current']['wind_speed_10m'])
        units = str(data['current_units']['wind_speed_10m'])
        
        return {
            "status": "success",
            "report": f"The windspeed in {city} is {windspeed}{units}" 
        }
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Sorry, I don't have weather information for '{city}'.\nError Details: " + str(e)
        }

# -------------------------
# EXECUTE SERVER
# -------------------------
if __name__ == "__main__":
    mcp.run(transport="streamable-http")