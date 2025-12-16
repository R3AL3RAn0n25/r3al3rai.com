#!/usr/bin/env python3
from crypto_knowledge_query_tool import CryptoKnowledgeQueryTool
import json

tool = CryptoKnowledgeQueryTool()

queries = [
    'bitcoin wallet private key',
    'base58 encoding address',
    'secp256k1 elliptic curve',
    'seed phrase bip32 derivation',
    'ripemd160 hash bitcoin',
    'ecdsa digital signature',
    'cryptocurrency key management'
]

print('\n' + '='*70)
print('FEEDING CRYPTOCURRENCY KNOWLEDGE TO R3AL3R AI')
print('='*70 + '\n')

all_knowledge = []

for query in queries:
    feed = tool.feed_to_r3aler(query)
    all_knowledge.append(feed)
    print(f'[FEED] Query: "{query}"')
    print(f'       Status: {feed["status"]}')
    print(f'       Results: {feed["total_results"]}')
    print(f'       Categories: {", ".join(feed["categories_found"])}')
    print()

print('='*70)
print('KNOWLEDGE FEED COMPLETE - R3AL3R AI UPDATED')
print('='*70)

stats = tool.get_stats()
print('\nKnowledge Base Status:')
for key, value in stats.items():
    print(f'  {key}: {value}')

print('\nTotal Knowledge Entries Fed: ' + str(sum([f['total_results'] for f in all_knowledge])))
print('\n' + '='*70)
