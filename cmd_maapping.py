"""
cmd_mapping.py
==============
Mapping from model internal class/folder names → display Stone Names.
"""

from __future__ import annotations

# ── COMPREHENSIVE MAPPING TABLE ──────────────────────────────────────────
# Mapping of model output classes to high-fidelity display names.
MODEL_OUTPUT_MAPPING: dict[str, str] = {
    "Alaska_White_All_Variations": "Alaska White",
    "Amazonite_All_Variations": "Amazonite",
    "Ammazza_All_Variations": "Ammazza",
    "Ancora_All_Variations": "Ancora",
    "Aphrodite_All_Variations": "Aphrodite",
    "Aquabella_All_Variations": "Aquabella",
    "Avocado_All_Variations": "Avocado",
    "Basaltino_All_Variations": "Basaltino",
    "Bianco_Eliptus_All_Variations": "Bianco Eliptus",
    "Bianco_Lasa_All_Variations": "Bianco Lasa",
    "Bianco_Lazuli_All_Variations": "Bianco Lazuli",
    "Bianco_Reale_Cream_All_Variation": "Bianco Reale Cream",
    "Bianco_Siena_All_Variations": "Bianco Siena",
    "Bianco_Vogue": "Bianco Vogue",
    "Breccia_Aura_All_Variations": "Breccia Aura",
    "Calacatta_Caldiya_All_Variations": "Calacatta Caldiya",
    "Carrara_40_Variations": "Carrara 40",
    "Chianti_All_Variations": "Chianti",
    "Corteccia_All_Variations": "Corteccia",
    "Cosmic_Gold_All_Variations": "Cosmic Gold",
    "Crema_Marfil_All_Variations": "Crema Marfil",
    "Crema_Purrisima_All_Variations": "Crema Purrisima",
    "Crema_Siena_All_Variations": "Crema Siena",
    "Dark_Emperador_All_Variations": "Dark Emperador",
    "Ebony_Travertino_All_Variations": "Ebony Travertino",
    "Estremoz": "Estremoz",
    "Fantasy_Brown_All_Variations": "Fantasy Brown",
    "Ferragamo_Beige_Variations": "Ferragamo Beige",
    "Fontana_All_Variations": "Fontana",
    "French_Brown_All_Variations": "French Brown",
    "Fusion_Black_All_Variations": "Fusion Black",
    "Granello_All_Variations": "Granello",
    "Green_Jadezcala_All_Variations": "Green Jadezcala",
    "Grey_Granitilo": "Grey Granitilo",
    "Grey_Saran_Coline_All_Variations": "Grey Saran Coline",
    "Grey_Williams_All_Variations": "Grey Williams",
    "Grey_Williams_Italy_All_Variations": "Grey Williams Italy",
    "Grigio_Broze_Amani": "Grigio Broze Amani",
    "Grigio_Fiasco_All_Variations": "Grigio Fiasco",
    "Lasa_Covelano": "Lasa Covelano",
    "Pantheon": "Pantheon",
    "Pirgon": "Pirgon",
    "Statuario_All_Variations": "Statuario",
    "Statuario_Barattini": "Statuario Barattini",
    "Thassos": "Thassos",
    "Thassos_Novelato": "Thassos Novelato",

    "tile_Algae_Vitrum_All_Variations": "Algae Vitrum",
    "tile_Amazon_Blush_All_Variations": "Amazon Blush",
    "tile_Amozonita_All_Variations": "Amozonita",
    "tile_Aqua_Patagonia_Extra_All_Variations": "Aqua Patagonia Extra",
    "tile_Artico_All_Variations": "Artico",
    "tile_Aventurine_All_Variations": "Aventurine",
    "tile_Avocatus_All_Variations": "Avocatus",
    "tile_Azul_Bahia_All_Variations": "Azul Bahia",
    "tile_Azul_Brichani_All_Variations": "Azul Brichani",
    "tile_Azul_Calcite_All_Variations": "Azul Calcite",
    "tile_Azulado_All_Variations": "Azulado",
    "tile_Beige_Travertino_All_Variations": "Beige Travertino",
    "tile_Bianco_Moronus_All_Variations": "Bianco Moronus",
    "tile_Black_Marquina_All_Variations": "Black Marquina",
    "tile_Blue_Onyx_All_Variations": "Blue Onyx",
    "tile_Bulberry_Beige_All_Variations": "Bulberry Beige",
    "tile_Bulberry_Grey_All_Variations": "Bulberry Grey",

    "tile_Calacatta_Picasso_All_Variations": "Calacatta Picasso",
    "tile_Celina_Grey_All_Variations": "Celina Grey",
    "tile_Cream_Wave_Onyx_All_Variations": "Cream Wave Onyx",
    "tile_Crema_Elysee_All_Variations": "Crema Elysee",
    "tile_Crema_Uno_All_Variations": "Crema Uno",
    "tile_Crystal_Yellow_Onyx_All_Variations": "Crystal Yellow Onyx",
    "tile_Dior_Pearl_All_Variations": "Dior Pearl",
    "tile_Dover_White_All_Variations": "Dover White",
    "tile_Emerald_Crystallo_All_Variations": "Emerald Crystallo",
    "tile_Emerald_Flame_All_Variations": "Emerald Flame",
    "tile_Emerald_Harmony_All_Variations": "Emerald Harmony",
    "tile_Flortine_Beige_All_Variations": "Flortine Beige",
    "tile_Grey_Bardilo_All_Variations": "Grey Bardilo",
    "tile_Grey_Flurry_All_Variations": "Grey Flurry",
    "tile_Grey_Saint_Laurent_All_Variations": "Grey Saint Laurent",
    "tile_Grey_Travertino_All_Variations": "Grey Travertino",
    "tile_Grigio_Fusion_All_Variations": "Grigio Fusion",
    "tile_Grigio_Trambisera_All_Variations": "Grigio Trambisera",
    "tile_Hermes_Grey_All_Variations": "Hermes Grey",
    "tile_Honey_Onyx_All_Variations": "Honey Onyx",
    "tile_Ice_Berg_All_Variations": "Ice Berg",
    "tile_Icicle_Onyx_All_Variations": "Icicle Onyx",
    "tile_Indian_Tobacco_All_Variations": "Indian Tobacco",
    "tile_La_Tella_All_Variations": "La Tella",
    "tile_Lagos_All_Variations": "Lagos",
    "tile_Lavanto_All_Variations": "Lavanto",
    "tile_Lazurite_All_Variations": "Lazurite",
    "tile_Lemurian_Blue_All_Variations": "Lemurian Blue",
    "tile_Lilac_White_All_Variations": "Lilac White",
    "tile_Mango_Onyx_All_Variations": "Mango Onyx",
    "tile_Marco_Polo_All_Variations": "Marco Polo",
    "tile_Masa_grey_All_Variations": "Masa grey",
    "tile_Metal_Rust_All_Variations": "Metal Rust",
    "tile_Mocca_Cream_All_variations": "Mocca Cream",
    "tile_Mont_Sierra_All_Variations": "Mont Sierra",
    "tile_Nebula_All_Variations": "Nebula",
    "tile_Nero_Saint_Laurent_All_Variations": "Nero Saint Laurent",
    "tile_Noche_Travertino_All_Variations": "Noche Travertino",
    "tile_Obsidian_All_Variations": "Obsidian",
    "tile_Omni_Bianco_All_Variations": "Omni Bianco",
    "tile_Opus_All_Variations": "Opus",
    "tile_Oracle_Grey_All_Variations": "Oracle Grey",
    "tile_Oreo_Grey_All_Variations": "Oreo Grey",
    "tile_Ottoman_Beige_All_Variations": "Ottoman Beige",
    "tile_Palissandro_Bronzo_All_Variations": "Palissandro Bronzo",
    "tile_Panda_White_All_Variations": "Panda White",
    "tile_Parquet_All_Variations": "Parquet",
    "tile_Patagonia_All_Variations": "Patagonia",
    "tile_Patanal_All_Variations": "Patanal",
    "tile_Patina_All_Variations": "Patina",
    "tile_Peach_Onyx_All_Variations": "Peach Onyx",
    "tile_Phantus_Hydro_All_Variations": "Phantus Hydro",
    "tile_Pico_Dorado_All_Variations": "Pico Dorado",
    "tile_Pietra_Finno_All_Variations": "Pietra Finno",
    "tile_Pigus_White_All_Variations": "Pigus White",
    "tile_Pink_Onyx_All_Variations": "Pink Onyx",
    "tile_Pink_Valencia_All_Variations": "Pink Valencia",
    "tile_Platinum_Gold_All_Variations": "Platinum Gold",
    "tile_Polaris_All_Variations": "Polaris",
    "tile_Polurrian_All_Variations": "Polurrian",
    "tile_Red_Alikante_All_Variations": "Red Alikante",
    "tile_Red_Lavante_All_Variations": "Red Lavante",
    "tile_Red_Verona_All_Variations": "Red Verona",
    "tile_Rivera_Black_All_Variations": "Rivera Black",
    "tile_Rosso_Lavante_All_Variations": "Rosso Lavante",
    "tile_Silver_Potro_All_Variations": "Silver Potro",
    "tile_Silver_Serpegiantte_All_Variations": "Silver Serpegiantte",
    "tile_Silver_Travertino_All_Variations": "Silver Travertino",
    "tile_Soda_Lite_Blue_All_Variations": "Soda Lite Blue",
    "tile_Spider_Beige_All_Variations": "Spider Beige",
    "tile_Superio_Beige_All_Variations": "Superio Beige",
    "tile_Superior_Beige_All_Variations": "Superior Beige",
    "tile_Tempest_All_Variations": "Tempest",
    "tile_Tiffany_All_Variations": "Tiffany",
    "tile_Tiger_Onyx_All_Variations": "Tiger Onyx",
    "tile_Tobacco_Brown_All_Variations": "Tobacco Brown",
    "tile_Tropical_All_Variations": "Tropical",
    "tile_Tropical_Storm_All_Variations": "Tropical Storm",
    "tile_Twilight_All_Variations": "Twilight",
    "tile_Valle_Rossa_All_Variations": "Valle Rossa",
    "tile_Verde_Fusion_All_Variations": "Verde Fusion",
    "tile_Verde_Karzai_All_Variations": "Verde Karzai",
    "tile_Verde_Onyx_All_Variations": "Verde Onyx",
    "tile_Verde_Patagonia_Extra_All_Variations": "Verde Patagonia Extra",
    "tile_Verde_Vermont_All_Variations": "Verde Vermont",
    "tile_Vibranium_All_Variations": "Vibranium",
    "tile_Vietnam_White_All_Variations": "Vietnam White",
    "tile_White_Onyx_All_Variations": "White Onyx",
    "tile_Zebrano_All_Variations": "Zebrano"
}

# ── LEGACY CMD OFFICE MAPPING ──────────────────────────────────────────
CMD_OFFICE_MAPPING: dict[str, str] = {
    "tile_CMD_office_Flooring_Storage":           "Grigio Bronze Amani",
    "tile_CMD_office_Storage_Flooring":           "Grigio Bronze Amani",
    "tile_CMD_Office_Storage_Flooring":           "Grigio Bronze Amani",
    "tile_CMD_office_Flooring_Storage_2":         "Breccia",
    "tile_CMD_office_Storage_Flooring_2":         "Breccia",
    "tile_CMD_Office_Flooring_Storage_2":         "Breccia",
    "tile_CMD_Cabin_1":                           "Griccia Onyx",
    "tile_CMD_Office_Cabin_1":                    "Griccia Onyx",
    "tile_CMD_Office_Cabin_2":                    "Golden Spider",
    "tile_CMD_Cabin_2":                           "Golden Spider",
    "tile_CMD_Office_Reception_Flooring":         "Soda Lite Blue",
    "tile_CMD_Office_Conference_Table":           "Nozet Florry",
    "tile_CMD_Office_Stairs":                     "Nozet Florry",
    "tile_CMD_office_Stairs":                     "Nozet Florry",
}

# Merge mappings (Model Output takes priority if overlap, though unlikely)
RAW_MAPPING = {**CMD_OFFICE_MAPPING, **MODEL_OUTPUT_MAPPING}

# ── Derived normalised lookup ─────────────────────────────────────────────

def _normalise(name: str) -> str:
    """Lowercase + collapse underscores/hyphens to spaces + strip."""
    return name.lower().replace("_", " ").replace("-", " ").strip()

_NORMALISED_LOOKUP: dict[str, str] = {
    _normalise(k): v for k, v in RAW_MAPPING.items()
}

_DIRECT_LOOKUP: dict[str, str] = RAW_MAPPING

# ── Public API ────────────────────────────────────────────────────────────

def is_cmd_class(family_name: str) -> bool:
    """Return True if the family name is a CMD Office internal class."""
    return _normalise(family_name) in { _normalise(k) for k in CMD_OFFICE_MAPPING.keys() }

def resolve_family_name(family_name: str) -> str:
    """
    Return the display stone name for known classes, or the original
    family name if unmapped. Unter underscore replacement is disabled.
    """
    # 1. Direct match (case-sensitive as provided by user)
    if family_name in _DIRECT_LOOKUP:
        return _DIRECT_LOOKUP[family_name]
    
    # 2. Normalised match (fallback for variations)
    norm = _normalise(family_name)
    if norm in _NORMALISED_LOOKUP:
        return _NORMALISED_LOOKUP[norm]
    
    # 3. No fallback underscored replacement
    return family_name