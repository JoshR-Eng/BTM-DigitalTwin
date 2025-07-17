# /main.py
import functions_framework
from pidController import PID_Controller

pi = PID_Controller(Kp=-32000, Ki=-138560, Kd = 0, setpoint = 295)
@functions_framework.http
def controller(request):
    """
    Recives a JSON file containing a time-stamped temperature data value
    Returns a cooling value for recieved data
    """
    request_json = request.get_json(silent=TRUE)
    if request_json is None:
        return "Invalid JSON: Request body is empty or not valid JSON", 400
  
    current_temp = request_json['temp']
    dt = request_json['dt']

    pi_value = pi.feedback(current_temp, dt)
    cooling_power = {'coolingPower': max(0, pi_value)}

    return cooling_power
