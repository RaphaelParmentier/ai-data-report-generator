from __future__ import annotations

import json
import os
import re
from typing import Any

import google.genai as genai


def build_ai_audit_payload(analysis: dict[str, Any]) -> dict[str, Any]:
    """Keep only compact, non-sensitive audit information for the LLM."""
    return {
        "quality_score": analysis.get("quality_score"),
        "status": analysis.get("status"),
        "quality_summary": analysis.get("quality_summary"),
        "issues": analysis.get("issues", []),
        "recommendations": analysis.get("recommendations", []),
        "chart_data": {
            "missing_values_by_column": analysis.get("chart_data", {}).get(
                "missing_values_by_column", []
            ),
            "column_types_distribution": analysis.get("chart_data", {}).get(
                "column_types_distribution", []
            ),
        },
    }


def extract_json_from_model_response(raw_text: str) -> dict[str, Any]:
    """Parse JSON even if the model wraps it in markdown fences."""
    cleaned = raw_text.strip()

    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

        if json_match:
            return json.loads(json_match.group(0))

        raise


def generate_ai_insights(analysis: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    compact_payload = build_ai_audit_payload(analysis)

    prompt = f"""
Tu es un auditeur senior en qualité des données.

Tu reçois un audit déterministe produit par un moteur Python/Pandas.
Tu ne dois inventer aucune métrique.
Tu dois utiliser uniquement les informations présentes dans le JSON.
Ta réponse doit être en français professionnel, clair et exploitable.
Les champs JSON doivent rester en anglais.
Les valeurs de risk_level doivent rester exactement : low, medium ou high.

Retourne UNIQUEMENT un objet JSON valide.
N'ajoute pas de markdown.
N'ajoute pas de bloc ```json.
N'ajoute aucun commentaire hors JSON.

Schéma obligatoire :

{{
  "executive_summary": "Résumé exécutif en français, 3 à 5 phrases.",
  "risk_level": "low | medium | high",
  "business_impact": "Impact métier en français, concret et orienté décision.",
  "key_findings": [
    "Constat clé en français",
    "Constat clé en français"
  ],
  "priority_actions": [
    "Action prioritaire en français",
    "Action prioritaire en français"
  ],
  "technical_notes": [
    "Note technique courte en français",
    "Note technique courte en français"
  ]
}}

Audit JSON :
{json.dumps(compact_payload, ensure_ascii=False)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )

    raw_text = response.text or ""

    try:
        parsed = extract_json_from_model_response(raw_text)
    except Exception:
        return {
            "executive_summary": (
                "L’analyse IA a été générée, mais la réponse du modèle n’a pas "
                "pu être structurée correctement. Les diagnostics déterministes "
                "restent disponibles et fiables."
            ),
            "risk_level": "medium",
            "business_impact": (
                "La couche IA n’a pas pu être interprétée automatiquement. "
                "Utilisez les issues et recommandations déterministes pour guider "
                "les actions de nettoyage."
            ),
            "key_findings": [],
            "priority_actions": [],
            "technical_notes": [
                "La réponse brute du modèle n’était pas un JSON exploitable.",
            ],
        }

    return {
        "executive_summary": str(parsed.get("executive_summary", "")),
        "risk_level": parsed.get("risk_level", "medium"),
        "business_impact": str(parsed.get("business_impact", "")),
        "key_findings": list(parsed.get("key_findings", [])),
        "priority_actions": list(parsed.get("priority_actions", [])),
        "technical_notes": list(parsed.get("technical_notes", [])),
    }