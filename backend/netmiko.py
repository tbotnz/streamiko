from netmiko import ConnectHandler, SSHDetect

from config import config


def get_command(driver, hostname, command):
    response = ""
    try:
        connection_params = {
            "device_type": "autodetect",
            "host": hostname,
            "username": config["netmiko_username"],
            "password": config["netmiko_password"],
            "timeout": config["netmiko_timeout"],
            "fast_cli": True
        }

        guesser = SSHDetect(**connection_params)
        best_match = guesser.autodetect()
        connection_params["device_type"] = best_match

        with ConnectHandler(**connection_params) as net_connect:
            output = net_connect.send_command(command)
            return output.replace("\n", "<br>")
    except Exception as e:
        return f"error {e}"
