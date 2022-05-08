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
validation_address-part1.txt
The length of 66 in the file is the transaction hash of the above address
The number of validation addresses is 705, and the number of available airdrops is 905444
