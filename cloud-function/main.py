import functions_framework

@functions_framework.http
def echo(request):
    """
    HTTP-Triggered function that echoes incoming data back to source
    """
    request_data = request.get_data()
    return request_data
