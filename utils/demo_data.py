"""
Demo data for fallback / demonstration mode when no API key is provided.
"""

DEMO_PPE_REPORT = {
    "safety_score": 62,
    "overall_status": "AT RISK",
    "ppe_detection": {
        "helmets": {
            "detected": True,
            "compliant_workers": 4,
            "total_workers": 6,
            "compliance_rate": "67%",
            "notes": "2 workers observed without hard hats in active work zone"
        },
        "high_vis_vests": {
            "detected": True,
            "compliant_workers": 5,
            "total_workers": 6,
            "compliance_rate": "83%",
            "notes": "1 worker wearing faded vest that does not meet IS 15809 retro-reflectivity"
        },
        "steel_toe_boots": {
            "detected": False,
            "compliant_workers": 3,
            "total_workers": 6,
            "compliance_rate": "50%",
            "notes": "Footwear cannot be clearly verified from current angle; recommend closer inspection"
        },
        "safety_harnesses": {
            "detected": True,
            "compliant_workers": 2,
            "total_workers": 2,
            "compliance_rate": "100%",
            "notes": "Workers at elevation appear correctly harnessed"
        },
        "safety_gloves": {
            "detected": False,
            "compliant_workers": 1,
            "total_workers": 6,
            "compliance_rate": "17%",
            "notes": "Most workers handling materials without protective gloves"
        }
    },
    "site_hazards": [
        {
            "hazard": "Workers without helmets in active construction zone",
            "severity": "Critical",
            "osha_reference": "OSHA 1926.100",
            "is_reference": "IS 2925",
            "corrective_remedy": "Immediate work stoppage until PPE is donned. Issue hard hats from site store. Post safety marshal at zone entry."
        },
        {
            "hazard": "Unguarded floor opening / edge near scaffolding",
            "severity": "High",
            "osha_reference": "OSHA 1926.502",
            "is_reference": "IS 3696 Part 1",
            "corrective_remedy": "Install guard rails min 1.05 m high with mid-rail and toe board within 24 hours."
        },
        {
            "hazard": "Inadequate glove usage during material handling",
            "severity": "Medium",
            "osha_reference": "OSHA 1910.138",
            "is_reference": "IS 6994",
            "corrective_remedy": "Supply cut-resistant gloves to all manual-handling workers. Conduct 15-min toolbox talk on hand protection."
        },
        {
            "hazard": "Non-compliant reflective vest",
            "severity": "Low",
            "osha_reference": "ANSI/ISEA 107",
            "is_reference": "IS 15809",
            "corrective_remedy": "Replace worn vest before next shift. Maintain PPE replacement log on site."
        }
    ],
    "compliance_standards": ["OSHA 29 CFR 1926 (Construction)", "IS 456:2000", "IS 3696", "NBC 2016"],
    "recommendation_summary": "Site requires immediate corrective action on helmet compliance. Schedule emergency safety briefing today. Overall readiness classified as AT RISK until critical items are resolved.",
    "audit_timestamp": "2026-10-27T22:39:00+05:30",
    "demo_mode": True
}

DEMO_CRACK_REPORT = {
    "defect_type": "Structural Shear Crack",
    "severity_level": "High",
    "crack_width_mm": 3.2,
    "crack_length_estimate_cm": 45,
    "orientation": "Diagonal (45 to 60 degrees)",
    "root_causes": [
        "Differential settlement of foundation due to uneven soil bearing capacity",
        "Inadequate shear reinforcement (stirrup spacing) per IS 456:2000",
        "Possible overloading beyond design dead + live load combination",
        "Shrinkage of concrete during curing with insufficient expansion joints"
    ],
    "affected_zone": "Structural Column-Beam Junction (Ground to First Floor)",
    "structural_risk": "Compromised lateral load transfer; risk of progressive failure under seismic load",
    "recommended_repairs": [
        {
            "repair": "Epoxy Injection Grouting",
            "description": "Inject low-viscosity epoxy resin under pressure to seal and bond crack faces. Suitable for cracks > 0.2mm.",
            "urgency": "Immediate",
            "estimated_cost_inr": "Rs. 18,000 to 35,000 per running meter"
        },
        {
            "repair": "Carbon Fiber Reinforced Polymer (CFRP) Wrapping",
            "description": "Apply CFRP strips around column to restore tensile capacity and prevent further shear crack propagation.",
            "urgency": "Within 7 days",
            "estimated_cost_inr": "Rs. 45,000 to 90,000 per column"
        },
        {
            "repair": "Structural Re-grouting & Concrete Jacketing",
            "description": "Remove deteriorated concrete, apply bonding agent, and pour new concrete jacket with additional rebar to restore section size.",
            "urgency": "Within 30 days",
            "estimated_cost_inr": "Rs. 1.2L to 2.5L per structural element"
        }
    ],
    "monitoring_protocol": "Install DEMEC gauge or vibrating wire strain gauge for weekly crack width monitoring. Document readings in site structural log.",
    "is_standard_reference": "IS 456:2000 Clause 35, IS 13920 (Seismic), ACI 318-19",
    "requires_structural_engineer": True,
    "demo_mode": True
}

WEATHER_PROTOCOLS = {
    "High Wind": {
        "alert_level": "RED",
        "color": "#FF4444",
        "icon": "WIND",
        "suspended_operations": [
            "All crane and tower crane lifts above 6m",
            "Scaffolding erection / dismantling",
            "Curtain wall glass installation",
            "Concrete placement in open areas",
            "Any aerial work platform (AWP) operations"
        ],
        "active_measures": [
            "Secure all loose materials, formwork, and sheeting with tie-downs",
            "Lower crane jibs and lock slew brakes",
            "Issue safety harness lanyard checks for all elevated workers",
            "Erect windbreaks around critical concrete pours",
            "Monitor sustained wind speed -- halt all work above 50 km/h"
        ],
        "osha_threshold": "Wind >28 mph (45 km/h): crane operations halt per OSHA 1926.1417",
        "is_standard": "IS 875 Part 3 (Wind Loads)"
    },
    "Heavy Rain": {
        "alert_level": "ORANGE",
        "color": "#FF8C00",
        "icon": "RAIN",
        "suspended_operations": [
            "Electrical panel installations and live cable work",
            "Open excavations exceeding 1.5m depth",
            "Freshly poured concrete exposure (first 24h)",
            "Painting, waterproofing membrane application",
            "Basement/below-grade work in flood risk zones"
        ],
        "active_measures": [
            "Cover all fresh concrete with polythene sheeting immediately",
            "Pump out standing water from excavations before re-entry",
            "De-energize all temporary electrical installations near water ingress",
            "Inspect and reinstate trench sheet piling / shoring after rain",
            "Concrete curing protocol: Keep moist but not flooded for 28-day period"
        ],
        "osha_threshold": "OSHA 1926.651: Inspect trenches daily and after rainstorms",
        "is_standard": "IS 456:2000 Section 13 (Curing), IS 13754 (Excavation Safety)"
    },
    "Extreme Heat": {
        "alert_level": "AMBER",
        "color": "#FFB300",
        "icon": "HEAT",
        "suspended_operations": [
            "Outdoor heavy physical work between 12:00 to 15:00 hrs",
            "Hot works (welding / cutting) during peak UV hours",
            "Asphalt / tar application without cooling protocols",
            "Long-duration confined space work"
        ],
        "active_measures": [
            "Mandate hydration breaks every 30 min -- 250ml water per worker",
            "Erect shade shelters and mist cooling fans at rest areas",
            "Reschedule concrete pours to early morning (05:00 to 09:00) or evening",
            "Use ice water curing for all freshly poured slabs",
            "Monitor workers for heat exhaustion: confusion, rapid pulse, cessation of sweating are emergencies",
            "Reduce concrete water-cement ratio -- use GGBS or fly ash to control heat of hydration"
        ],
        "osha_threshold": "OSHA Heat Illness Prevention: Heat Index > 103F (39.4C) = High Risk",
        "is_standard": "IS 456:2000 Clause 9 (Hot Weather Concreting)"
    },
    "Normal": {
        "alert_level": "GREEN",
        "color": "#00C851",
        "icon": "OK",
        "suspended_operations": [],
        "active_measures": [
            "Standard daily toolbox talk before operations commence",
            "Verify PPE compliance at each zone entry point",
            "Maintain housekeeping -- clear walkways and access routes",
            "Document all near-miss incidents in site safety register",
            "Conduct daily crane pre-operation inspection per IS 3938"
        ],
        "osha_threshold": "All standard OSHA 1926 construction requirements apply",
        "is_standard": "IS 456:2000, IS 3696, NBC 2016 Part 7 (Safety)"
    }
}
