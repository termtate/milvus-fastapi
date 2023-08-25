from pydantic import BaseModel, ConfigDict


class Patient2(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    
    id: int
    feeding_difficulties: str
    emotion_or_feeling: str
    epilepsy_syndromes_no_specifically_related_to_age: str
    ketogenic_diet: str
    stained_amniotic_fluid: str
    blood_transfusion_history: str
    trauma_history: str
    focal_secondary_bilateral_tonic_clonic_seizures: str
    is_parents_consanguineous_married: str
    fall: str
    has_birth_asphyxia: str
    convulsion_history: str
    growth_regression: str
    high_psychological_pressure: str
    vomit: str
    accompanying_fever: str
    delivery_mode: str
    diarrhea: str
    tic: str
    autism: str
