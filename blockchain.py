from functools import reduce
from collections import OrderedDict

from hash_util import hash_block,hash_string_256

# The reward we give to miners
MINING_REWARD=10

# Starting block for the blockchain 
genesis_block={
        "previous_hash":'',
        'index':0,
        'transactions':[],
        'proof':100
}
# Initializing our blockchain list ()
blockchain=[genesis_block]
# Unhandlen transaction list
open_transactions=[]
# We are the owneh of this blockchain node
owner='Hubert'
# Registered participants: Ourselfs + other people sending/receiving coins
participant={'Hubert'}

def load_data():
      with open('blockchain.txt',mode='r') as f:        
        file_content=f.readlines()
        global blockchain
        global open_transactions
        blockchain=file_content[0]
        open_transactions=file_content[1]
        
load_data()

def save_data():
    with open('blockchain.txt',mode='w') as f:
        f.write(str(blockchain))
        f.write('\n')
        f.write(str(open_transactions))
        

def valid_proof(transactions,last_hash,proof_number):
    guess = (str(transactions)+str(last_hash)+str(proof_number)).encode()
    guess_hash=hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] =='00'
    
def proof_of_work():
    last_block=blockchain[-1]
    last_hash=hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions,last_hash,proof):
        proof+=1
    return proof



def get_balance(participant):
    """Calculate and return the balance for a participant.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
   
    tx_sender=[[tx['amount'] for tx  in block['transactions'] if tx['sender']==participant] for block in blockchain]
  
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
   
    open_tx_sender=[tx['amount'] for tx in open_transactions if tx['sender']==participant]
    
    tx_sender.append(open_tx_sender)
    amount_sent=reduce(lambda tx_sum,tx_amt: tx_sum+sum(tx_amt) if len(tx_amt)>0 else tx_sum+0,tx_sender,0)
    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient=[[tx['amount'] for tx  in block['transactions'] if tx['recipient']==participant] for block in blockchain]
    amount_received=reduce(lambda tx_sum,tx_amt: tx_sum+sum(tx_amt) if len(tx_amt)>0 else tx_sum+0,tx_recipient,0)
    # Return the total balance
    return amount_received-amount_sent

# Last blockchain value
def get_last_blockchain_value():
    """ Return the last value of the current blockchain"""
    if len(blockchain)<1:
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    """Verify a transaction by checking whether the sender has sufficient coins.

    Arguments:
        :transaction: The transaction that should be verified.
    """
    sender_balance = get_balance(transaction['sender'])
    return sender_balance>= transaction['amount']        
    

# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]


def add_transaction(recipient,sender=owner,amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain
    
    Arguments:
        :sender: The sender of the coins.
        :recipient: The reciient of the coins
        :amount: The amount of coins sent with the transition
    """
    # transaction = {
    #     "sender":sender,
    #     "recipient":recipient,
    #     "amount":amount
    # }
    transaction=OrderedDict([('sender',sender),('recipient',recipient),('amount',amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participant.add(sender)
        participant.add(recipient)
        save_data()
        return True
    return False
    
    

#Process open transactions
def mine_block():
    """Create a new block and add open transactions to it."""
    # Fetch the currently las block of the blockchain
    last_block=blockchain[-1]
    # Hash the last block => to be able to compare it to the stored hash
    hashed_block=hash_block(last_block)
    proof = proof_of_work()
    # Mines should be rewarded, so let's create a reward
    # reward_transaction={
    #     "sender":'MINING',
    #     "recipient":owner,
    #     "amount":MINING_REWARD
    # }
    reward_transaction=OrderedDict([('sender',"MINING"),('recipient',owner),('amount',MINING_REWARD)])

    # Copy transation instaead of manipulating the original open_transactions
    # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
    copied_transactions=open_transactions[:]
    copied_transactions.append(reward_transaction)
    block={
        "previous_hash":hashed_block,
        'index':len(blockchain),
        'transactions':copied_transactions,
        'proof':proof
        }
    blockchain.append(block)
    save_data()
    return True

# User Input
def get_transaction_value():
    """ Return the input of the use (a nwe transaction amount) as a float"""
    # Get the user input, transform it from a string to a float and store it in user_input
    tx_recipient=input("Enter the sender of the transactions:")
    tx_amount= float(input("Your transaction amount please: "))
    return tx_recipient, tx_amount
    
def get_user_choice():
    """ Return the choice of user"""
    user_input=input("Your choice: ")
    return user_input

def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print("Outputting Block")
        print(block)
    else:
        print('-'*20)

def verify_chain():
    """ Verify the current blockchain and return True if it is valid"""
    for (index,block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash']!=hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block['transactions'][:-1],block['previous_hash'],block['proof']):
            return False
    return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input=True

while waiting_for_input:
    print("Please choose:")
    print("1: Add a new transaction value:")
    print("2: Mine block")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("h: Manipulate the chain")
    print('q: Quit')
    user_choice=get_user_choice()
    if user_choice=='1':
        tx_data = get_transaction_value()
        recipient,amount=tx_data
        if add_transaction(recipient,amount=amount):
            print('Added transaction')
        else:
            print('Transaction failed')    
        print(open_transactions)   
    elif user_choice=='2':
        if mine_block():
            open_transactions=[]
    elif user_choice=='3':
        print_blockchain_elements()    
    elif user_choice=='4':
        print(participant)
    elif user_choice=='5':
        if verify_transaction():
            print("All transaction are valid")
        else:
            print("There are invalid transaction")
    elif user_choice=='h':
        if len(blockchain)>=1:
            blockchain[0]={
                "previous_hash":'',
                'index':0,
                'transactions':[{"sender":"Chris","recipient":"Max","amount":100}]
            }           
    elif user_choice=='q':
        waiting_for_input=False
    else:
        print("Input was invalid, please pick a value from the list!")
    if  not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain!!!")
        break
    print('Balance of {}:{:6.2f}'.format('Hubert',get_balance('Hubert')))
else:
    print("User left!")


