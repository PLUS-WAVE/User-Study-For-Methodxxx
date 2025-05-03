import json
import os
from collections import defaultdict
import re

def case_sort_key(case):
    nums = re.findall(r'\d+', case)
    return (re.sub(r'\d+', '', case), int(nums[0]) if nums else 0)

result_dir = 'user_results'
algorithms = ['Method1', 'Method2', 'Method3']

case_stats = defaultdict(lambda: {alg: {1: 0, 2: 0, 3: 0} for alg in algorithms})
total_stats = {alg: {1: 0, 2: 0, 3: 0} for alg in algorithms}

for fname in os.listdir(result_dir):
    if fname.endswith('.json'):
        with open(os.path.join(result_dir, fname), 'r') as f:
            data = json.load(f)
        for case, ranks in data.items():
            for alg in algorithms:
                rank = int(ranks[alg])
                case_stats[case][alg][rank] += 1
                total_stats[alg][rank] += 1

print('Per-case algorithm rank distribution (all users):')
for case in sorted(case_stats.keys(), key=case_sort_key):
    print(f'{case}:')
    for alg in algorithms:
        print(f'  {alg}: rank1={case_stats[case][alg][1]}, rank2={case_stats[case][alg][2]}, rank3={case_stats[case][alg][3]}')
    print()

print('Total algorithm rank distribution (all users):')
for alg in algorithms:
    print(f'{alg}: rank1={total_stats[alg][1]}, rank2={total_stats[alg][2]}, rank3={total_stats[alg][3]}')

user_count = len([fname for fname in os.listdir(result_dir) if fname.endswith('.json')])
print(f'Number of users: {user_count}')
