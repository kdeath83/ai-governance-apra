#!/usr/bin/env python3
"""
AI Governance Well-Architected Survey for APRA Regulated Entities
Maps current state to required AWS components
"""

import json
import sys
from typing import Dict, List, Any
from datetime import datetime

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{color.HEADER}{'='*60}{color.ENDC}")
    print(f"{color.BOLD}{text}{color.ENDC}")
    print(f"{color.HEADER}{'='*60}{color.ENDC}\n")

def ask_question(question: str, options: List[str], allow_multiple: bool = False) -> Any:
    print(f"{color.OKBLUE}? {question}{color.ENDC}")
    for i, opt in enumerate(options, 1):
        marker = "[ ]" if allow_multiple else "( )"
        print(f"  {marker} {i}. {opt}")
    
    if allow_multiple:
        print(f"\n  Enter numbers (comma-separated, e.g., 1,3,5) or 0 for none:")
        response = input("> ").strip()
        if response == "0":
            return []
        return [int(x.strip()) - 1 for x in response.split(",") if x.strip().isdigit()]
    else:
        print(f"\n  Enter number (1-{len(options)}):")
        while True:
            response = input("> ").strip()
            if response.isdigit() and 1 <= int(response) <= len(options):
                return int(response) - 1
            print(f"{color.FAIL}Invalid input. Please enter 1-{len(options)}{color.ENDC}")

def run_survey():
    results = {}
    
    print_header("AI GOVERNANCE WELL-ARCHITECTED SURVEY")
    print("For APRA Regulated Entities | v1.0")
    print("\nThis survey assesses your AI governance posture")
    print("and generates a customized deployment roadmap.\n")
    
    # Governance
    print_header("PILLAR 1: GOVERNANCE & STRATEGY")
    
    results['board_literacy'] = ask_question(
        "Does your Board have sufficient AI literacy?",
        ["Yes - Regular AI briefings", "Partial - Annual updates", "No - Lacks technical understanding", "Unknown"]
    )
    
    results['ai_strategy_documented'] = ask_question(
        "Is your AI strategy formally documented and Board-approved?",
        ["Yes - Documented and approved", "Partial - Informal", "No - No formal strategy", "In development"]
    )
    
    results['risk_appetite_defined'] = ask_question(
        "Do you have AI-specific risk appetite statements?",
        ["Yes - Quantified limits", "Partial - Qualitative only", "No - No AI-specific appetite", "Uses generic"]
    )
    
    # Risk
    print_header("PILLAR 2: RISK MANAGEMENT")
    
    results['model_inventory'] = ask_question(
        "Do you maintain an inventory of all AI models?",
        ["Yes - Complete with risk ratings", "Partial - Some tracked", "No - No inventory", "Unknown"]
    )
    
    results['validation_process'] = ask_question(
        "What validation occurs before AI deployment?",
        ["Independent red team + Board approval", "Internal testing + sign-off", "Vendor says it's safe", "Deploy first"]
    )
    
    results['monitoring_post_deploy'] = ask_question(
        "How do you monitor models after deployment?",
        ["Continuous monitoring", "Periodic review", "Reactive only", "No monitoring"]
    )
    
    # Audit
    print_header("PILLAR 3: AUDIT & COMPLIANCE")
    
    results['inference_logging'] = ask_question(
        "Do you log AI inference inputs/outputs for audit?",
        ["Yes - Complete 7-year trail", "Partial - API logs only", "No - No inference logging", "Vendor manages"]
    )
    
    results['cps_234_compliance'] = ask_question(
        "How do you address CPS 234 for AI?",
        ["Included in framework", "Basic controls", "Cloud provider only", "Not assessed"]
    )
    
    # Preferences
    print_header("DEPLOYMENT PREFERENCES")
    
    results['cost_tolerance'] = ask_question(
        "Monthly budget for AI governance tooling?",
        ["Near-zero (<$50)", "Low ($50-300)", "Medium ($300-1000)", "Enterprise ($1000+)"]
    )
    
    print_header("SURVEY COMPLETE!")
    return results

def calculate_score(results):
    score = 0
    for key, value in results.items():
        if isinstance(value, int):
            score += value * 10
    return min(100, score)

def generate_recommendations(results):
    with open('decision-matrix.json') as f:
        matrix = json.load(f)
    
    components = []
    for comp_id, rules in matrix['components'].items():
        score = 0
        for rule in rules['triggers']:
            q = rule['question']
            val = results.get(q)
            if rule['condition'] == 'less_than' and isinstance(val, int) and val < rule['threshold']:
                score += rule['weight']
        
        if score >= rules['deploy_threshold']:
            components.append({
                'id': comp_id,
                'name': rules['name'],
                'priority': rules['priority'],
                'file': rules['file'],
                'rationale': rules['rationale'],
                'estimated_cost': rules['estimated_cost']
            })
    
    components.sort(key=lambda x: x['priority'])
    return components

def main():
    try:
        results = run_survey()
        maturity = calculate_score(results)
        components = generate_recommendations(results)
        
        output = {
            'survey_results': results,
            'maturity_score': maturity,
            'maturity_level': 'Basic' if maturity < 33 else 'Developing' if maturity < 66 else 'Advanced',
            'recommended_components': components,
            'estimated_monthly_cost': sum(c['estimated_cost'] for c in components),
            'generated_at': datetime.now().isoformat()
        }
        
        with open('survey-results.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print_header("RESULTS")
        print(f"Maturity: {maturity}/100 ({output['maturity_level']})")
        print(f"Components: {len(components)}")
        print(f"Est. Cost: ${output['estimated_monthly_cost']}/mo\n")
        
        print(f"{color.OKGREEN}Recommended:{color.ENDC}")
        for comp in components:
            p_color = color.FAIL if comp['priority'] == 1 else color.WARNING if comp['priority'] == 2 else color.OKGREEN
            print(f"  {p_color}[P{comp['priority']}] {comp['name']}{color.ENDC} - ${comp['estimated_cost']}/mo")
        
        print(f"\n{color.OKBLUE}Next: python generate-deployment-guide.py{color.ENDC}")
        
    except KeyboardInterrupt:
        print(f"\n{color.WARNING}Cancelled.{color.ENDC}")
        sys.exit(0)

if __name__ == '__main__':
    main()