# Airdrop-Killer
Fun games

## Strategy 1

The first round of screening  
1. whether the first From address is the contract address  
2. The transaction record is less than 20  
3. ETH interaction is 0 - "because the interaction in other chains, temporarily excluded and abandoned  

The second round of screening: (transaction records less than 20 into the second round of screening)  
1. Addresses that have interacted with the HOP smart contract  

The third round of screening  
1. Addresses with similar number of airdrops  

Fourth round of screening  
1.Manually track these filtered addresses  
2.Analyze the transaction records between them to determine if they are Sybil Attacker  

## Strategy 2

1.Check the internal transactions in the address to determine if the contract address for the bulk transfer was called  
2.Check if the "to" address in the contract log has the same number of airdrops  

# Document Description

The address files for group 1 and group 30 are stored in "address_hash_info-1.txt"  
The verified address is stored in "validation_address-part1.txt"  
The address in part2 is stored in the "address_hash_info-1.txt " file  
The verified address is stored in "validation_address-part2.txt"  

##validation_address-part1.txt    
The length of 66 in the file is the transaction hash of the above address   
Address number:705  
Total number of airdrops:905444

##validation_address-part2.txt  
Address number:2187   
Total number of airdrops:2089573.71


##internal_ts-1-32335.txt  
Use check_internam_ts.py to detect addresses that have used the Disperse.app type, internal transactions, from the 30,000 addresses


