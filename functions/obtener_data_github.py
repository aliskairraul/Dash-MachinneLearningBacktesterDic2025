import requests
import time
from utils.utils import urls_inferencias_predicciones, paths_data_github
from utils.logger import get_logger

logger = get_logger("Extrayendo Data Github")


def obtener_data_github() -> bool:
    instrumentos_finacieros = ["BTCUSD", "EURUSD", "SPX", "XAUUSD"]
    for instrumento in instrumentos_finacieros:
        try:
            response = requests.get(urls_inferencias_predicciones[instrumento])
            if response.status_code == 200:
                with open(paths_data_github[instrumento], "wb") as f:
                    f.write(response.content)
                logger.info(f"Data del instrumento {instrumento} actualizada correctamente")
            else:
                logger.warning(f"Status code {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error tratando de Cargar la data desde github:  {e}")
            return False
        time.sleep(1)
    return True
