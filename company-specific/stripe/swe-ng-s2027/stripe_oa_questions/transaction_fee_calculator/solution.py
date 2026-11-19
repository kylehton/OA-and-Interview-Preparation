from typing import List

class Solution:
    def calculateDiscountedFees(self, csvData: str, countryFees: List[List[str]]) -> List[str]:
        RESULT_HEADER = "id,transaction_type,payment_provider,fee"
        csvToList = csvData.strip().split()

        transaction_counts = {}
        country_fees = {}

        for ctr, provider, p, u in countryFees: 
            if ctr not in country_fees:
                country_fees[ctr] = {}
            country_fees[ctr][provider] = (float(p)/10000, int(u))
        
        result = []
        result.append(RESULT_HEADER)
        
        for i in range(1, len(csvToList)):
            id, ref, amount, cur, date, merchant_id, buyer_ctr, transaction_type, payment_provider, status = csvToList[i].strip().split(',')
            
            amount = int(amount)
            res_string = ''

            if merchant_id not in transaction_counts:
                transaction_counts[merchant_id] = 0
            if status == 'payment_completed':
                transaction_counts[merchant_id] += 1
                if buyer_ctr in country_fees:
                    percent, unit = country_fees[buyer_ctr][payment_provider]
                else:
                    percent, unit = country_fees['default'][payment_provider]

                fee = (amount * percent) + unit
                    
                merchant_count = transaction_counts[merchant_id]
                if merchant_count >= 101:
                    fee *= 0.8
                elif merchant_count >= 51:
                    fee *= 0.85
                elif merchant_count >= 11:
                    fee *= 0.9
                    
                fee = str(int(fee))
                res_string = ",".join([id, transaction_type, payment_provider, fee])
            else:
                res_string = ",".join([id, transaction_type, payment_provider, '0'])

            result.append(res_string)
        return result
            