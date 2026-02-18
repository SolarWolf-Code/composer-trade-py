from composer import ComposerClient, client
from composer.utils import symphony_to_python

client = ComposerClient(api_key="", api_secret="")

score = client.public_symphony.get_score("VPVpD1SoqR5ykVu4NdWS")

symphony_to_python(score, dedup=True)