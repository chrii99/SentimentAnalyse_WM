TODO:
[] Daten aufbereiten
    [X] Duplikate entfernt
    [] mit numpy und pands die Daten in ein pd.Dataframe packen für die weiterverarbeitung
    [] 

[] Themenmodelierung
    ([]verfeinern mit eigenen annotierten Daten)?

[] Sentimentanalyse
    []BERT laden
    []verfeinern mit eigenen annotierten Daten. Nutze DistilBert -> kleiner, besser zum anlernen, warum? (Quelle)
    []sentiment score berechnen



Datenaufbereitung:

Bert Tokenizer:
    input_ids
    token_type_ids (Satzunterteilung)
    attention_mask (1 wenn Wort, 0 wenn kein Wort [PAD])



Topic Modeling:
    BERTopic (https://github.com/MaartenGr/BERTopic)

[News, Spiel, Allgemeine Meinung]

