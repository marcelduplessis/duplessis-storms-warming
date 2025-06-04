# calculate specific humidity using the temperature and relative humidity

def calculate_specific_humidity(temperature, relative_humidity):
    # Constants
    M_v = 18.01528  # molar mass of water vapor (g/mol)
    M_d = 28.9647   # molar mass of dry air (g/mol)

    # Magnus-Tetens formula for saturation vapor pressure
    e_s = 6.112 * (2.71828**((17.67 * temperature) / (temperature + 243.5)))

    # Vapor pressure of water vapor in the air
    e = e_s * (relative_humidity / 100.0)

    # print(f"Saturated Vapor Pressure (e_s): {e_s:.4f} hPa")
    # print(f"Vapor Pressure (e): {e:.4f} hPa")

    # Modified specific humidity formula
    specific_humidity = (relative_humidity * e) / (relative_humidity + (M_v / M_d) * (1 - relative_humidity / 100.0))

    return specific_humidity