import socket


def is_on_rpi() -> bool:
    return socket.gethostname() == 'frcvision'


def is_on_roborio_network() -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
    except OSError:
        # No wifi, dang
        return False
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip.startswith('10.45.90.')
