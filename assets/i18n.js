/**
 * ANKR Labs Landing Page — i18n
 * Powered by @ankr/i18n (6 Indian languages)
 * Languages: en, hi, ta, te, kn, mr
 */
const LANGS = {
  en: { label: 'EN',    native: 'English',    flag: '🌐' },
  hi: { label: 'हिं',   native: 'हिंदी',      flag: '🇮🇳' },
  ta: { label: 'தமிழ்',native: 'தமிழ்',      flag: '🇮🇳' },
  te: { label: 'తె',   native: 'తెలుగు',    flag: '🇮🇳' },
  kn: { label: 'ಕನ್ನ', native: 'ಕನ್ನಡ',     flag: '🇮🇳' },
  mr: { label: 'मर',   native: 'मराठी',      flag: '🇮🇳' },
  bn: { label: 'বাং',  native: 'বাংলা',      flag: '🇮🇳' },
  gu: { label: 'ગુજ',  native: 'ગુજરાતી',   flag: '🇮🇳' },
  pa: { label: 'ਪੰਜ',  native: 'ਪੰਜਾਬੀ',    flag: '🇮🇳' },
  ml: { label: 'മല',   native: 'മലയാളം',    flag: '🇮🇳' },
  ur: { label: 'اردو', native: 'اردو',       flag: '🇮🇳' },
  or: { label: 'ଓଡ଼',  native: 'ଓଡ଼ିଆ',      flag: '🇮🇳' },
};

const T = {
  // EN intentionally EMPTY — index.html is the single source of truth for English.
  // A populated en{} dict silently overwrote HTML edits on every load (stale "AI Summit
  // 2026" copy survived an HTML rewrite, caught 2026-06-04). Switching back to EN is
  // handled by restoreOriginals() via data-orig snapshots, not this dict.
  en: {},
  hi: {
    badge:     'एजेंटिक OS · 9 इंजन लाइनें · 20 वर्टिकल · 231 सेवाएं · शून्य हैलुसिनेशन',
    h1a:       'एजेंटिक OS।',
    h1b:       'अनेक डोमेन के साथ।',
    hero_p:    'ANKR पहले एक एजेंटिक ऑपरेटिंग सिस्टम है — कर्नेल-स्तर एजेंट गवर्नेंस, बाइनरी-ट्रुथ कैपेबिलिटी ओरेकल, डोमेन SLM — और उसके बाद वर्टिकल्स का पोर्टफोलियो। हर सेवा घोषित करती है कि वह क्या जानती है — बिट सेट है या नहीं।',
    cta1:      'आर्किटेक्चर देखें ↓',
    cta2:      '84 Zenodo पेपर →',
    vert_tag:  'डोमेन कवरेज',
    vert_h:    'एक एजेंटिक OS।\nबीस वर्टिकल।',
    vert_p:    'मछुआरे से फंड मैनेजर तक, ट्रक ड्राइवर से जहाज कप्तान तक — हमारा AI आपकी भाषा बोलता है और असली समस्याएं सुलझाता है।',
    prod_tag:  'लाइव उत्पाद',
    prod_h:    'अभी चल रहे हैं।',
    prod_p:    'नीचे हर उत्पाद प्रोडक्शन में तैनात, परखा हुआ और आज ही उपलब्ध है।',
    plat_tag:  'AI प्लेटफ़ॉर्म',
    plat_h:    'इंजन रूम।',
    plat_p:    'मल्टी-प्रोवाइडर AI बैकबोन, पर्सिस्टेंट मेमोरी, और 800+ npm पैकेज हर उत्पाद को शक्ति देते हैं।',
    svc_tag:   'ANKR CTL',
    svc_h:     '231 सेवाएं।\nसभी Forja-नेटिव। सभी निगरानी में।',
    svc_p:     'हर सेवा ANKR CTL v5 के तहत AI Compass ऑटोपायलट के साथ चलती है।',
    cta_h:     'आइए साथ मिलकर बनाएं।',
    cta_p:     'हम भारत का AI इन्फ्रास्ट्रक्चर बना रहे हैं — एक-एक क्षेत्र करके। पार्टनरशिप, डेमो या पायलट के लिए संपर्क करें।',
    btn_interact: 'ANKR Interact खोलें →',
    btn_mari8x:   'Mari8X देखें →',
    btn_power:    'PowerP Box →',
    footer_copy:  '© 2026 ANKR Labs · भारत में निर्मित 🇮🇳 · हर भारतीय के लिए AI',
    explore:      'क्षमताएं देखें ↓',
    live_platform:'लाइव प्लेटफ़ॉर्म →',
  },
  ta: {
    badge:     'ஏஜெண்டிக் OS · 9 இன்ஜின் லைன்கள் · 20 வெர்டிகல்கள் · 231 சேவைகள்',
    h1a:       'ஏஜெண்டிக் OS.',
    h1b:       'பல டொமைன்களுடன்.',
    hero_p:    'ANKR முதலில் ஒரு ஏஜெண்டிக் இயக்க முறைமை — கர்னல்-நிலை ஏஜெண்ட் நிர்வாகம், பைனரி-உண்மை திறன் ஆரக்கிள்கள், டொமைன் SLM-கள் — பிறகே வெர்டிகல்களின் தொகுப்பு. ஒவ்வொரு சேவையும் தான் அறிந்ததை அறிவிக்கிறது.',
    cta1:      'கட்டமைப்பைப் பார்க்கவும் ↓',
    cta2:      '84 Zenodo ஆய்வுக் கட்டுரைகள் →',
    vert_tag:  'டொமைன் கவரேஜ்',
    vert_h:    'ஒரே ஏஜெண்டிக் OS.\nஇருபது வெர்டிகல்கள்.',
    vert_p:    'மீனவர் முதல் நிதி மேலாளர் வரை, லாரி ஓட்டுனர் முதல் கப்பல் கேப்டன் வரை — எங்கள் AI உங்கள் மொழியில் பேசுகிறது.',
    prod_tag:  'நேரடி தயாரிப்புகள்',
    prod_h:    'இப்போதே இயங்குகிறது.',
    prod_p:    'கீழே உள்ள ஒவ்வொரு தயாரிப்பும் உற்பத்தியில் பயன்படுத்தப்பட்டது, சோதிக்கப்பட்டது.',
    plat_tag:  'AI தளம்',
    plat_h:    'எஞ்சின் அறை.',
    plat_p:    'பல-வழங்குனர் AI முதுகெலும்பு, நிலையான நினைவகம், மற்றும் 800+ npm தொகுப்புகள்.',
    svc_tag:   'ANKR CTL',
    svc_h:     '231 சேவைகள்.\nஅனைத்தும் Forja-நேட்டிவ். அனைத்தும் கண்காணிக்கப்படுகின்றன.',
    svc_p:     'ஒவ்வொரு சேவையும் ANKR CTL v5 கீழ் AI Compass தன்னியக்க வழிகாட்டியுடன் இயங்குகிறது.',
    cta_h:     'ஒன்றாக கட்டுவோம்.',
    cta_p:     'இந்தியாவின் AI உள்கட்டமைப்பை நாங்கள் கட்டுகிறோம். கூட்டாண்மை, செயல்விளக்கம் அல்லது பைலட்டிற்கு தொடர்பு கொள்ளுங்கள்.',
    btn_interact: 'ANKR Interact திறக்கவும் →',
    btn_mari8x:   'Mari8X பார்க்கவும் →',
    btn_power:    'PowerP Box →',
    footer_copy:  '© 2026 ANKR Labs · இந்தியாவில் கட்டப்பட்டது 🇮🇳',
    explore:      'திறன்களை ஆராயுங்கள் ↓',
    live_platform:'நேரடி தளம் →',
  },
  te: {
    badge:     'ఏజెంటిక్ OS · 9 ఇంజిన్ లైన్లు · 20 వర్టికల్స్ · 231 సేవలు',
    h1a:       'ఏజెంటిక్ OS.',
    h1b:       'అనేక డొమైన్‌లతో.',
    hero_p:    'ANKR ముందుగా ఒక ఏజెంటిక్ ఆపరేటింగ్ సిస్టమ్ — కెర్నల్-స్థాయి ఏజెంట్ గవర్నెన్స్, బైనరీ-ట్రూత్ కెపాబిలిటీ ఒరాకిల్స్, డొమైన్ SLMలు — ఆ తర్వాతే వర్టికల్స్ పోర్ట్‌ఫోలియో. ప్రతి సేవ తనకు తెలిసింది ప్రకటిస్తుంది.',
    cta1:      'ఆర్కిటెక్చర్ చూడండి ↓',
    cta2:      '84 Zenodo పేపర్లు →',
    vert_tag:  'డొమైన్ కవరేజ్',
    vert_h:    'ఒకే ఏజెంటిక్ OS.\nఇరవై వర్టికల్స్.',
    vert_p:    'మత్స్యకారుల నుండి ఫండ్ మేనేజర్ల వరకు, ట్రక్ డ్రైవర్ల నుండి షిప్ కెప్టెన్ల వరకు — మా AI మీ భాషలో మాట్లాడుతుంది.',
    prod_tag:  'లైవ్ ఉత్పత్తులు',
    prod_h:    'ఇప్పుడే నడుస్తున్నాయి.',
    prod_p:    'దిగువ ప్రతి ఉత్పత్తి ప్రొడక్షన్‌లో మోహరించబడి, పరీక్షించబడి, నేడు అందుబాటులో ఉంది.',
    plat_tag:  'AI వేదిక',
    plat_h:    'ఇంజిన్ గది.',
    plat_p:    'మల్టీ-ప్రొవైడర్ AI వెన్నెముక, నిరంతర మెమరీ, మరియు 800+ npm ప్యాకేజీలు ప్రతి ఉత్పత్తికి శక్తినిస్తున్నాయి.',
    svc_tag:   'ANKR CTL',
    svc_h:     '231 సేవలు.\nఅన్నీ Forja-నేటివ్. అన్నీ పర్యవేక్షణలో.',
    svc_p:     'ప్రతి సేవా ANKR CTL v5 కింద AI Compass ఆటోపైలట్‌తో నడుస్తుంది.',
    cta_h:     'కలిసి నిర్మిద్దాం.',
    cta_p:     'భారత్ AI మౌలిక సదుపాయాలు నిర్మిస్తున్నాం — ఒక రంగం ఒక్కొక్కటిగా. భాగస్వామ్యం, డెమో లేదా పైలట్ కోసం సంప్రదించండి.',
    btn_interact: 'ANKR Interact తెరవండి →',
    btn_mari8x:   'Mari8X చూడండి →',
    btn_power:    'PowerP Box →',
    footer_copy:  '© 2026 ANKR Labs · భారత్‌లో నిర్మించబడింది 🇮🇳',
    explore:      'సామర్థ్యాలు అన్వేషించండి ↓',
    live_platform:'లైవ్ వేదిక →',
  },
  kn: {
    badge:     'ಏಜೆಂಟಿಕ್ OS · 9 ಇಂಜಿನ್ ಲೈನ್‌ಗಳು · 20 ವರ್ಟಿಕಲ್‌ಗಳು · 231 ಸೇವೆಗಳು',
    h1a:       'ಏಜೆಂಟಿಕ್ OS.',
    h1b:       'ಹಲವು ಡೊಮೇನ್‌ಗಳೊಂದಿಗೆ.',
    hero_p:    'ANKR ಮೊದಲು ಒಂದು ಏಜೆಂಟಿಕ್ ಆಪರೇಟಿಂಗ್ ಸಿಸ್ಟಮ್ — ಕರ್ನಲ್-ಮಟ್ಟದ ಏಜೆಂಟ್ ಆಡಳಿತ, ಬೈನರಿ-ಸತ್ಯ ಸಾಮರ್ಥ್ಯ ಒರಾಕಲ್‌ಗಳು, ಡೊಮೇನ್ SLMಗಳು — ನಂತರ ವರ್ಟಿಕಲ್‌ಗಳ ಪೋರ್ಟ್‌ಫೋಲಿಯೊ. ಪ್ರತಿ ಸೇವೆಯೂ ತನಗೆ ತಿಳಿದದ್ದನ್ನು ಘೋಷಿಸುತ್ತದೆ.',
    cta1:      'ಆರ್ಕಿಟೆಕ್ಚರ್ ನೋಡಿ ↓',
    cta2:      '84 Zenodo ಪೇಪರ್‌ಗಳು →',
    vert_tag:  'ಡೊಮೇನ್ ಕವರೇಜ್',
    vert_h:    'ಒಂದೇ ಏಜೆಂಟಿಕ್ OS.\nಇಪ್ಪತ್ತು ವರ್ಟಿಕಲ್‌ಗಳು.',
    vert_p:    'ಮೀನುಗಾರರಿಂದ ಫಂಡ್ ಮ್ಯಾನೇಜರ್‌ವರೆಗೆ — ನಮ್ಮ AI ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಮಾತನಾಡುತ್ತದೆ.',
    prod_tag:  'ನೇರ ಉತ್ಪನ್ನಗಳು',
    prod_h:    'ಈಗ ಚಾಲನೆಯಲ್ಲಿದೆ.',
    prod_p:    'ಕೆಳಗಿನ ಪ್ರತಿ ಉತ್ಪನ್ನವು ಪ್ರೊಡಕ್ಷನ್‌ನಲ್ಲಿ ನಿಯೋಜಿಸಲಾಗಿದೆ, ಪರೀಕ್ಷಿಸಲಾಗಿದೆ.',
    plat_tag:  'AI ವೇದಿಕೆ',
    plat_h:    'ಇಂಜಿನ್ ಕೋಣೆ.',
    plat_p:    'ಬಹು-ಪೂರೈಕೆದಾರ AI ಬೆನ್ನೆಲುಬು, ನಿರಂತರ ಸ್ಮರಣೆ, ಮತ್ತು 800+ npm ಪ್ಯಾಕೇಜ್‌ಗಳು.',
    svc_tag:   'ANKR CTL',
    svc_h:     '231 ಸೇವೆಗಳು.\nಎಲ್ಲವೂ Forja-ನೇಟಿವ್. ಎಲ್ಲವೂ ಮೇಲ್ವಿಚಾರಣೆಯಲ್ಲಿ.',
    svc_p:     'ಪ್ರತಿ ಸೇವೆಯೂ ANKR CTL v5 ಅಡಿ AI Compass ಆಟೋಪೈಲಟ್‌ನೊಂದಿಗೆ ಚಾಲನೆಯಲ್ಲಿದೆ.',
    cta_h:     'ಒಟ್ಟಿಗೆ ನಿರ್ಮಿಸೋಣ.',
    cta_p:     'ಭಾರತದ AI ಮೂಲಸೌಕರ್ಯ ನಿರ್ಮಿಸುತ್ತಿದ್ದೇವೆ. ಪಾಲುದಾರಿಕೆ, ಡೆಮೋ ಅಥವಾ ಪೈಲಟ್‌ಗಾಗಿ ಸಂಪರ್ಕಿಸಿ.',
    btn_interact: 'ANKR Interact ತೆರೆಯಿರಿ →',
    btn_mari8x:   'Mari8X ನೋಡಿ →',
    btn_power:    'PowerP Box →',
    footer_copy:  '© 2026 ANKR Labs · ಭಾರತದಲ್ಲಿ ನಿರ್ಮಿಸಲಾಗಿದೆ 🇮🇳',
    explore:      'ಸಾಮರ್ಥ್ಯಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ↓',
    live_platform:'ನೇರ ವೇದಿಕೆ →',
  },
  mr: {
    badge:     'एजेंटिक OS · 9 इंजिन लाइन्स · 20 व्हर्टिकल्स · 231 सेवा',
    h1a:       'एजेंटिक OS.',
    h1b:       'अनेक डोमेनसह.',
    hero_p:    'ANKR आधी एक एजेंटिक ऑपरेटिंग सिस्टम आहे — कर्नल-स्तरीय एजंट गव्हर्नन्स, बायनरी-ट्रुथ कॅपेबिलिटी ओरॅकल्स, डोमेन SLM — आणि नंतर व्हर्टिकल्सचा पोर्टफोलिओ. प्रत्येक सेवा स्वतःला काय माहीत आहे ते जाहीर करते.',
    cta1:      'आर्किटेक्चर पहा ↓',
    cta2:      '84 Zenodo पेपर्स →',
    vert_tag:  'डोमेन कव्हरेज',
    vert_h:    'एक एजेंटिक OS.\nवीस व्हर्टिकल्स.',
    vert_p:    'मासेमार ते फंड मॅनेजर, ट्रक चालक ते जहाज कप्तान — आमचा AI तुमच्या भाषेत बोलतो.',
    prod_tag:  'थेट उत्पादने',
    prod_h:    'आत्ता चालू आहे.',
    prod_p:    'खालील प्रत्येक उत्पादन प्रोडक्शनमध्ये तैनात, परीक्षित आणि आज उपलब्ध आहे.',
    plat_tag:  'AI व्यासपीठ',
    plat_h:    'इंजिन रूम.',
    plat_p:    'मल्टी-प्रोव्हायडर AI कणा, सतत मेमरी, आणि 800+ npm पॅकेजेस प्रत्येक उत्पादनाला शक्ती देतात.',
    svc_tag:   'ANKR CTL',
    svc_h:     '231 सेवा.\nसर्व Forja-नेटिव्ह. सर्व निगराणीत.',
    svc_p:     'प्रत्येक सेवा ANKR CTL v5 अंतर्गत AI Compass ऑटोपायलटसह चालते.',
    cta_h:     'चला एकत्र घडवूया.',
    cta_p:     'भारताची AI पायाभूत सुविधा बांधत आहोत — एका वेळी एक क्षेत्र. भागीदारी, डेमो किंवा पायलटसाठी संपर्क करा.',
    btn_interact: 'ANKR Interact उघडा →',
    btn_mari8x:   'Mari8X पहा →',
    btn_power:    'PowerP Box →',
    footer_copy:  '© 2026 ANKR Labs · भारतात बनवला 🇮🇳',
    explore:      'क्षमता एक्सप्लोर करा ↓',
    live_platform:'थेट व्यासपीठ →',
  },
};

// Map data-i18n attributes to their DOM queries
const SELECTORS = {
  badge:        '#i18n-badge',
  h1a:          '#i18n-h1a',
  h1b:          '#i18n-h1b',
  hero_p:       '#i18n-hero-p',
  cta1:         '#i18n-cta1',
  cta2:         '#i18n-cta2',
  vert_tag:     '#i18n-vert-tag',
  vert_h:       '#i18n-vert-h',
  vert_p:       '#i18n-vert-p',
  prod_tag:     '#i18n-prod-tag',
  prod_h:       '#i18n-prod-h',
  prod_p:       '#i18n-prod-p',
  plat_tag:     '#i18n-plat-tag',
  plat_h:       '#i18n-plat-h',
  plat_p:       '#i18n-plat-p',
  svc_tag:      '#i18n-svc-tag',
  svc_h:        '#i18n-svc-h',
  svc_p:        '#i18n-svc-p',
  cta_h:        '#i18n-cta-h',
  cta_p:        '#i18n-cta-p',
  btn_interact: '#i18n-btn-interact',
  btn_mari8x:   '#i18n-btn-mari8x',
  btn_power:    '#i18n-btn-power',
  footer_copy:  '#i18n-footer-copy',
  explore:      '#i18n-explore',
  live_platform:'#i18n-live-platform',
};

function applyLang(lang) {
  const strings = T[lang] || T.en;
  Object.entries(SELECTORS).forEach(([key, sel]) => {
    const el = document.querySelector(sel);
    if (el && strings[key] !== undefined) {
      el.textContent = strings[key];
    }
  });
  // Update active button
  document.querySelectorAll('.lang-btn').forEach(b => {
    b.classList.toggle('lang-active', b.dataset.lang === lang);
  });
  document.documentElement.lang = lang;
  localStorage.setItem('ankr-lang', lang);
}

// ─── AI Full-Page Translate (powered by @ankr/ai-translate) ──────────────────
// Auto-triggers on any non-English language selection — no button click needed.
// Endpoint: ankr.in/ai/translate/batch → @ankr/ai-translate → Sarvam/IndicTrans2/AI-Router
const AI_TRANSLATE_ENDPOINT = '/ai/translate/batch';
const AI_BATCH_SIZE = 25; // smaller batches = faster first paint + less timeout risk

// All translatable content. Excludes code/package .tag, numeric stats (.ti-n, .sm-v).
const AI_TRANSLATE_SELECTORS = [
  '[id^="i18n-"]',         // hero H1, CTAs, section heads, footer (all languages)
  '.vc-h', '.vc-p',        // 9 vertical cards
  '.sc-desc', '.sc-tagline', '.sc-cat',  // 12 product cards
  '.svc-name', '.svc-desc',// 42 service list items
  '.sm-k',                 // metric labels: "AIS positions", "Regulations live"
  '.bc-sub', '.bc-tag',    // big cards
  '.ti-l',                 // ticker labels: "Packages", "Live Services"
  '.pr-name', '.pr-note',  // partner rows
].join(',');

const aiCache  = {};   // lang → string[]
let aiActive   = false;
let aiLang     = null;

function getTranslatableEls() {
  return Array.from(document.querySelectorAll(AI_TRANSLATE_SELECTORS))
    .filter(el => !el.closest('[data-no-translate]') && el.textContent.trim().length > 1);
}

// ⚠️ Must be called on page load (English state) before applyLang() changes anything.
// Saves English originals so AI translate always sends English → target, not target → target.
function snapshotEnglishOriginals() {
  getTranslatableEls().forEach(el => {
    if (!el.dataset.orig) el.dataset.orig = el.textContent.trim();
  });
}

function restoreOriginals() {
  document.querySelectorAll('[data-orig]').forEach(el => { el.textContent = el.dataset.orig; });
  aiLang = null;
  setAiBadge(false);
  setAiBtn('🤖', false);
}

async function fetchBatch(texts, to) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 30000); // 30s timeout per batch
  try {
    const res = await fetch(AI_TRANSLATE_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texts, from: 'en', to, domain: 'general' }),
      signal: ctrl.signal,
    });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    return (data.results || []).map(r => r.translated || '');
  } finally {
    clearTimeout(timer);
  }
}

async function aiTranslatePage(lang) {
  if (lang === 'en') { restoreOriginals(); return; }
  if (aiActive) return;  // busy with another translation

  const els = getTranslatableEls();
  if (!els.length) return;

  // Serve from cache (re-apply even if aiLang === lang, since applyLang may have reset some)
  if (aiCache[lang]) {
    els.forEach((el, i) => { if (aiCache[lang][i]) el.textContent = aiCache[lang][i]; });
    aiLang = lang;
    setAiBadge(true);
    setAiBtn('✓', true);
    return;
  }

  aiActive = true;
  aiLang = null;
  setAiBtn('⏳', true);
  // Always use data-orig (English) as source — never the already-translated display text
  const texts = els.map(el => el.dataset.orig || el.textContent.trim());
  const all   = [];

  try {
    for (let i = 0; i < texts.length; i += AI_BATCH_SIZE) {
      const chunk  = texts.slice(i, i + AI_BATCH_SIZE);
      const result = await fetchBatch(chunk, lang);
      all.push(...result);
      result.forEach((t, j) => { if (t && els[i + j]) els[i + j].textContent = t; });
      const pct = Math.round((i + chunk.length) / texts.length * 100);
      setAiBtn(pct < 100 ? `⏳${pct}%` : '✓', true);
    }
    aiCache[lang] = all;
    aiLang = lang;
    setAiBadge(true);
    setAiBtn('✓', true);
  } catch (e) {
    console.warn('AI translate failed:', e);
    setAiBtn('⚠️', false);
    showToast('Translation failed — check console for details');
  } finally {
    aiActive = false;
  }
}

function showToast(msg) {
  const t = document.createElement('div');
  t.textContent = msg;
  t.style.cssText = 'position:fixed;bottom:1rem;left:50%;transform:translateX(-50%);' +
    'background:#1a1a2e;border:1px solid rgba(255,100,100,.4);color:#ff8080;' +
    'font-size:.75rem;padding:.5rem 1rem;border-radius:8px;z-index:9999;pointer-events:none;';
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 5000);
}

function setAiBadge(show) {
  let badge = document.getElementById('ai-pow-badge');
  if (!badge && show) {
    badge = document.createElement('div');
    badge.id = 'ai-pow-badge';
    badge.innerHTML = '🤖 Powered by <strong>@ankr/ai-translate</strong>';
    badge.style.cssText = [
      'position:fixed;bottom:5.5rem;left:1.5rem;z-index:7999',
      'background:rgba(0,0,0,.82);border:1px solid rgba(0,212,255,.3)',
      'color:rgba(0,212,255,.92);font-size:.6875rem;padding:.35rem .75rem',
      'border-radius:6px;backdrop-filter:blur(8px);pointer-events:none',
      'opacity:0;transition:opacity .4s',
    ].join(';');
    document.body.appendChild(badge);
  }
  if (badge) setTimeout(() => { badge.style.opacity = show ? '1' : '0'; }, 40);
}

function setAiBtn(text, active) {
  const btn = document.querySelector('.ai-translate-btn');
  if (!btn) return;
  btn.textContent = text;
  btn.style.opacity = active ? '1' : '0.55';
  btn.title = active ? 'Translation active — click to restore English' : 'AI Full-Page Translate';
}

(function init() {
  const saved = localStorage.getItem('ankr-lang') || 'en';
  document.addEventListener('DOMContentLoaded', () => {
    // ⚠️ Snapshot English originals FIRST — before applyLang() changes any text.
    // This ensures AI translate always sends English → target, never target → target.
    snapshotEnglishOriginals();

    applyLang(saved);
    // Auto-translate on startup if non-English saved
    if (saved !== 'en') aiTranslatePage(saved);

    document.querySelectorAll('.lang-btn:not(.ai-translate-btn)').forEach(btn => {
      btn.addEventListener('click', () => {
        const lang = btn.dataset.lang;
        aiLang = null; // reset so cache re-applies after applyLang() resets i18n elements
        applyLang(lang);
        if (lang !== 'en') {
          aiTranslatePage(lang);
        } else {
          restoreOriginals();
        }
      });
    });

    // 🤖 button — toggle off/on
    const aiBtn = document.querySelector('.ai-translate-btn');
    if (aiBtn) {
      aiBtn.addEventListener('click', () => {
        if (aiLang) {
          restoreOriginals();
          applyLang(document.documentElement.lang || 'en');
        } else {
          const lang = document.documentElement.lang || localStorage.getItem('ankr-lang') || 'en';
          if (lang !== 'en') aiTranslatePage(lang);
        }
      });
    }
  });
})();
