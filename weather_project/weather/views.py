import requests
from django.shortcuts import render

def weather_view(request):
    weather_data = {}
    api_key = "FXL5YPAPQDNFATZFYFXSQZ6E6"  # Replace with your actual API key

    if 'city' in request.GET:
        city = request.GET['city']
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}"
        params = {
            "unitGroup": "metric",
            "key": api_key,
            "contentType": "json"
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()

                # Current weather details
                weather_data = {
                    "city": city,
                    "current_temp": data["currentConditions"]["temp"],
                    "conditions": data["currentConditions"]["conditions"],
                    "humidity": data["currentConditions"]["humidity"],
                    "wind_speed": data["currentConditions"]["windspeed"],
                    "icon": data["currentConditions"].get("icon", "default"),
                }

                # 10-Day Forecast
                forecast = []
                for day in data["days"][:10]:
                    forecast.append({
                        "date": day["datetime"],
                        "temp": day["temp"],
                        "conditions": day["conditions"],
                        "icon": day.get("icon", "default"),
                    })

                weather_data["forecast"] = forecast
            else:
                weather_data["error"] = f"Failed to fetch data. Status code: {response.status_code}, Error: {response.text}"
        except Exception as e:
            weather_data["error"] = f"An error occurred: {e}"
    else:
        weather_data["error"] = "Please enter a city name."

    return render(request, "weather.html", {"weather_data": weather_data})
