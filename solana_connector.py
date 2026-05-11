import requests
import os

class SolanaDAOConnector:
    def __init__(self):
        self.api_key = os.environ.get("HELIUS_API_KEY")
        # Используем Helius RPC для получения данных
        self.rpc_url = f"https://mainnet.helius-rpc.com/?api-key={self.api_key}" if self.api_key else None

    def fetch_treasury_balance(self, address):
        """
        Получает баланс SOL для указанного адреса.
        Если адрес - это Program ID (как GovER5...), баланс часто будет 0.
        """
        if not self.rpc_url:
            # Возвращаем 0, если API ключ не настроен (режим симуляции)
            return 0.0
            
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [address]
            }
            response = requests.post(self.rpc_url, json=payload, timeout=5)
            data = response.json()
            
            if "result" in data:
                # Баланс возвращается в Лампортах (1 SOL = 10^9 Lamports)
                return data["result"]["value"] / 10**9
            return 0.0
        except Exception as e:
            print(f"Ошибка RPC: {e}")
            return 0.0

    def fetch_token_assets(self, address):
        """
        Заготовка для получения SPL-токенов (USDC, JUP и т.д.)
        Будет реализована в Phase 2.
        """
        return []