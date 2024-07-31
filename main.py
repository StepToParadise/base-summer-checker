import requests
import time
import random
import json

def read_wallets(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file.readlines()]

def send_get_request(wallet, endpoint):
    url = f'https://basehunt.xyz/api/{endpoint}?userAddress={wallet}&gameId=2'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

def log_result(wallet, currentScore, rank, num_referrals):
    with open('result.log', 'a') as file:
        file.write(f"Address: {wallet} | Score: {currentScore} | Rank: {rank} | Referrals: {num_referrals}\n")

def log_totals(total_referrals, total_score, rank_stats):
    with open('result.log', 'a') as file:
        file.write(f"\nTotal Referrals: {total_referrals}\n")
        file.write(f"Total Score: {total_score}\n")
        file.write(f"\nRank 0 - 10000: {rank_stats['0-10000']}\n")
        file.write(f"Rank 10000 - 30000: {rank_stats['10000-30000']}\n")
        file.write(f"Rank 30000 - 100000: {rank_stats['30000-100000']}\n")
        file.write(f"Rank 100000+: {rank_stats['100000+']}\n\n")

def main():
    wallets = read_wallets('wallets.txt')

    total_referrals = 0
    total_score = 0
    rank_stats = {
        '0-10000': 0,
        '10000-30000': 0,
        '30000-100000': 0,
        '100000+': 0
    }

    for wallet in wallets:
        state_result = send_get_request(wallet, 'profile/state')
        rank_result = send_get_request(wallet, 'leaderboard/rank')

        if state_result is not None and rank_result is not None:
            num_referrals = int(state_result.get("referralData", {}).get("numReferrals", "0"))
            currentScore = int(state_result.get("scoreData", {}).get("currentScore", "0"))
            rank = int(rank_result.get("rank", "0"))
            total_referrals += num_referrals
            total_score += currentScore

            # Update rank statistics
            if rank < 10000:
                rank_stats['0-10000'] += 1
            elif rank < 30000:
                rank_stats['10000-30000'] += 1
            elif rank < 100000:
                rank_stats['30000-100000'] += 1
            else:
                rank_stats['100000+'] += 1

            print(f"Address: {wallet} | Score: {currentScore} | Rank: {rank} | Referrals: {num_referrals}")
            log_result(wallet, currentScore, rank, num_referrals)

        # Случайная задержка от 1 до 10 секунд между запросами
        time.sleep(random.randint(1, 10))

    print(f"\nTotal Referrals: {total_referrals}")
    print(f"Total Score: {total_score}\n")
    print(f"Rank 0 - 10 000: {rank_stats['0-10000']}")
    print(f"Rank 10 000 - 30 000: {rank_stats['10000-30000']}")
    print(f"Rank 30 000 - 100 000: {rank_stats['30000-100000']}")
    print(f"Rank 100 000+: {rank_stats['100000+']}\n")

    log_totals(total_referrals, total_score, rank_stats)

if __name__ == "__main__":
    main()
