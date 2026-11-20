from ui.app import RSAApp
from rsa_service import RealRSAService


if __name__ == "__main__":
    RSAApp(service=RealRSAService()).mainloop()
