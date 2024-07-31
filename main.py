import requests
import time
import random
import json

def read_wallets(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file.readlines()]

def send_get_request(wallet):
    url = f'https://basehunt.xyz/api/profile/state?userAddress={wallet}&gameId=2'
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

def log_result(wallet, num_referrals, currentScore):
    with open('result.log', 'a') as file:
        file.write(f"Address: {wallet} | Referrals: {num_referrals} | Score: {currentScore}\n")

def log_totals(total_referrals, total_score):
    with open('result.log', 'a') as file:
        file.write(f"\nTotal Referrals: {total_referrals}\n")
        file.write(f"Total Score: {total_score}\n")

def main():
    wallets = read_wallets('wallets.txt')

    total_referrals = 0
    total_score = 0

    for wallet in wallets:
        result = send_get_request(wallet)
        if result is not None:
            num_referrals = int(result.get("referralData", {}).get("numReferrals", "0"))
            currentScore = int(result.get("scoreData", {}).get("currentScore", "0"))
            total_referrals += num_referrals
            total_score += currentScore
            print(f"Address: {wallet} | Referrals: {num_referrals} | Score: {currentScore}")
            log_result(wallet, num_referrals, currentScore)

        time.sleep(random.randint(1, 10))

    print(f"Total Referrals: {total_referrals}")
    print(f"Total Score: {total_score}")
    log_totals(total_referrals, total_score)

if __name__ == "__main__":
    main()