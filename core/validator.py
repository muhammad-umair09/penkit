import re
import socket
from urllib.parse import urlparse

class Validator:
    @staticmethod
    def is_valid_ipv4(ip: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return True
        except socket.error:
            return False

    @staticmethod
    def is_valid_ipv6(ip: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True
        except socket.error:
            return False

    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        pattern = re.compile(
            r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$'
        )
        return bool(pattern.match(domain))

    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def is_valid_port(port: int) -> bool:
        return 1 <= port <= 65535