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
  en: {
    badge:     'AI Summit 2026 · Building India\'s AI Infrastructure',
    h1a:       'Enterprise AI,',
    h1b:       'Built for Bharat.',
    hero_p:    'From maritime intelligence to voice AI in 22 Indian languages — we build the full-stack AI operating system powering logistics, compliance, fintech, and education for the common man and enterprise alike.',
    cta1:      'See Live Products ↓',
    cta2:      'Open ANKR Interact →',
    vert_tag:  'Core Specialisations',
    vert_h:    'Nine Verticals. One Platform.\nFor Every Indian.',
    vert_p:    'From fishermen to fund managers, truck drivers to ship captains, rural students to algo traders — our AI speaks your language and solves real problems.',
    prod_tag:  'Live Products',
    prod_h:    'Running. Right Now.',
    prod_p:    'Every product below is production-deployed, battle-tested, and accessible today.',
    plat_tag:  'AI Platform',
    plat_h:    'The Engine Room.',
    plat_p:    'Multi-provider AI backbone, persistent memory, and 202 packages powering every product in the ecosystem.',
    svc_tag:   'ANKR CTL',
    svc_h:     '40+ Live Services.\nAll Monitored. All Managed.',
    svc_p:     'Every service runs under ANKR CTL v5 with AI Compass autopilot — Prometheus metrics, auto-recovery, health checks, and AI-powered log analysis across 9 verticals.',
    cta_h:     'Let\'s Talk at the Summit.',
    cta_p:     'We\'re building India\'s AI infrastructure — one vertical at a time. Reach out to explore a partnership, demo, or pilot.',
    btn_interact: 'Open ANKR Interact →',
    btn_mari8x:   'Visit Mari8X →',
    btn_power:    'PowerPbox →',
    footer_copy:  '© 2026 ANKR Labs · Built in India 🇮🇳 · Making AI work for every Indian',
    explore:      'Explore Capabilities ↓',
    live_platform:'Live Platform →',
  },
  hi: {
    badge:     'AI शिखर सम्मेलन 2026 · भारत का AI इन्फ्रास्ट्रक्चर बना रहे हैं',
    h1a:       'एंटरप्राइज AI,',
    h1b:       'भारत के लिए बना।',
    hero_p:    'समुद्री बुद्धिमत्ता से 22 भारतीय भाषाओं में Voice AI तक — हम लॉजिस्टिक्स, कंप्लायंस, फिनटेक और शिक्षा के लिए पूर्ण AI ऑपरेटिंग सिस्टम बनाते हैं।',
    cta1:      'लाइव उत्पाद देखें ↓',
    cta2:      'ANKR Interact खोलें →',
    vert_tag:  'मुख्य विशेषज्ञताएं',
    vert_h:    'नौ क्षेत्र। एक प्लेटफ़ॉर्म।\nहर भारतीय के लिए।',
    vert_p:    'मछुआरे से फंड मैनेजर तक, ट्रक ड्राइवर से जहाज कप्तान तक — हमारा AI आपकी भाषा बोलता है और असली समस्याएं सुलझाता है।',
    prod_tag:  'लाइव उत्पाद',
    prod_h:    'अभी चल रहे हैं।',
    prod_p:    'नीचे हर उत्पाद प्रोडक्शन में तैनात, परखा हुआ और आज ही उपलब्ध है।',
    plat_tag:  'AI प्लेटफ़ॉर्म',
    plat_h:    'इंजन रूम।',
    plat_p:    'मल्टी-प्रोवाइडर AI बैकबोन, पर्सिस्टेंट मेमोरी, और 202 पैकेज हर उत्पाद को शक्ति देते हैं।',
    svc_tag:   'ANKR CTL',
    svc_h:     '40+ लाइव सेवाएं।\nसभी निगरानी में। सभी प्रबंधित।',
    svc_p:     'हर सेवा ANKR CTL v5 के तहत AI Compass ऑटोपायलट के साथ चलती है।',
    cta_h:     'शिखर सम्मेलन में मिलते हैं।',
    cta_p:     'हम भारत का AI इन्फ्रास्ट्रक्चर बना रहे हैं — एक-एक क्षेत्र करके। पार्टनरशिप, डेमो या पायलट के लिए संपर्क करें।',
    btn_interact: 'ANKR Interact खोलें →',
    btn_mari8x:   'Mari8X देखें →',
    btn_power:    'PowerPbox →',
    footer_copy:  '© 2026 ANKR Labs · भारत में निर्मित 🇮🇳 · हर भारतीय के लिए AI',
    explore:      'क्षमताएं देखें ↓',
    live_platform:'लाइव प्लेटफ़ॉर्म →',
  },
  ta: {
    badge:     'AI உச்சி மாநாடு 2026 · இந்தியாவின் AI உள்கட்டமைப்பை உருவாக்குகிறோம்',
    h1a:       'நிறுவன AI,',
    h1b:       'பாரதத்திற்காக கட்டப்பட்டது.',
    hero_p:    'கடல் நுண்ணறிவிலிருந்து 22 இந்திய மொழிகளில் குரல் AI வரை — தளவாட, இணக்கம், நிதி தொழில்நுட்பம் மற்றும் கல்விக்கான முழு AI இயக்க முறைமையை உருவாக்குகிறோம்.',
    cta1:      'நேரடி தயாரிப்புகளைப் பார்க்கவும் ↓',
    cta2:      'ANKR Interact திறக்கவும் →',
    vert_tag:  'முக்கிய நிபுணத்துவங்கள்',
    vert_h:    'ஒன்பது துறைகள். ஒரே தளம்.\nஒவ்வொரு இந்தியருக்கும்.',
    vert_p:    'மீனவர் முதல் நிதி மேலாளர் வரை, லாரி ஓட்டுனர் முதல் கப்பல் கேப்டன் வரை — எங்கள் AI உங்கள் மொழியில் பேசுகிறது.',
    prod_tag:  'நேரடி தயாரிப்புகள்',
    prod_h:    'இப்போதே இயங்குகிறது.',
    prod_p:    'கீழே உள்ள ஒவ்வொரு தயாரிப்பும் உற்பத்தியில் பயன்படுத்தப்பட்டது, சோதிக்கப்பட்டது.',
    plat_tag:  'AI தளம்',
    plat_h:    'எஞ்சின் அறை.',
    plat_p:    'பல-வழங்குனர் AI முதுகெலும்பு, நிலையான நினைவகம், மற்றும் 202 தொகுப்புகள்.',
    svc_tag:   'ANKR CTL',
    svc_h:     '40+ நேரடி சேவைகள்.\nஅனைத்தும் கண்காணிக்கப்படுகின்றன.',
    svc_p:     'ஒவ்வொரு சேவையும் ANKR CTL v5 கீழ் AI Compass தன்னியக்க வழிகாட்டியுடன் இயங்குகிறது.',
    cta_h:     'உச்சி மாநாட்டில் பேசுவோம்.',
    cta_p:     'இந்தியாவின் AI உள்கட்டமைப்பை நாங்கள் கட்டுகிறோம். கூட்டாண்மை, செயல்விளக்கம் அல்லது பைலட்டிற்கு தொடர்பு கொள்ளுங்கள்.',
    btn_interact: 'ANKR Interact திறக்கவும் →',
    btn_mari8x:   'Mari8X பார்க்கவும் →',
    btn_power:    'PowerPbox →',
    footer_copy:  '© 2026 ANKR Labs · இந்தியாவில் கட்டப்பட்டது 🇮🇳',
    explore:      'திறன்களை ஆராயுங்கள் ↓',
    live_platform:'நேரடி தளம் →',
  },
  te: {
    badge:     'AI సమ్మిట్ 2026 · భారత్ AI మౌలిక సదుపాయాలు నిర్మిస్తున్నాం',
    h1a:       'ఎంటర్‌ప్రైజ్ AI,',
    h1b:       'భారత్ కోసం నిర్మించబడింది.',
    hero_p:    'సముద్ర మేధస్సు నుండి 22 భారతీయ భాషలలో వాయిస్ AI వరకు — లాజిస్టిక్స్, కంప్లయన్స్, ఫిన్‌టెక్ మరియు విద్య కోసం పూర్తి AI నిర్వహణ వ్యవస్థను నిర్మిస్తున్నాం.',
    cta1:      'లైవ్ ఉత్పత్తులు చూడండి ↓',
    cta2:      'ANKR Interact తెరవండి →',
    vert_tag:  'ముఖ్య నైపుణ్యాలు',
    vert_h:    'తొమ్మిది రంగాలు. ఒకే వేదిక.\nప్రతి భారతీయుడికీ.',
    vert_p:    'మత్స్యకారుల నుండి ఫండ్ మేనేజర్ల వరకు, ట్రక్ డ్రైవర్ల నుండి షిప్ కెప్టెన్ల వరకు — మా AI మీ భాషలో మాట్లాడుతుంది.',
    prod_tag:  'లైవ్ ఉత్పత్తులు',
    prod_h:    'ఇప్పుడే నడుస్తున్నాయి.',
    prod_p:    'దిగువ ప్రతి ఉత్పత్తి ప్రొడక్షన్‌లో మోహరించబడి, పరీక్షించబడి, నేడు అందుబాటులో ఉంది.',
    plat_tag:  'AI వేదిక',
    plat_h:    'ఇంజిన్ గది.',
    plat_p:    'మల్టీ-ప్రొవైడర్ AI వెన్నెముక, నిరంతర మెమరీ, మరియు 202 ప్యాకేజీలు ప్రతి ఉత్పత్తికి శక్తి నిస్తున్నాయి.',
    svc_tag:   'ANKR CTL',
    svc_h:     '40+ లైవ్ సేవలు.\nన్నీ పర్యవేక్షించబడుతున్నాయి.',
    svc_p:     'ప్రతి సేవా ANKR CTL v5 కింద AI Compass ఆటోపైలట్‌తో నడుస్తుంది.',
    cta_h:     'సమ్మిట్‌లో మాట్లాడదాం.',
    cta_p:     'భారత్ AI మౌలిక సదుపాయాలు నిర్మిస్తున్నాం — ఒక రంగం ఒక్కొక్కటిగా. భాగస్వామ్యం, డెమో లేదా పైలట్ కోసం సంప్రదించండి.',
    btn_interact: 'ANKR Interact తెరవండి →',
    btn_mari8x:   'Mari8X చూడండి →',
    btn_power:    'PowerPbox →',
    footer_copy:  '© 2026 ANKR Labs · భారత్‌లో నిర్మించబడింది 🇮🇳',
    explore:      'సామర్థ్యాలు అన్వేషించండి ↓',
    live_platform:'లైవ్ వేదిక →',
  },
  kn: {
    badge:     'AI ಶೃಂಗಸಭೆ 2026 · ಭಾರತದ AI ಮೂಲಸೌಕರ್ಯ ನಿರ್ಮಿಸುತ್ತಿದ್ದೇವೆ',
    h1a:       'ಎಂಟರ್‌ಪ್ರೈಸ್ AI,',
    h1b:       'ಭಾರತಕ್ಕಾಗಿ ನಿರ್ಮಿಸಲಾಗಿದೆ.',
    hero_p:    'ಸಾಗರ ಬುದ್ಧಿಮತ್ತೆಯಿಂದ 22 ಭಾರತೀಯ ಭಾಷೆಗಳಲ್ಲಿ ಧ್ವನಿ AI ವರೆಗೆ — ಲಾಜಿಸ್ಟಿಕ್ಸ್, ಅನುಸರಣೆ, ಫಿನ್‌ಟೆಕ್ ಮತ್ತು ಶಿಕ್ಷಣಕ್ಕಾಗಿ ಸಂಪೂರ್ಣ AI ಆಪರೇಟಿಂಗ್ ಸಿಸ್ಟಮ್ ನಿರ್ಮಿಸುತ್ತಿದ್ದೇವೆ.',
    cta1:      'ನೇರ ಉತ್ಪನ್ನಗಳನ್ನು ನೋಡಿ ↓',
    cta2:      'ANKR Interact ತೆರೆಯಿರಿ →',
    vert_tag:  'ಮುಖ್ಯ ತಜ್ಞತೆಗಳು',
    vert_h:    'ಒಂಬತ್ತು ಕ್ಷೇತ್ರಗಳು. ಒಂದೇ ವೇದಿಕೆ.\nಪ್ರತಿ ಭಾರತೀಯನಿಗೂ.',
    vert_p:    'ಮೀನುಗಾರರಿಂದ ಫಂಡ್ ಮ್ಯಾನೇಜರ್‌ವರೆಗೆ — ನಮ್ಮ AI ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಮಾತನಾಡುತ್ತದೆ.',
    prod_tag:  'ನೇರ ಉತ್ಪನ್ನಗಳು',
    prod_h:    'ಈಗ ಚಾಲನೆಯಲ್ಲಿದೆ.',
    prod_p:    'ಕೆಳಗಿನ ಪ್ರತಿ ಉತ್ಪನ್ನವು ಪ್ರೊಡಕ್ಷನ್‌ನಲ್ಲಿ ನಿಯೋಜಿಸಲಾಗಿದೆ, ಪರೀಕ್ಷಿಸಲಾಗಿದೆ.',
    plat_tag:  'AI ವೇದಿಕೆ',
    plat_h:    'ಇಂಜಿನ್ ಕೋಣೆ.',
    plat_p:    'ಬಹು-ಪೂರೈಕೆದಾರ AI ಬೆನ್ನೆಲುಬು, ನಿರಂತರ ಸ್ಮರಣೆ, ಮತ್ತು 202 ಪ್ಯಾಕೇಜ್‌ಗಳು.',
    svc_tag:   'ANKR CTL',
    svc_h:     '40+ ನೇರ ಸೇವೆಗಳು.\nಎಲ್ಲವೂ ಮೇಲ್ವಿಚಾರಣೆಯಲ್ಲಿದೆ.',
    svc_p:     'ಪ್ರತಿ ಸೇವೆಯೂ ANKR CTL v5 ಅಡಿ AI Compass ಆಟೋಪೈಲಟ್‌ನೊಂದಿಗೆ ಚಾಲನೆಯಲ್ಲಿದೆ.',
    cta_h:     'ಶೃಂಗಸಭೆಯಲ್ಲಿ ಮಾತನಾಡೋಣ.',
    cta_p:     'ಭಾರತದ AI ಮೂಲಸೌಕರ್ಯ ನಿರ್ಮಿಸುತ್ತಿದ್ದೇವೆ. ಪಾಲುದಾರಿಕೆ, ಡೆಮೋ ಅಥವಾ ಪೈಲಟ್‌ಗಾಗಿ ಸಂಪರ್ಕಿಸಿ.',
    btn_interact: 'ANKR Interact ತೆರೆಯಿರಿ →',
    btn_mari8x:   'Mari8X ನೋಡಿ →',
    btn_power:    'PowerPbox →',
    footer_copy:  '© 2026 ANKR Labs · ಭಾರತದಲ್ಲಿ ನಿರ್ಮಿಸಲಾಗಿದೆ 🇮🇳',
    explore:      'ಸಾಮರ್ಥ್ಯಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ↓',
    live_platform:'ನೇರ ವೇದಿಕೆ →',
  },
  mr: {
    badge:     'AI शिखर परिषद 2026 · भारताची AI पायाभूत सुविधा बांधतो आहोत',
    h1a:       'एंटरप्राइज AI,',
    h1b:       'भारतासाठी बनवला.',
    hero_p:    'सागरी बुद्धिमत्तेपासून 22 भारतीय भाषांमध्ये व्हॉइस AI पर्यंत — लॉजिस्टिक्स, अनुपालन, फिनटेक आणि शिक्षणासाठी संपूर्ण AI ऑपरेटिंग सिस्टम बनवत आहोत.',
    cta1:      'थेट उत्पादने पहा ↓',
    cta2:      'ANKR Interact उघडा →',
    vert_tag:  'मुख्य विशेषज्ञता',
    vert_h:    'नऊ क्षेत्रे. एक व्यासपीठ.\nप्रत्येक भारतीयासाठी.',
    vert_p:    'मासेमार ते फंड मॅनेजर, ट्रक चालक ते जहाज कप्तान — आमचा AI तुमच्या भाषेत बोलतो.',
    prod_tag:  'थेट उत्पादने',
    prod_h:    'आत्ता चालू आहे.',
    prod_p:    'खालील प्रत्येक उत्पादन प्रोडक्शनमध्ये तैनात, परीक्षित आणि आज उपलब्ध आहे.',
    plat_tag:  'AI व्यासपीठ',
    plat_h:    'इंजिन रूम.',
    plat_p:    'मल्टी-प्रोव्हायडर AI कणा, सतत मेमरी, आणि 202 पॅकेजेस प्रत्येक उत्पादनाला शक्ती देतात.',
    svc_tag:   'ANKR CTL',
    svc_h:     '40+ थेट सेवा.\nसर्व निगराणीत. सर्व व्यवस्थापित.',
    svc_p:     'प्रत्येक सेवा ANKR CTL v5 अंतर्गत AI Compass ऑटोपायलटसह चालते.',
    cta_h:     'शिखर परिषदेत भेटूया.',
    cta_p:     'भारताची AI पायाभूत सुविधा बांधत आहोत — एका वेळी एक क्षेत्र. भागीदारी, डेमो किंवा पायलटसाठी संपर्क करा.',
    btn_interact: 'ANKR Interact उघडा →',
    btn_mari8x:   'Mari8X पहा →',
    btn_power:    'PowerPbox →',
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
const AI_BATCH_SIZE = 50;

// All translatable content — [id^="i18n-"] covers hero H1, CTAs, footer (works for
// ALL languages including those without static dictionary entries).
// Excludes code/package .tag, nav buttons, brand names, numeric stats (.ti-n).
const AI_TRANSLATE_SELECTORS = [
  '[id^="i18n-"]',
  '.hero-p', '.sec-h', '.sec-tag', '.sec-p',
  '.vc-h', '.vc-p',
  '.sc-desc', '.sc-tagline', '.sc-cat',
  '.svc-name', '.svc-desc',
  '.bc-sub', '.bc-tag',
  '.ti-l',
  '.pr-name', '.pr-note',
].join(',');

const aiCache  = {};   // lang → string[]
let aiActive   = false;
let aiLang     = null;

function getTranslatableEls() {
  return Array.from(document.querySelectorAll(AI_TRANSLATE_SELECTORS))
    .filter(el => !el.closest('[data-no-translate]') && el.textContent.trim().length > 1);
}

function saveOriginals(els) {
  els.forEach(el => { if (!el.dataset.orig) el.dataset.orig = el.textContent.trim(); });
}

function restoreOriginals() {
  document.querySelectorAll('[data-orig]').forEach(el => { el.textContent = el.dataset.orig; });
  aiLang = null;
  setAiBadge(false);
  setAiBtn('🤖', false);
}

async function fetchBatch(texts, to) {
  const res = await fetch(AI_TRANSLATE_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ texts, from: 'en', to, domain: 'general' }),
  });
  if (!res.ok) throw new Error('HTTP ' + res.status);
  const data = await res.json();
  return (data.results || []).map(r => r.translated || '');
}

async function aiTranslatePage(lang) {
  if (lang === 'en') { restoreOriginals(); return; }
  if (aiLang === lang) return;   // already applied
  if (aiActive) return;          // busy

  const els = getTranslatableEls();
  if (!els.length) return;
  saveOriginals(els);

  // Serve from cache instantly
  if (aiCache[lang]) {
    els.forEach((el, i) => { if (aiCache[lang][i]) el.textContent = aiCache[lang][i]; });
    aiLang = lang;
    setAiBadge(true);
    setAiBtn('✓', true);
    return;
  }

  aiActive = true;
  setAiBtn('⏳', true);
  const texts  = els.map(el => el.dataset.orig || el.textContent.trim());
  const all    = [];

  try {
    for (let i = 0; i < texts.length; i += AI_BATCH_SIZE) {
      const chunk  = texts.slice(i, i + AI_BATCH_SIZE);
      const result = await fetchBatch(chunk, lang);
      all.push(...result);
      // Apply each chunk as it arrives
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
    setAiBtn('🤖', false);
  } finally {
    aiActive = false;
  }
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
    applyLang(saved);
    // Auto-translate on startup if non-English saved
    if (saved !== 'en') aiTranslatePage(saved);

    document.querySelectorAll('.lang-btn:not(.ai-translate-btn)').forEach(btn => {
      btn.addEventListener('click', () => {
        const lang = btn.dataset.lang;
        applyLang(lang);
        // Always auto-trigger AI translate for non-English
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
