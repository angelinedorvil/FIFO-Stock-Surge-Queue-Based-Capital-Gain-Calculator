#
# Capital Gain Calculator using Queues
#

from timeit import default_timer as timer
import sys

# ---- Class ArrayQueue (mostly from textbook, code fragments 6.6 and 6.7) ---- #
# ---- You do not need to modify this class. ---- #
class ArrayQueue:
	"""FIFO queue implementation using a Python list as underlying storage."""
	DEFAULT_CAPACITY = 10 # moderate capacity for all new queues
	
	def __init__(self):
		"""Create an empty queue."""
		self.data = [None] * ArrayQueue.DEFAULT_CAPACITY
		self.size = 0
		self.front = 0

	def len(self):
		"""Return the number of elements in the queue."""
		return self.size

	def is_empty(self):
		"""Return True if the queue is empty."""
		return self.size == 0

	def first(self):
		"""Return (but do not remove) the element at the front of the queue.
		Raise Empty exception if the queue is empty.
		"""
		if self.is_empty():
			raise Empty('Queue is empty') 
		return self.data[self.front]

	def dequeue(self):
		"""Remove and return the first element of the queue (i.e., FIFO).
		Raise Empty exception if the queue is empty.
		"""
		if self.is_empty():
			raise Empty('Queue is empty')
		answer = self.data[self.front]
		self.data[self.front] = None    	# help garbage collection
		self.front = (self.front + 1) % len(self.data)
		self.size -= 1
		return answer

	def enqueue(self, e):
		"""Add an element to the back of queue."""
		if self.size == len(self.data):         # if queue is full
			self.resize(2 *len(self.data))	# double the array size
		avail = (self.front + self.size) % len(self.data)
		self.data[avail] = e
		self.size += 1

	def resize(self, cap):	
		"""Resize to a new list of capacity >= len(self)."""
		old = self.data 			# keep track of existing list
		self.data = [None] * cap 		# allocate list with new capacity
		walk = self.front
		for k in range(self.size):		# only consider existing elements
			self.data[k] = old[walk]	# intentionally shift indices
			walk = (1 + walk) %len(old)	# use old size as modulus
		self.front = 0				# front has been realigned

	def replace_first(self, e): 
		"""Update the element at the front of the queue. """
		if self.is_empty():
			raise Empty('Queue is empty')
		self.data[self.front] = e

# -------- Main Program -------- #
# ----- Add your code here ----- #

# TO DO: start timer.
import time

# Start a timer to measure the program's execution time.
start = time.time()


# TO DO: Parse the command line arguments.
if len(sys.argv) != 2:
 raise ValueError('Please provide one file name.')

inputFileName = sys.argv[1]

print("\n**********************")
print("\nThe file that will be used for input is", inputFileName)
print("\n**********************")
print()


# DONE: Initialize a queue named q. Use this queue to store the "buy" transactions.
q = ArrayQueue()

# DONE: Initialize a variable to keep track of the overall capital gain.
totalGain = 0

# TO DO: Read text file. Each line is a "transaction".
#        For each transaction, update the queue (add, update, or remove elements).
#        For transactions of type "sell", print the capital gain for that transaction.

f = open("transactions.txt", "r")
myList = f.readlines()
f.close()

# Process each transaction from the file.
for line in myList:
        sections = line.split()
        transaction_type = sections[0]
        shares = int(sections[1])
        price = int(sections[4][1:])  #removing the dollar sign to make it easier for later
                
        transaction_info = (shares, price) #create tuple data to be used later for the 

        if transaction_type == "buy":
                q.enqueue(transaction_info)  #store the data for the shares that were bought
                print("Buy: {0} at ${1}" .format(shares, price))
        else:
                shares_sell = shares
                print("Sell: {0} at ${1}" .format(shares, price))
                capital_gain = 0
                while shares_sell > 0:
                        if q.is_empty():
                                print("All shares have been sold.")
                                break

                        buy_data = q.first()
                        buy_shares = buy_data[0]
                        buy_price = buy_data[1]
        
                        if buy_shares <= shares_sell:
                                q.dequeue()
                                transaction_capital_gain = buy_shares * (price - buy_price)
                                capital_gain += transaction_capital_gain
                                shares_sell -= buy_shares
                                totalGain += transaction_capital_gain
                        else:
                                q.replace_first((buy_shares - shares_sell, buy_price))
                                transaction_capital_gain = shares_sell * (price - buy_price)
                                capital_gain += transaction_capital_gain
                                totalGain += transaction_capital_gain
                                shares_sell = 0

                print("This transaction's capital gain is: ", capital_gain)
                print()

                             
       
# DONE: After processing the file, print the total capital gain for the entire sequence.
print("**********************")
print("The total capital gain is:", totalGain)

# TO DO: Print remaining elements in the queue.
print("\n**********************")
print("Shares remaining in the queue:")

while not q.is_empty():
    remain_data = q.first()
    remain_shares = remain_data[0]
    remain_price = remain_data[1]
    print("{0} shares bought at ${1} per share." .format(remain_shares, remain_price))
    q.dequeue()

# TO DO: end timer.
end = time.time()


# TO DO: Print program's runtime. 
totalTime = end - start
print("\nTotal time of program: {0} milliseconds".format(totalTime))


