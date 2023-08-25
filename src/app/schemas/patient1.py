from pydantic import BaseModel, ConfigDict


class Patient1(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    
    id: int
    id_card_number: str
    name: str
    hospitalize_num: str
    case_number: str
    sex: str
    age: str
    phone_number: str
    seizure_evolution: str
    seizure_duration: str
    seizure_freq: str
    maternal_pregnancy_age: str
    pregnancy_num: str
    birth_weight: str
    head_c: str
    blood_urine_screening: str
    copper_cyanin: str
    csf: str
    genetic_test: str
    head_ct: str
    head_mri: str
    scalp_eeg: str
    precipitating_factor: str
    childhood_onset: str
    aed: str
    epilepsy_surgery: str
    simple_sensory_seizure: str
    is_parent_febrile_convulsion: str
    pregnancy_diseases: str
    infancy_onset: str
    motor_seizure: str
    metabolic_disorders: str
    postictal_manifestation: str
    symptomatic_epilepsy: str
    have_surgery_history: str
    automatism: str
    generalized_motor_seizures: str
    pigmentation: str
    local_motor_seizures: str
    autonomic_nerves: str
    cognition: str
    other_epilepsy_syndrome: str
    electrolyte: str
    neonatal_onset: str
    vaccination_history: str
    is_relatives_have_epilepsy: str
    lactate: str
    growth_milestone: str
    growth_retardation: str
    adolescent_adult_onset: str
    stunting: str
    blood_ammonia: str
    generalized_non_motor_seizures: str
    learning_difficulties: str
    focal_non_motor_seizures: str
    overprotected: str
    has_febrile_seizures_history: str
    has_neonatal_convulsion: str
    adhd: str
    has_severe_jaundice: str
