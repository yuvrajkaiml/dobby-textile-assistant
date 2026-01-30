"""
Dobby Parameters Schema
Complete schema matching Design Dobby Ver 22.0.0.357 "Automise Warp/Weft" dialog.
"""

from typing import List, Optional, Literal, Dict
from typing_extensions import TypedDict


# ============================================================================
# COMPONENT STRUCTURES
# ============================================================================

class GenerateRange(TypedDict):
    """Controls the pattern generation scope (From/To)."""
    from_value: int  # e.g., 96
    to_value: int    # e.g., 192


class CheckOptions(TypedDict):
    """Check pattern constraints. Only active when generate_mode = 'Check'."""
    regular: bool         # Standard check pattern
    balance_checks: bool  # Equal color distribution
    graded: bool          # Size gradation
    counter: bool         # Counter-balanced
    even_warp: bool       # Force even warp ends
    even_weft: bool       # Force even weft picks
    weave: bool           # Weave structure variation


class FilAFil(TypedDict):
    """Fil-a-Fil pattern settings (alternating single threads)."""
    enabled: bool
    mode: Literal["Auto", "Manually"]


class SolidMode(TypedDict):
    """Parameters for 'Solid' design style."""
    stripe_width_min: int   # Minimum stripe width (1-32)
    stripe_width_max: int   # Maximum stripe width (1-32)
    multi_factor_min: int   # Minimum multiplier (1-10)
    multi_factor_max: int   # Maximum multiplier (1-10)


class GradientMode(TypedDict):
    """Parameters for 'Grad' design style."""
    max_ends_start: int  # Max ends range start
    max_ends_end: int    # Max ends range end
    min_ends_start: int  # Min ends range start
    min_ends_end: int    # Min ends range end


class ColorMapping(TypedDict):
    """Color palette mapping. Keys are color1, color2, etc."""
    color1: str  # Primary color (e.g., "Maroon", "#8B0000", or index "A")
    color2: str  # Secondary color
    color3: Optional[str]  # Tertiary (if colors >= 3)
    color4: Optional[str]  # Quaternary (if colors >= 4)


class DisplaySwatch(TypedDict):
    """Preview swatch repeat settings."""
    x: int  # Horizontal repeats (1-8)
    y: int  # Vertical repeats (1-8)


# ============================================================================
# MAIN PARAMETER STRUCTURE
# ============================================================================

class DobbyParameters(TypedDict):
    """
    Complete parameter set for the Dobby Auto-Generation Engine.
    Maps 1:1 to the 'Automise Warp/Weft' dialog in Design Dobby.
    """
    # --- Core Settings ---
    unit: Literal["Ends", "Picks"]  # Calculation basis
    colors: int                      # Number of colors (2-8)
    ground: int                      # Ground/background color index (0-7)
    
    # --- Generation Range ---
    generate_range: GenerateRange    # From/To values
    
    # --- Mode Selection ---
    generate_mode: Literal["Warp", "Weft", "Check"]  # Direction
    epi_ppi: bool                                     # Link EPI to PPI
    
    # --- Check Options (conditional on generate_mode="Check") ---
    checks: CheckOptions
    
    # --- Fil-a-Fil ---
    fil_a_fil: FilAFil
    
    # --- Design Style ---
    design_style: Literal["Solid", "Grad", "Shadow", "Similar"]
    
    # --- Mode (variation strategy) ---
    mode: Literal["Normal", "Fixed", "Mixed", "Increment", "Decrement"]
    
    # --- Style-specific parameters (conditional) ---
    solid_mode: Optional[SolidMode]      # Only if design_style="Solid"
    gradient_mode: Optional[GradientMode]  # Only if design_style="Grad"
    
    # --- Color Palette ---
    color_mapping: ColorMapping
    
    # --- Display Settings ---
    display_swatch: DisplaySwatch


# ============================================================================
# AI RESPONSE STRUCTURE
# ============================================================================

class IntentResponse(TypedDict):
    """
    The AI's structured response containing intent classification
    and generated parameters.
    """
    intent: str                          # Classified intent (e.g., "check", "stripe", "gradient")
    template: str                        # Selected template name (e.g., "classic_check")
    confidence: float                    # Confidence score (0.0 - 1.0)
    clarification_required: bool         # True if AI needs more info
    question: Optional[str]              # Clarifying question (if required)
    parameters: Optional[DobbyParameters]  # Generated parameters (if not clarifying)


# ============================================================================
# JSON SCHEMA FOR VALIDATION
# ============================================================================

DOBBY_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string"},
        "template": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "clarification_required": {"type": "boolean"},
        "question": {"type": ["string", "null"]},
        "parameters": {
            "type": ["object", "null"],
            "properties": {
                "unit": {"type": "string", "enum": ["Ends", "Picks"]},
                "colors": {"type": "integer", "minimum": 2, "maximum": 8},
                "ground": {"type": "integer", "minimum": 0, "maximum": 7},
                "generate_range": {
                    "type": "object",
                    "properties": {
                        "from_value": {"type": "integer", "minimum": 1},
                        "to_value": {"type": "integer", "minimum": 1}
                    },
                    "required": ["from_value", "to_value"]
                },
                "generate_mode": {"type": "string", "enum": ["Warp", "Weft", "Check"]},
                "epi_ppi": {"type": "boolean"},
                "checks": {
                    "type": "object",
                    "properties": {
                        "regular": {"type": "boolean"},
                        "balance_checks": {"type": "boolean"},
                        "graded": {"type": "boolean"},
                        "counter": {"type": "boolean"},
                        "even_warp": {"type": "boolean"},
                        "even_weft": {"type": "boolean"},
                        "weave": {"type": "boolean"}
                    }
                },
                "fil_a_fil": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean"},
                        "mode": {"type": "string", "enum": ["Auto", "Manually"]}
                    }
                },
                "design_style": {"type": "string", "enum": ["Solid", "Grad", "Shadow", "Similar"]},
                "mode": {"type": "string", "enum": ["Normal", "Fixed", "Mixed", "Increment", "Decrement"]},
                "solid_mode": {
                    "type": ["object", "null"],
                    "properties": {
                        "stripe_width_min": {"type": "integer", "minimum": 1, "maximum": 32},
                        "stripe_width_max": {"type": "integer", "minimum": 1, "maximum": 32},
                        "multi_factor_min": {"type": "integer", "minimum": 1, "maximum": 10},
                        "multi_factor_max": {"type": "integer", "minimum": 1, "maximum": 10}
                    }
                },
                "gradient_mode": {
                    "type": ["object", "null"],
                    "properties": {
                        "max_ends_start": {"type": "integer"},
                        "max_ends_end": {"type": "integer"},
                        "min_ends_start": {"type": "integer"},
                        "min_ends_end": {"type": "integer"}
                    }
                },
                "color_mapping": {
                    "type": "object",
                    "properties": {
                        "color1": {"type": "string"},
                        "color2": {"type": "string"},
                        "color3": {"type": ["string", "null"]},
                        "color4": {"type": ["string", "null"]}
                    },
                    "required": ["color1", "color2"]
                },
                "display_swatch": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "integer", "minimum": 1, "maximum": 8},
                        "y": {"type": "integer", "minimum": 1, "maximum": 8}
                    }
                }
            },
            "required": ["unit", "colors", "generate_mode", "design_style", "mode", "color_mapping"]
        }
    },
    "required": ["intent", "confidence"]
}


# ============================================================================
# DEFAULT TEMPLATES
# ============================================================================

TEMPLATES = {
    "classic_check": {
        "unit": "Ends",
        "colors": 2,
        "ground": 0,
        "generate_range": {"from_value": 96, "to_value": 192},
        "generate_mode": "Check",
        "epi_ppi": True,
        "checks": {
            "regular": True,
            "balance_checks": True,
            "graded": False,
            "counter": False,
            "even_warp": True,
            "even_weft": True,
            "weave": False
        },
        "fil_a_fil": {"enabled": False, "mode": "Auto"},
        "design_style": "Solid",
        "mode": "Normal",
        "solid_mode": {
            "stripe_width_min": 2,
            "stripe_width_max": 8,
            "multi_factor_min": 1,
            "multi_factor_max": 2
        },
        "gradient_mode": None,
        "color_mapping": {"color1": "Black", "color2": "White", "color3": None, "color4": None},
        "display_swatch": {"x": 4, "y": 4}
    },
    "premium_plaid": {
        "unit": "Ends",
        "colors": 3,
        "ground": 0,
        "generate_range": {"from_value": 96, "to_value": 192},
        "generate_mode": "Check",
        "epi_ppi": True,
        "checks": {
            "regular": True,
            "balance_checks": True,
            "graded": True,
            "counter": False,
            "even_warp": False,
            "even_weft": False,
            "weave": False
        },
        "fil_a_fil": {"enabled": False, "mode": "Auto"},
        "design_style": "Solid",
        "mode": "Normal",
        "solid_mode": {
            "stripe_width_min": 1,
            "stripe_width_max": 10,
            "multi_factor_min": 1,
            "multi_factor_max": 4
        },
        "gradient_mode": None,
        "color_mapping": {"color1": "Maroon", "color2": "Gold", "color3": "Cream", "color4": None},
        "display_swatch": {"x": 4, "y": 4}
    },
    "simple_stripe": {
        "unit": "Ends",
        "colors": 2,
        "ground": 0,
        "generate_range": {"from_value": 48, "to_value": 96},
        "generate_mode": "Warp",
        "epi_ppi": True,
        "checks": {
            "regular": False,
            "balance_checks": False,
            "graded": False,
            "counter": False,
            "even_warp": False,
            "even_weft": False,
            "weave": False
        },
        "fil_a_fil": {"enabled": False, "mode": "Auto"},
        "design_style": "Solid",
        "mode": "Normal",
        "solid_mode": {
            "stripe_width_min": 4,
            "stripe_width_max": 12,
            "multi_factor_min": 1,
            "multi_factor_max": 2
        },
        "gradient_mode": None,
        "color_mapping": {"color1": "Navy", "color2": "White", "color3": None, "color4": None},
        "display_swatch": {"x": 4, "y": 4}
    },
    "gradient_stripe": {
        "unit": "Ends",
        "colors": 2,
        "ground": 0,
        "generate_range": {"from_value": 48, "to_value": 96},
        "generate_mode": "Warp",
        "epi_ppi": True,
        "checks": {
            "regular": False,
            "balance_checks": False,
            "graded": False,
            "counter": False,
            "even_warp": False,
            "even_weft": False,
            "weave": False
        },
        "fil_a_fil": {"enabled": False, "mode": "Auto"},
        "design_style": "Grad",
        "mode": "Increment",
        "solid_mode": None,
        "gradient_mode": {
            "max_ends_start": 2,
            "max_ends_end": 10,
            "min_ends_start": 1,
            "min_ends_end": 2
        },
        "color_mapping": {"color1": "Blue", "color2": "White", "color3": None, "color4": None},
        "display_swatch": {"x": 4, "y": 4}
    }
}
