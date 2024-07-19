# Initializing
genesis_block={
        "previous_hash":'',
        'index':0,
        'transactions':[]
}
blockchain=[genesis_block]
open_transactions=[]
owner='Hubert'


# Last blockchain value
def get_last_blockchain_value():
    """ Return the last value of the current blockchain"""
    if len(blockchain)<1:
        return None
    return blockchain[-1]

# Add Value to block chain
def add_transaction(recipient,sender=owner,amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain
    
    Arguments:
        :sender: The sender of the coins.
        :recipient: The reciient of the coins
        :amount: The amount of coins sent with the transition
    """
    transaction = {
        "sender":sender,
        "recipient":recipient,
        "amount":amount
    }
    open_transactions.append(transaction)
    
    

#Process open transactions
def mine_block():
    last_block=blockchain[-1]
    hashed_block=''
    for key in last_block:
        value=last_block[key]
        hashed_block=hashed_block+str(value)

    block={
        "previous_hash":hashed_block,
        'index':len(blockchain),
        'transactions':open_transactions
        }
    blockchain.append(block)

# User Input
def get_transaction_value():
    """ Return the input of the use (a nwe transaction amount) as a float"""
    tx_recipient=input("Enter the sender of the transactions:")
    tx_amount= float(input("Your transaction amount please: "))
    return tx_recipient, tx_amount
    
def get_user_choice():
    """ Return the choice of user"""
    user_input=input("Your choice: ")
    return user_input

def print_blockchain_elements():
    for block in blockchain:
        print("Outputting Block")
        print(block)
    else:
        print('-'*20)

def verify_chain():
    is_valid=True
    for block_index in range(len(blockchain)):
        if block_index==0:            
            continue
        elif blockchain[block_index][0]==blockchain[block_index-1]:
            print(block_index)
            is_valid=True
        else:
            is_valid=False
    return is_valid

    # block_index=0
    # is_valid=True
    # for block in blockchain:
    #     if block_index==0:
    #         block_index+=1
    #         continue
    #     elif block[0]==blockchain[block_index-1]:
    #         is_valid=True
    #     else:
    #         is_valid=False
    #         break 
    #     block_index+1

waiting_for_input=True

while waiting_for_input:
    print("Please choose:")
    print("1: Add a new transaction value:")
    print("2: Mine block")
    print("3: Output the blockchain blocks")
    print("h: Manipulate the chain")
    print('q: Quit')
    user_choice=get_user_choice()
    if user_choice=='1':
        tx_data = get_transaction_value()
        recipient,amount=tx_data
        add_transaction(recipient,amount=amount) 
        print(open_transactions)   
    elif user_choice=='2':
        mine_block()
    elif user_choice=='3':
        print_blockchain_elements()    
    elif user_choice=='h':
        if len(blockchain)>=1:
            blockchain[0]=[2]            
    elif user_choice=='q':
        waiting_for_input=False
    else:
        print("Input was invalid, please pick a value from the list!")
    # if  not verify_chain():
    #     print_blockchain_elements()
    #     print("Invalid blockchain")

    #     break
else:
    print("User left!")


