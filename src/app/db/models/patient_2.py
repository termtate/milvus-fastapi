from pymilvus import CollectionSchema, DataType, FieldSchema


fields: list[FieldSchema] = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="feeding_difficulties", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="emotion_or_feeling", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="epilepsy_syndromes_no_specifically_related_to_age", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="ketogenic_diet", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="stained_amniotic_fluid", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="blood_transfusion_history", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="trauma_history", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="focal_secondary_bilateral_tonic_clonic_seizures", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="is_parents_consanguineous_married", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="fall", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="has_birth_asphyxia", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="convulsion_history", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="growth_regression", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="high_psychological_pressure", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="vomit", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="accompanying_fever", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="delivery_mode", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="diarrhea", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="tic", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="autism", dtype=DataType.VARCHAR, max_length=200),
]

schema = CollectionSchema(fields=fields, description='')