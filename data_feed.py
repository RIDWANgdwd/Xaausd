"""
Modul buat konek ke MetaAPI dan ambil data candle XAUUSD.
Butuh: pip install metaapi-cloud-sdk pandas
"""
import pandas as pd
from metaapi_cloud_sdk import MetaApi

from config import METAAPI_TOKEN, METAAPI_ACCOUNT_ID, SYMBOL, TIMEFRAME


class DataFeed:
    def __init__(self):
        self.api = MetaApi(METAAPI_TOKEN)
        self.account = None

    async def connect(self):
        """Ambil handle akun MT5 dan pastikan sudah deployed/connected."""
        self.account = await self.api.metatrader_account_api.get_account(METAAPI_ACCOUNT_ID)

        if self.account.state != "DEPLOYED":
            await self.account.deploy()

        print("Menunggu koneksi ke broker...")
        await self.account.wait_connected()
        print("Akun MT5 terkoneksi ke MetaAPI.")

    async def get_candles(self, limit: int = 300) -> pd.DataFrame:
        """
