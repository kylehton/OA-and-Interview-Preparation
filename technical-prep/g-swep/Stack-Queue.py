'''
Imagine a marketplace where individuals sell product "ABC." Sellers enter the market at any time and 
input their desired selling price for ABC into the market's computer system. The system then sorts 
this information (known as the order book) in ascending order of price. If multiple sellers offer 
the same price, their entries are further ordered by the time they entered the system (timestamp). 
This ensures that the seller with the lowest asking price is always the first to sell when a buyer 
arrives. All prices entered are in the range of $0.01 to $100.00. Each seller can only submit one 
order at a time (but may submit multiple orders), and each order can only offer one unit of product 
ABC.

Input:
- seller_id: A unique identifier for each seller.
- price: The price the seller is willing to sell ABC for.
- timestamp: The time the order was submitted.


Design two functions:

- insert_order(seller_id, price, timestamp): This function inserts the seller's order into the order 
book, ensuring proper sorting based on price and timestamp.

- get_lowest_seller_id(): This function returns the unique identifier of the seller currently offering
ABC at the lowest price and remove the seller from the order book (their product is sold!).
'''

class OrderBook:
    def __init__(self):
        self.orders = [[] for _ in range(10000)]  # hold tuples of (price, timestamp, seller_id)

    def insert_order(self, seller_id, price, timestamp):
        index = (int((price*100)-1))
        self.orders[index].append((price, timestamp, seller_id))

    def get_lowest_seller_id(self):
        index = 0
        while self.orders[index] == []:
            index += 1
        return self.orders[index][0][2]  # return seller_id of the first order at the lowest price
        
    def remove_entry(self, seller_id, price, timestamp):
        index = (int((price*100)-1))
        self.orders[index].remove((price, timestamp, seller_id))