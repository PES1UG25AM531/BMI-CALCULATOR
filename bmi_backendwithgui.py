
# BMI CALCULATOR BACKEND SCRIPT
# Features:
# - Accepts weight in kg or lbs
# - Accepts height in cm, m, or feet
# - Converts all values to standard units (kg + meters)
# - Calculates BMI using standard formula
# - Determines BMI category
# - Returns dictionary output for easy frontend usage
# UNIT CONVERSION FUNCTIONS

def convert_weight_to_kg(weight, unit):
    unit = unit.lower().strip()

    if unit == "kg":
        return weight

    elif unit in ["lbs", "pounds", "lb"]:
        return weight * 0.453592

    else:
        raise ValueError("Invalid weight unit. Use 'kg' or 'lbs'.")


def convert_height_to_meters(height, unit):
    unit = unit.lower().strip()

    if unit == "m":
        return height

    elif unit == "cm":
        return height / 100

    elif unit in ["ft", "feet"]:
        return height * 0.3048

    else:
        raise ValueError("Invalid height unit. Use 'cm', 'm', or 'ft'.")



# BMI MAIN FUNCTIONS

def calculate_bmi(weight_kg, height_m):
    if height_m == 0:
        raise ValueError("Height cannot be zero.")
    return weight_kg / (height_m ** 2)


def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif 18.5 <= bmi < 24.9:
        return "Normal Weight"

    elif 25.0 <= bmi < 29.9:
        return "Overweight"

    else:
        return "Obese"



# BACKEND CONTROLLER FUNCTION


def bmi_backend(weight, weight_unit, height, height_unit):
    """
    Main backend function.
    Frontend should call this function and pass:
    - weight (float)
    - weight_unit: "kg" or "lbs"
    - height (float)
    - height_unit: "cm", "m", or "ft"
    """

    try:
        # Convert everything to standard units
        weight_kg = convert_weight_to_kg(weight, weight_unit)
        height_m = convert_height_to_meters(height, height_unit)

        # Calculate BMI
        bmi_value = calculate_bmi(weight_kg, height_m)
        category = bmi_category(bmi_value)

        # Prepare clean output for frontend
        result = {
            "weight_kg": round(weight_kg, 2),
            "height_m": round(height_m, 2),
            "bmi": round(bmi_value, 2),
            "category": category
        }

        return result

    except Exception as e:
        # Useful for debugging + frontend error display
        return {"error": str(e)}




import wx

# Create app and frame
app = wx.App()
frame = wx.Frame(None, title="BMI Calculator", size=(400, 350))
panel = wx.Panel(frame)
sizer = wx.BoxSizer(wx.VERTICAL)

# Weight input
sizer.Add(wx.StaticText(panel, label="Weight:"), 0, wx.TOP | wx.LEFT, 10)
weight_sizer = wx.BoxSizer(wx.HORIZONTAL)
weight_input = wx.TextCtrl(panel, size=(150, -1))
weight_sizer.Add(weight_input, 0, wx.RIGHT, 10)
weight_unit = wx.Choice(panel, choices=["kg", "lbs"])
weight_unit.SetSelection(0)
weight_sizer.Add(weight_unit, 0)
sizer.Add(weight_sizer, 0, wx.LEFT | wx.BOTTOM, 10)

# Height input
sizer.Add(wx.StaticText(panel, label="Height:"), 0, wx.TOP | wx.LEFT, 10)
height_sizer = wx.BoxSizer(wx.HORIZONTAL)
height_input = wx.TextCtrl(panel, size=(150, -1))
height_sizer.Add(height_input, 0, wx.RIGHT, 10)
height_unit = wx.Choice(panel, choices=["cm", "m", "ft"])
height_unit.SetSelection(0)
height_sizer.Add(height_unit, 0)
sizer.Add(height_sizer, 0, wx.LEFT | wx.BOTTOM, 10)

# Results display
result_text = wx.TextCtrl(panel, size=(350, 100), style=wx.TE_MULTILINE | wx.TE_READONLY)
sizer.Add(result_text, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

# Button frame
button_sizer = wx.BoxSizer(wx.HORIZONTAL)

def on_calculate(event):
    try:
        weight = float(weight_input.GetValue())
        height = float(height_input.GetValue())
        weight_u = weight_unit.GetStringSelection()
        height_u = height_unit.GetStringSelection()
        
        result = bmi_backend(weight, weight_u, height, height_u)
        
        if "error" in result:
            output = f"Error: {result['error']}"
        else:
            output = f"Weight: {result['weight_kg']} kg\nHeight: {result['height_m']} m\nBMI: {result['bmi']}\nCategory: {result['category']}"
        
        result_text.SetValue(output)
    except:
        result_text.SetValue("Error: Enter valid numbers")

def on_clear(event):
    weight_input.SetValue("")
    height_input.SetValue("")
    result_text.SetValue("")

calc_btn = wx.Button(panel, label="Calculate")
calc_btn.Bind(wx.EVT_BUTTON, on_calculate)
button_sizer.Add(calc_btn, 0, wx.RIGHT, 10)

clear_btn = wx.Button(panel, label="Clear")
clear_btn.Bind(wx.EVT_BUTTON, on_clear)
button_sizer.Add(clear_btn, 0)

sizer.Add(button_sizer, 0, wx.LEFT | wx.BOTTOM, 10)

panel.SetSizer(sizer)
frame.Show()
app.MainLoop()

