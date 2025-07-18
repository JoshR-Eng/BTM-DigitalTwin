# cloud-function/main.py
import functions_framework 
from datetime import datetime, timezone
from pidController import PID_Controller

pid = PID_Controller(Kp=-5.21, Ki=-1.12, Kd = 0, setpoint = 295)
@functions_framework.http
def controller(request):
    """
    Recives a JSON file containing temperature
    Returns a cooling value for recieved data
    """
    server_recieve_time = datetime.now(timezone.utc).isoformat()

    request_json = request.get_json(silent=True)
    if request_json is None:
        return "Invalid JSON: Request body is empty or not valid JSON", 400
    
    current_temp = request_json['temperature']
    dt = request_json['dt']
    client_send_time = request_json.get('client_send_time')

    pid_value = pid.feedback(current_temp, dt)
    cooling_power = max(0, pid_value)

    response = {
        "cooling_power": cooling_power,
        "client_send_time": client_send_time,
        "server_recieve_time": server_recieve_time
    }

    return response
