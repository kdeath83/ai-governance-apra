#!/usr/bin/env python3
"""
Generate customized deployment guide based on survey results
"""
import json
from datetime import datetime

def load_survey_results():
    with open('survey-results.json') as f:
        return json.load(f)

def generate_guide(data):
    components = data['recommended_components']
    maturity = data['maturity_score']
    
    guide = f"""# Customized Deployment Guide
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

### Your AI Governance Maturity: {maturity}/100 ({data['maturity_level']})

### Recommended Components ({len(components)} total, ${data['estimated_monthly_cost']}/mo)

"""
    
    for comp in sorted(components, key=lambda x: x['priority']):
        priority_label = "🔴 CRITICAL" if comp['priority'] == 1 else "🟡 HIGH" if comp['priority'] == 2 else "🟢 MEDIUM"
        guide += f"""
#### {priority_label}: {comp['name']}
- **File:** `{comp['file']}`
- **Monthly Cost:** ${comp['estimated_cost']}
- **Why:** {comp['rationale']}

**Deployment:**
```bash
# Step for {comp['name']}
./{comp['file']}
```

---
"""
    
    guide += f"""
### Deployment Order (by Priority)

"""
    
    p1 = [c for c in components if c['priority'] == 1]
    p2 = [c for c in components if c['priority'] == 2]
    p3 = [c for c in components if c['priority'] == 3]
    
    if p1:
        guide += "**Phase 1 - Critical (Deploy First):**\n"
        for c in p1:
            guide += f"- [ ] {c['name']}\n"
    
    if p2:
        guide += "\n**Phase 2 - High Priority:**\n"
        for c in p2:
            guide += f"- [ ] {c['name']}\n"
    
    if p3:
        guide += "\n**Phase 3 - Medium Priority:**\n"
        for c in p3:
            guide += f"- [ ] {c['name']}\n"
    
    guide += """
### Next Steps

1. Review the components above
2. Deploy in priority order (Phase 1 first)
3. Validate each component before proceeding
4. Run `python survey.py` quarterly to reassess

### Support

- Issues: https://github.com/kdeath83/ai-governance-apra/issues
- APRA Letter: https://www.apra.gov.au/ai-letter
"""
    
    return guide

def main():
    data = load_survey_results()
    guide = generate_guide(data)
    
    filename = 'DEPLOYMENT-GUIDE.md'
    with open(filename, 'w') as f:
        f.write(guide)
    
    print(f"Generated: {filename}")
    print(f"Components: {len(data['recommended_components'])}")
    print(f"Monthly cost: ${data['estimated_monthly_cost']}")

if __name__ == '__main__':
    main()