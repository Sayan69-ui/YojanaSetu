import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
BASE = 'http://127.0.0.1:8000'

def test_query(title, message, language='auto', history=None):
    payload = {'message': message, 'language': language, 'history': history or []}
    req = urllib.request.Request(
        f'{BASE}/api/chat',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"=== {title} ===")
        print(f"Lang: {res['detected_language']}")
        print(f"Sources: {[s['title'] for s in res['sources']]}")
        print(f"Reply Preview (first 200 chars):\n{res['reply'][:200].strip()}...\n")
        return res

print('>>> TEST 1: What is Ayushman Bharat PM-JAY? (English)')
t1 = test_query('Test 1: What is PM-JAY', 'What is Ayushman Bharat PM-JAY?', 'en')
assert 'Ayushman' in t1['reply'] or 'PM-JAY' in t1['reply']
assert '5,00,000' in t1['reply'] or '5 Lakh' in t1['reply'] or '5 lakh' in t1['reply']

print('>>> TEST 2: Who is eligible for PM-JAY? (English)')
t2 = test_query('Test 2: Eligibility', 'Who is eligible for PM-JAY?', 'en')
assert 'Who can benefit' in t2['reply'] or 'Eligib' in t2['reply']

print('>>> TEST 3: What benefits does PM-JAY provide? (English)')
t3 = test_query('Test 3: Benefits', 'What benefits does PM-JAY provide?', 'en')
assert '5,00,000' in t3['reply'] or '5 Lakh' in t3['reply'] or 'Benefits' in t3['reply']

print('>>> TEST 4: How can I apply for PM-JAY? (English)')
t4 = test_query('Test 4: Apply', 'How can I apply for PM-JAY?', 'en')
assert 'Apply' in t4['reply'] or 'Portal' in t4['reply'] or 'pmjay.gov.in' in t4['reply']

print('>>> TEST 5: Hindi questions (हिन्दी)')
t5 = test_query('Test 5: Hindi What is it', 'आयुष्मान भारत पीएम-जेएवाई योजना क्या है?', 'hi')
assert 'योजना क्या है' in t5['reply'] or 'आयुष्मान' in t5['reply']

print('>>> TEST 6: Hinglish questions')
t6 = test_query('Test 6: Hinglish What is it', 'Ayushman Bharat PM-JAY kya hai aur benefits kya hain?', 'hinglish')
assert 'Yojana Kya Hai' in t6['reply'] or 'scheme' in t6['reply'].lower() or 'benefits' in t6['reply'].lower()

print('>>> TEST 7: Bengali questions (বাংলা)')
t7 = test_query('Test 7: Bengali What is it', 'আয়ুষ্মান ভারত যোজনা কি এবং এর সুবিধা কি?', 'bn')
assert 'এটি কি' in t7['reply'] or 'আয়ুষ্মান' in t7['reply']

print('>>> TEST 8: Follow-up question with history: What documents do I need?')
hist = [
    {'sender': 'user', 'text': 'What is Ayushman Bharat PM-JAY?'},
    {'sender': 'bot', 'text': t1['reply']}
]
t8 = test_query('Test 8: Follow-up Documents', 'What documents do I need?', 'en', history=hist)
assert 'Aadhaar' in t8['reply'] or 'Ration' in t8['reply']
assert len(t8['sources']) > 0 and 'Ayushman' in t8['sources'][0]['title']

print('>>> TEST 9: Query for another government scheme (PM-KISAN)')
t9 = test_query('Test 9: PM-KISAN', 'पीएम किसान सम्मान निधि योजना क्या है?', 'hi')
assert '6,000' in t9['reply'] or '६,০০০' in t9['reply'] or '6000' in t9['reply']

print('>>> TEST 10: Non-existent scheme query')
t10 = test_query('Test 10: Non-existent scheme', 'What is the Alien Galaxy Welfare Scheme 2026?', 'en')
assert 'could not find' in t10['reply'].lower() or 'not found' in t10['reply'].lower()
assert len(t10['sources']) == 0

print('>>> TEST 11: Language override test (Hindi query but English selected)')
t11 = test_query('Test 11: Lang Override', 'मुझे लोन चाहिए', 'en')
assert t11['detected_language'] == 'en'

print('>>> TEST 12: Supported languages endpoint')
with urllib.request.urlopen(f'{BASE}/api/languages') as resp:
    langs = json.loads(resp.read().decode('utf-8'))['languages']
    lang_codes = [l['code'] for l in langs]
    print('Supported Language Codes:', lang_codes)
    assert 'ta' not in lang_codes
    assert 'te' not in lang_codes
    assert set(lang_codes) == {'auto', 'hi', 'en', 'hinglish', 'bn'}

print('\n=========================================')
print('ALL 12 RIGOROUS QUALITY TESTS PASSED!')
print('=========================================')
