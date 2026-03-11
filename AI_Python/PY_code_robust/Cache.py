# import functools
# import hashlib
# import json

# # The student's memory — stores everything already learned
# CACHE = {}

# # The study manager — checks memory before opening the textbook
# def cache_predictions(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         # Create a unique fingerprint for this exact question
#         # Same question = same fingerprint, different question = different fingerprint
#         key_parts = [func.__name__] + list(args) + sorted([(k, v) for k, v in kwargs.items()])
#         cache_key = hashlib.md5(json.dumps(key_parts, sort_keys=True).encode()).hexdigest()

#         if cache_key in CACHE:
#             # Already learned this — answer in memory, no need to study again
#             print(f"MEMORY HIT: Already know this! Returning saved answer instantly...")
#             return CACHE[cache_key]
#         else:
#             # Never seen this question — open textbook, study hard, remember for next time
#             print(f"MEMORY MISS: New question! Studying hard...")
#             result = func(*args, **kwargs)
#             CACHE[cache_key] = result  # write in memory — never forget again
#             return result
#     return wrapper

# # The expensive AI worker — only called when memory has no answer
# @cache_predictions
# def get_sentiment_score(text: str, model_version: str = "v1"):
#     print(f"WORKER: Studying '{text[:20]}...' using model {model_version}")
#     if "happy" in text.lower() or "good" in text.lower():
#         return {"score": 0.9, "model": model_version}
#     elif "bad" in text.lower() or "sad" in text.lower():
#         return {"score": 0.1, "model": model_version}
#     else:
#         return {"score": 0.5, "model": model_version}

# print("--- First time — worker studies, writes in memory ---")
# result1 = get_sentiment_score("This is a really good day!", model_version="v2")

# print("\n--- Same question — memory has it, worker sleeps ---")
# result2 = get_sentiment_score("This is a really good day!", model_version="v2")

# print("\n--- Different question — worker wakes up again ---")
# result3 = get_sentiment_score("I am feeling very happy.", model_version="v1")

# print("\n--- Same as above — memory has it ---")
# result4 = get_sentiment_score("I am feeling very happy.", model_version="v1")

# print("\n--- Results ---")
# print(result1)
# print(result2)  # exact same as result1 — from memory, free of cost!
# print(result3)
# print(result4)  # exact same as result3 — from memory, free of cost!


### validation and transformation of intputs

import functools
import re

# The Agency — you call them with the rulebook
# "My club needs guests at least 20 chars long, and lowercase only"
def club_agency(min_length: int = 10, make_lowercase: bool = True):
    
    # Agency briefs the bouncer for THIS specific club
    def bouncer(club_entrance):
        @functools.wraps(club_entrance)
        def check_and_clean_guest(guest: str, *args, **kwargs):
            
            # Bouncer Check 1 — is this even a real guest?
            if not isinstance(guest, str):
                raise TypeError("You're not even a person! No entry.")
            
            # Bouncer Check 2 — are you tall enough to ride?
            if len(guest) < min_length:
                raise ValueError(f"Too short! This club needs at least {min_length} characters.")
            
            # Makeover counter — clean up before you meet the DJ
            clean_guest = guest.strip()                          # trim rough edges
            if make_lowercase:
                clean_guest = clean_guest.lower()               # no shouting inside
            clean_guest = re.sub(r'[^a-z0-9\s]', '', clean_guest)  # no weird symbols allowed
            
            print(f"BOUNCER: '{clean_guest[:30]}...' — you're clean, go in!")
            return club_entrance(clean_guest, *args, **kwargs)  # clean guest meets DJ
        return check_and_clean_guest
    return bouncer

# Strict club — long texts, lowercase only
@club_agency(min_length=20, make_lowercase=True)
def keyword_club(clean_guest: str):
    # DJ only sees clean guests
    print(f"DJ: Finding keywords in '{clean_guest[:30]}...'")
    keywords = [word for word in clean_guest.split() if len(word) > 4]
    return {"keywords": list(set(keywords))}

# Chill club — short texts allowed, case flexible
@club_agency(min_length=5, make_lowercase=False)
def summary_club(clean_guest: str):
    print(f"DJ: Summarising '{clean_guest[:30]}...'")
    summary = " ".join(clean_guest.split()[:5]) + "..."
    return {"summary": summary}

print("--- Valid guest entering strict club ---")
print(keyword_club("This is a very important document for keyword extraction."))

print("\n--- Valid guest entering chill club ---")
print(summary_club("Hello World! This is a short piece of text."))

print("\n--- Guest too short for strict club ---")
try:
    keyword_club("too short")
except ValueError as e:
    print(f"BOUNCER REJECTS: {e}")

print("\n--- Not even a real guest ---")
try:
    keyword_club(12345)
except TypeError as e:
    print(f"BOUNCER REJECTS: {e}")