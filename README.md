# MuslimBuddy
## About
A Discord bot for the Muslim community

## Description
- Reminds server members of prayer five times a day at the appointed times
- Commands include: 
  - `!hadith hadith_source`: Sends a random hadith from the given hadith source
    - hadith_source is one of: 'bukhari': (1, 7563), 'muslim': (1,3032), 'abudawud': (1,3998), 'ibnmajah': (1,4342), 'tirmidhi': (1,3956)
    - External API, custom script
  - `!surah chapter verse_start verse_end`: Get the verse from the chapter by the specified numbers 
  - `!mosque`: Sends a photo of a random mosque 
    - Custom API, custom script

## User Stories (Features)
- [X] Get random hadiths (Command)
- [X] Get ranges of verses from surahs (Command)
- [X] Bot reminds users of the five daily prayers at the appointed times
- [X] Send random mosque photo (Command)


## Technical Details
- APIs used:
    1. https://random-hadith-generator.vercel.app/
    2. https://quranenc.com/en/home/api/
- [ ] Bot should be hosted on a free-tier cloud hosting service like GCP (Cloud Compute) or AWS (EC2 or Lambda)


