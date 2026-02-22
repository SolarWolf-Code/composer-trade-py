import logging
from composer import ComposerClient
from composer.utils import symphony_to_python

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

client = ComposerClient(api_key="", api_secret="")

score = client.public_symphony.get_score("VPVpD1SoqR5ykVu4NdWS")
print("Score fetched:", score.name)

symphony_to_python(score, dedup=True)
