            if await executor.has_open_position():
                await asyncio.sleep(CHECK_INTERVAL_SECONDS)
                continue

            df = await feed.get_candles(limit=300)
            if df.empty:
                print("Data candle kosong, skip cek kali ini.")
                await asyncio.sleep(CHECK_INTERVAL_SECONDS)
                continue

            result = check_signal(df)

            if result["signal"] in ("BUY", "SELL"):
                lot = calculate_lot_size(equity_now, result["entry"], result["sl"])
                print(f"Sinyal {result['signal']} terdeteksi | entry={result['entry']} sl={result['sl']} tp={result['tp']} lot={lot}")
                await executor.place_order(result["signal"], lot, result["sl"], result["tp"])
            else:
                print(f"[{datetime.datetime.now()}] Belum ada sinyal.")

        except Exception as e:
            print(f"Error di loop utama: {e}")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
                                      
