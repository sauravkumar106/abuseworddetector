"""
Hybrid content moderation service.

Primary scorer : detoxify (BERT trained on Jigsaw Toxic Comments dataset)
Secondary      : emoji detector (sexual / violent / vulgar emoji lists)
Fallback       : lightweight regex patterns (used if detoxify unavailable)
"""

import re
import logging

logger = logging.getLogger(__name__)

# ── Lazy-load detoxify model (singleton, loaded once at first call) ──────────
_detoxify_model = None
_detoxify_available = None   # None = unchecked, True/False after first call


def _get_model():
    global _detoxify_model, _detoxify_available
    if _detoxify_available is False:
        return None
    if _detoxify_model is not None:
        return _detoxify_model
    try:
        from detoxify import Detoxify
        _detoxify_model = Detoxify('original')
        _detoxify_available = True
        logger.info("detoxify BERT model loaded successfully.")
    except Exception as exc:
        logger.warning(f"detoxify unavailable, falling back to regex: {exc}")
        _detoxify_available = False
    return _detoxify_model


# ── Bad Emoji Definitions ────────────────────────────────────────────────────
BAD_EMOJIS = {
    'sexual': [
        '🍆', '🍑', '🍌', '🍒', '🫦', '💦', '🍭', '🌮', '🌭',
        '🥒', '🍯', '🍫', '🍬', '🎂', '💋', '😏', '🥵', '🔞',
        '👅', '🍓', '🍇', '🍈', '🍉',
    ],
    'violent': [
        '🔪', '🗡️', '⚔️', '💣', '🔫', '🪖', '☠️', '💀', '🩸',
        '🪓', '🧨', '💥', '🤜', '🤛', '👊', '🥊', '🪚',
    ],
    'vulgar': [
        '🖕', '💩', '🤮', '🤢', '🤬', '😤', '🤡', '💨', '💢',
        '🤦', '🙄', '😒',
    ],
}

_EMOJI_CATEGORY_MAP = {
    emoji: cat
    for cat, emojis in BAD_EMOJIS.items()
    for emoji in emojis
}

# ── Fallback Regex Patterns (used only when detoxify unavailable) ─────────────
_FALLBACK_PATTERNS = [
    (r'\b(fuck|shit|bitch|cunt|cock|dick|pussy|whore|slut)\b', 'Profanity', 0.85),
    (r'\b(kill\s+you|murder|i will hurt you|gonna die)\b',     'Threat',   0.90),
    (r'\b(n[i1]gg[ae]r|k[i1]ke|f[a4]gg[o0]t)\b',             'Hate Speech', 0.95),
    (r'\b(damn|hell|crap|ass|bastard|piss|wtf|stfu)\b',        'Profanity', 0.30),
    (r'\b(stupid|idiot|moron|loser|dumb|pathetic|ugly)\b',     'Harassment', 0.30),
    (r'\b(hate\s+you|worthless|useless|garbage|trash)\b',      'Harassment', 0.55),
    (r'\b(racist|sexist|bigot)\b',                             'Hate Speech', 0.70),
    (r'\b(toxic|disgusting|die|death|dead)\b',                 'Toxic', 0.45),
]

# ── Hindi Offensive Words (English transliteration) — always runs ────────────
# Extreme tier (score 0.90)
_HINDI_EXTREME = [
    r'\b(madarchod|madar\s*chod|m[a4]d[a4]rch[o0]d)\b',
    r'\b(bhenchod|bhen\s*chod|bh[e3]nch[o0]d)\b',
    r'\b(bhosdike|bh[o0]sdike|bh[o0]s\s*dike)\b',
    r'\b(randi|raand|r[a4]nd[i1])\b',
    r'\b(chutiya|ch[u]tiya|ch[u]t)\b',
    r'\b(lund|l[u]nd|lavda|l[a4]vd[a4])\b',
    r'\b(gaand|g[a4][a4]nd|gandu|g[a4]ndu)\b',
    r'\b(haramzada|har[a4]mzada|haramkhor)\b',
    r'\b(kutte|kamine|k[a4]mine|suar)\b',
]
# Moderate tier (score 0.45)
_HINDI_MODERATE = [
    r'\b(ullu|ulllu|bevakoof|bewakoof)\b',
    r'\b(bakwaas|bakwas|b[a4]kwas)\b',
    r'\b(pagal|p[a4]g[a4]l|chuttar)\b',
    r'\b(saala|sala|s[a4]la|saali|sali)\b',
    r'\b(gadha|gadhe|tharki|th[a4]rki)\b',
    r'\b(nalayak|n[a4]l[a4]yak|nikamma)\b',
]

# ── Bengali Offensive Words (English transliteration) — always runs ──────────
# Extreme tier (score 0.90)
_BENGALI_EXTREME = [
    r'\b(magi|m[a4]gi|maagi|m[a4][a4]gi)\b',
    r'\b(khankir\s*chele|khanki|kh[a4]nki)\b',
    r'\b(choda|chodi|ch[o0]d[a4]|banchod|b[a4]nchod)\b',
    r'\b(bokachoda|boka\s*choda|b[o0]k[a4]ch[o0]d[a4])\b',
    r'\b(shala|shali|sh[a4]l[a4])\b',
    r'\b(haramjada|har[a4]mjada|haramir\s*chele)\b',
    r'\b(randi|raand)\b',
]
# Moderate tier (score 0.45)
_BENGALI_MODERATE = [
    r'\b(boka|bok[a4]|b[o0]ka)\b',
    r'\b(gadha|g[a4]dh[a4]|goru)\b',
    r'\b(pagla|paagol|p[a4]g[a4])\b',
    r'\b(chup\s*kor|chup|ch[u]p)\b',
    r'\b(jhoot|jh[u]t|mithha)\b',
]

# Compile into a single unified always-on list: (pattern, label, score)
_REGIONAL_PATTERNS = (
    [(p, 'Hindi Offensive (Extreme)', 0.90) for p in _HINDI_EXTREME] +
    [(p, 'Hindi Offensive',           0.45) for p in _HINDI_MODERATE] +
    [(p, 'Bengali Offensive (Extreme)', 0.90) for p in _BENGALI_EXTREME] +
    [(p, 'Bengali Offensive',           0.45) for p in _BENGALI_MODERATE]
)

# ── Mode Thresholds ────────────────────────────────────────────────────────────
# Keys match detoxify output keys
_KID_THRESHOLDS = {
    'toxicity':        0.15,
    'severe_toxicity': 0.05,
    'obscene':         0.10,
    'threat':          0.10,
    'insult':          0.15,
    'identity_attack': 0.10,
}

_ADULT_THRESHOLDS = {
    'toxicity':        0.75,
    'severe_toxicity': 0.50,
    'obscene':         0.70,
    'threat':          0.60,
    'insult':          0.80,
    'identity_attack': 0.65,
}

# Human-readable labels for ML categories
_ML_CATEGORY_LABELS = {
    'toxicity':        'Toxic',
    'severe_toxicity': 'Severely Toxic',
    'obscene':         'Obscene',
    'threat':          'Threat',
    'insult':          'Insult',
    'identity_attack': 'Hate Speech',
}


# ── Emoji Detection ────────────────────────────────────────────────────────────
def detect_emojis(text):
    """Return list of {emoji, category} for each bad emoji found."""
    found = []
    seen = set()
    for char in text:
        if char in _EMOJI_CATEGORY_MAP and char not in seen:
            seen.add(char)
            found.append({'emoji': char, 'category': _EMOJI_CATEGORY_MAP[char]})
    return found


# ── ML Scoring ─────────────────────────────────────────────────────────────────
def _ml_score(text):
    """
    Run detoxify on text.
    Returns dict of {key: float} scores, or None if unavailable.
    """
    model = _get_model()
    if model is None:
        return None
    try:
        raw = model.predict(text)
        # raw values are numpy floats → convert to plain Python floats
        return {k: float(v) for k, v in raw.items()}
    except Exception as exc:
        logger.warning(f"detoxify prediction failed: {exc}")
        return None


# ── Fallback Regex Scoring ─────────────────────────────────────────────────────
def _regex_score(text):
    """Simple regex fallback. Returns (max_weight, categories, flagged_terms)."""
    text_lower = text.lower()
    categories = []
    flagged_terms = []
    max_weight = 0.0

    for pattern, cat, weight in _FALLBACK_PATTERNS:
        found = re.findall(pattern, text_lower)
        if found:
            if cat not in categories:
                categories.append(cat)
            flagged_terms.extend(found)
            max_weight = max(max_weight, weight)

    return max_weight, list(set(categories)), list(set(flagged_terms))


# ── Main Analysis ──────────────────────────────────────────────────────────────
def analyze_text(text, mode='adult'):
    """
    Analyze text for offensive content using hybrid ML + emoji detection.

    Args:
        text: The text to analyze.
        mode: 'kid' flags mild content; 'adult' flags only extreme content.

    Returns dict with:
        is_offensive, severity, confidence_score, categories,
        flagged_terms, emoji_detections, ml_scores, mode, analysis_details
    """
    mode = mode if mode in ('kid', 'adult') else 'adult'
    thresholds = _KID_THRESHOLDS if mode == 'kid' else _ADULT_THRESHOLDS

    if not text or not text.strip():
        return {
            'is_offensive': False,
            'severity': 'safe',
            'confidence_score': 0.0,
            'categories': [],
            'flagged_terms': [],
            'emoji_detections': [],
            'ml_scores': {},
            'mode': mode,
            'analysis_details': {'engine': 'n/a'},
        }

    # 1. Emoji detection (always runs, fast)
    emoji_detections = detect_emojis(text)

    # 2. ML scoring (primary)
    ml_scores = _ml_score(text)
    engine = 'detoxify-bert'

    detected_categories = []
    flagged_terms = []
    confidence_score = 0.0

    if ml_scores is not None:
        # Find which ML categories breach the threshold
        for key, score in ml_scores.items():
            if key in thresholds and score >= thresholds[key]:
                label = _ML_CATEGORY_LABELS.get(key, key.replace('_', ' ').title())
                detected_categories.append(label)

        # Confidence = highest ML score (weighted towards most serious dimensions)
        ml_confidence = max(
            ml_scores.get('toxicity', 0) * 0.9,
            ml_scores.get('severe_toxicity', 0) * 1.0,
            ml_scores.get('obscene', 0) * 0.85,
            ml_scores.get('threat', 0) * 1.0,
            ml_scores.get('insult', 0) * 0.8,
            ml_scores.get('identity_attack', 0) * 0.95,
        )
        confidence_score = round(min(ml_confidence, 1.0), 3)

    else:
        # 3. Fallback: regex
        engine = 'regex-fallback'
        max_weight, categories, terms = _regex_score(text)
        detected_categories = categories
        flagged_terms = terms
        confidence_score = round(min(max_weight, 1.0), 3)

    # 3. Always run regional (Hindi / Bengali transliteration) patterns
    text_lower = text.lower()
    _regional_threshold = 0.1 if mode == 'kid' else 0.7  # adult only flags extreme regional words
    for pattern, label, weight in _REGIONAL_PATTERNS:
        if re.search(pattern, text_lower):
            terms_found = re.findall(pattern, text_lower)
            flagged_terms.extend(terms_found)
            if weight >= _regional_threshold:
                if label not in detected_categories:
                    detected_categories.append(label)
                confidence_score = max(confidence_score, weight)
    flagged_terms = list(set(flagged_terms))

    # 4. Factor in bad emojis
    if emoji_detections:
        if mode == 'kid':
            # Even a single bad emoji = flagged in kid mode
            for det in emoji_detections:
                label = f"Bad Emoji ({det['category'].title()})"
                if label not in detected_categories:
                    detected_categories.append(label)
            confidence_score = max(confidence_score, 0.4)
        else:
            # Adult: sexual/violent emojis raise the score significantly
            for det in emoji_detections:
                if det['category'] in ('sexual', 'violent'):
                    boost = 0.75
                    label = f"Bad Emoji ({det['category'].title()})"
                    if label not in detected_categories:
                        detected_categories.append(label)
                    confidence_score = max(confidence_score, boost)
                else:
                    # Vulgar emoji in adult mode: minor boost
                    confidence_score = max(confidence_score, 0.3)

    # 5. Determine is_offensive based on mode
    is_offensive = len(detected_categories) > 0

    # 6. Severity label based on overall confidence score
    if confidence_score == 0 or not is_offensive:
        severity = 'safe'
    elif confidence_score < 0.35:
        severity = 'mild'
    elif confidence_score < 0.65:
        severity = 'moderate'
    else:
        severity = 'severe'

    return {
        'is_offensive': is_offensive,
        'severity': severity,
        'confidence_score': round(confidence_score, 3),
        'categories': detected_categories,
        'flagged_terms': flagged_terms,   # ML mode returns [] (BERT doesn't extract tokens)
        'emoji_detections': emoji_detections,
        'ml_scores': ml_scores or {},
        'mode': mode,
        'analysis_details': {
            'engine': engine,
        },
    }
