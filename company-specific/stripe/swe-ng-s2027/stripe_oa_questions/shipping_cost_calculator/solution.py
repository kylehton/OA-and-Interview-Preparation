class Solution:
  def calculateMixedShippingCost(self, country: str, items: List[str], rules: List[str]) -> int:
    prices = {}
    for rule in rules:
      parts = rule.strip().split(',')
      ctr, itemName, priceType, minQuantity, maxQuantity, itemPrice = parts
      minQuantity, itemPrice = int(minQuantity), int(itemPrice)
      if ctr == country:
        if itemName not in prices:
          prices[itemName] = []
        prices[itemName].append((minQuantity, maxQuantity, itemPrice, priceType))

    for tiers in prices.values():
      tiers.sort(key=lambda x: x[0])

    costSum = 0
    for item in items:
      itemName, itemQuantity = item.strip().split(',')
      itemQuantity = int(itemQuantity)
      if itemName in prices:
        for minQ, maxQ, price, type in prices[itemName]:
          if itemQuantity == 0:
            break
            
          if maxQ != '*':
            maxQ = int(maxQ)
            maxCount = maxQ - minQ
            if maxCount > 0:
              unitsUsed = min(maxCount, itemQuantity)
              if type == 'incremental':
                costSum += unitsUsed * price
              elif type == 'fixed':
                costSum += price
              itemQuantity -= unitsUsed
          else:
            if type == 'incremental':
                costSum += itemQuantity * price
            elif type == 'fixed':
                costSum += price
            itemQuantity = 0

    return costSum


