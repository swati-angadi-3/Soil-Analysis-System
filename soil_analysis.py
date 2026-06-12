def analyze_soil(ph, moisture, density, organic):
    
    # Strong soil condition
    if 6 <= ph <= 7.5 and density >= 1.5:
        strength = "Strong"
        usage = "Suitable for Construction"
    
    # Weak soil condition
    elif moisture > 50:
        strength = "Weak"
        usage = "Not suitable for building, suitable for agriculture"
    
    # Moderate soil
    else:
        strength = "Moderate"
        usage = "Can be used for light construction or farming"
    
    return strength, usage