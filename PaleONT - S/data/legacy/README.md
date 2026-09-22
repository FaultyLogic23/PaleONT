# A-Box scritte a mano, archivio

Questi due file sono stati la verità del progetto fino al passaggio al CSV.

Non si modificano più. Restano qui per due ragioni:

1. **la prova del round-trip**: `tools/roundtrip_check.py` li confronta con
   quello che il CSV rigenera, e il confronto torna pulito, è ciò che
   dimostra che le tabelle di annotazione non perdono informazione;
2. **le motivazioni**: i loro `rdfs:comment` lunghi (D4, D6, la nota
   sull'*accordance* di Refshale 130) sono l'unica traccia originale di come
   quelle decisioni sono state prese. Il loro posto definitivo è
   `STATO_PROGETTO.md`, dove sono già.

Da qui in avanti l'A-Box si modifica **solo** cambiando `data/csv/*.csv` e
rilanciando `python3 tools/build.py`.
