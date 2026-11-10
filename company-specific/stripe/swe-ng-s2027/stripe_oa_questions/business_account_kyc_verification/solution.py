from typing import List

'''
normalization:
1. must check all csv parsed fields are nonempty
2. must not equal any strings within specified list
3. full_statement_descriptor must be 5 - 31 char after trim
'''

class Solution:
  def validateBusinesses(self, csvData: str) -> List[str]:
    
    GENERIC_DESCRIPTORS = {'ONLINE STORE', 'ECOMMERCE', 'RETAIL', 'SHOP', 'GENERAL MERCHANDISE'}
    GENERIC_TOKENS = {'THE', 'INC', 'INCORPORATED', 'LLC', 'LTD', 'LIMITED', 'CORP', 'CORPORATION', 'COMPANY', 'CO'}

    def tokenized_name(word: str) -> set:
      token_str = ""
      token_str = "".join(char.upper() if char.isascii() and char.isalnum() else " " for char in word)
      
      res = set(token_str.strip().split())
      for token in GENERIC_TOKENS:
        if token in res:
          res.remove(token)
      return res

    def token_overlap_valid(set1, set2) -> bool:
      if len(set1) == 0 or len(set2) == 0:
        return False
        
      small, large = None, None
      if len(set1) < len(set2):
        small, large = set1, set2
      else:
        small, large = set2, set1
      count = 0
      for token in small:
        if token in large:
          count += 1
      return (count/len(small) >= 0.5)

        
    rows = csvData.strip().split('\n')
    result = []
    
    for i in range(1, len(rows)):
      parts = rows[i].strip().split(',')
      res = ''
      if len(parts) != 6 or any(len(part) == 0 for part in parts):
        res = "NOT VERIFIED: " + parts[0] + " | MISSING_FIELD"
        
      else:
        business_name, business_profile_name, full_statement_descriptor, short_statement_descriptor, url, product_description = parts
        full_statement_descriptor = full_statement_descriptor.strip()
        
        if 5 <= len(full_statement_descriptor) <= 31:
          if full_statement_descriptor.upper() in GENERIC_DESCRIPTORS:
            res = "NOT VERIFIED: " + business_name + " | GENERIC_DESCRIPTOR"
          else:
            
            normalized_business_name = tokenized_name(business_name)
            normalized_profile_name = tokenized_name(business_profile_name)

            if not token_overlap_valid(normalized_business_name, normalized_profile_name):
              res = "NOT VERIFIED: " + parts[0] + " | NAME_MISMATCH"
            
        else:
          res = "NOT VERIFIED: " + parts[0] + " | INVALID_DESCRIPTOR_LENGTH"

      if not res:
        res = "VERIFIED: " + parts[0] + " | OK"
      result.append(res)
    return result