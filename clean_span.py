import pandas as pd
import re

# Lecture du fichier CSV
df = pd.read_csv('informa.csv')

# Suppression des balises span dans chaque cellule
df = df.applymap(lambda x: re.sub(r'<span.*?>|<\/span>', '', str(x)))

# Sauvegarde du nouveau fichier CSV
df.to_csv('informa.csv', index=False)