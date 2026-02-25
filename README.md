# 🌤️IoT Weather Station - Group 3
A MicroPython-based IoT sensor node that collects local weather data, synchronizes with the Open-Meteo API for sea-level pressure, and securely publishes the combined dataset to an MQTT broker.
Designed with a object-oriented structure, this project separates hardware interactions, network management, and user interface logic into highly maintainable modules.
Key Features
- Dynamically switch between assigned locations (Tettnang, Meckenbeuren, Kressbronn) using physical button inputs
- Utilizes SSL/TLS encryption (Port 8883) with built-in Last Will and Testament (LWT) for real-time online/offline presence tracking
- Combines physical hardware sensor readings with real-time web API data
- Provides real-time visual feedback for network status, active locations and data transmission success 

