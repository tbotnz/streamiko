from netmiko import ConnectHandler

from config import config


def get_command(driver, hostname, command):
    response = ""
    try:
        connection_params = {
            "device_type": "cisco_ios",
            "host": hostname,
            "username": config["netmiko_username"],
            "password": config["netmiko_password"],
            "timeout": config["netmiko_timeout"]
        }
        # Show command that we execute
        with ConnectHandler(**connection_params) as net_connect:
            output = net_connect.send_command(command)
            return output.replace("\n", "<br>")
    except Exception as e:
        return f"error {e}"
