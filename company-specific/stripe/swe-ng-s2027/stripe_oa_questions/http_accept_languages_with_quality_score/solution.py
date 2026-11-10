from typing import List

class Solution:
  def parseAcceptLanguageWithQuality(self, acceptHeader: str, supportedLanguages: List[str]) -> List[str]:
    lang_dict = {}
    
    for language in acceptHeader.strip().split(','):
      parts = language.strip().split(';')
      accepted_lang, quality = parts[0].strip(), 1
      if len(parts) == 2:
        _, value = parts[1].strip().split('=')
        quality = float(value)
      
      if len(accepted_lang) >= 2:
        if '-' in accepted_lang:
          if accepted_lang in supportedLanguages and accepted_lang not in lang_dict:
            lang_dict[accepted_lang] = quality
        else:
          for word in supportedLanguages:
            print(word)
            if accepted_lang in word and word not in lang_dict:
              lang_dict[word] = quality
              
      elif accepted_lang == '*':
        for word in supportedLanguages:
          if word not in lang_dict:
            lang_dict[word] = quality

    res = sorted(lang_dict.items(), key=lambda x: -x[1])
    result = []
    for lang, val in res:
      result.append(lang)
    return result
            
