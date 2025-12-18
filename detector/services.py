import re
import spacy

nlp = spacy.load('en_core_web_sm')

OFFENSIVE_PATTERNS = {
    'profanity': [
        r'\b(damn|hell|crap|shit|fuck|bitch|ass|bastard|piss)\b',
        r'\b(wtf|stfu|lmao|lmfao)\b',
    ],
    'hate_speech': [
        r'\b(hate\s+you|hate\s+all|hate\s+every)\b',
        r'\b(racist|sexist|bigot)\b',
        r'\b(go\s+back\s+to)\b',
    ],
    'threats': [
        r'\b(kill\s+you|hurt\s+you|beat\s+you|destroy\s+you)\b',
        r'\b(gonna\s+die|will\s+die|you\'ll\s+die)\b',
        r'\b(attack|murder|assault)\b',
    ],
    'harassment': [
        r'\b(ugly|stupid|idiot|moron|loser|dumb|pathetic)\b',
        r'\b(shut\s+up|go\s+away|leave\s+me)\b',
        r'\b(nobody\s+likes|everyone\s+hates)\b',
    ],
    'toxic': [
        r'\b(toxic|disgusting|worthless|useless|garbage|trash)\b',
        r'\b(die|death|dead)\b',
    ],
}

SEVERITY_WEIGHTS = {
    'profanity': 0.4,
    'hate_speech': 0.8,
    'threats': 1.0,
    'harassment': 0.6,
    'toxic': 0.5,
}


def analyze_text(text):
    if not text or not text.strip():
        return {
            'is_offensive': False,
            'severity': 'safe',
            'confidence_score': 0.0,
            'categories': [],
            'flagged_terms': [],
            'analysis_details': {}
        }
    
    doc = nlp(text.lower())
    
    detected_categories = []
    flagged_terms = []
    category_matches = {}
    
    for category, patterns in OFFENSIVE_PATTERNS.items():
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text.lower())
            matches.extend(found)
        
        if matches:
            detected_categories.append(category)
            category_matches[category] = matches
            flagged_terms.extend(matches)
    
    negative_entities = []
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'NORP', 'GPE']:
            context_start = max(0, ent.start - 3)
            context_end = min(len(doc), ent.end + 3)
            context = doc[context_start:context_end].text.lower()
            
            negative_words = ['hate', 'stupid', 'ugly', 'bad', 'terrible', 'worst']
            if any(word in context for word in negative_words):
                negative_entities.append(ent.text)
    
    if negative_entities:
        if 'targeted_negativity' not in detected_categories:
            detected_categories.append('targeted_negativity')
        flagged_terms.extend(negative_entities)
    
    flagged_terms = list(set(flagged_terms))
    
    if detected_categories:
        max_weight = max(SEVERITY_WEIGHTS.get(cat, 0.3) for cat in detected_categories)
        term_factor = min(len(flagged_terms) * 0.1, 0.3)
        confidence_score = min(max_weight + term_factor, 1.0)
    else:
        confidence_score = 0.0
    
    if confidence_score == 0:
        severity = 'safe'
    elif confidence_score < 0.4:
        severity = 'mild'
    elif confidence_score < 0.7:
        severity = 'moderate'
    else:
        severity = 'severe'
    
    is_offensive = len(detected_categories) > 0
    
    return {
        'is_offensive': is_offensive,
        'severity': severity,
        'confidence_score': round(confidence_score, 2),
        'categories': detected_categories,
        'flagged_terms': flagged_terms,
        'analysis_details': {
            'word_count': len(doc),
            'entity_count': len(doc.ents),
            'category_matches': category_matches,
        }
    }
