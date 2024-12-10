from bot.commands.base import BaseCommand
from bot.config import Config
from riotwatcher import TftWatcher


class TFTRankedCommand(BaseCommand):
    async def execute(self):
        pass
        # tft_watcher = TftWatcher(api_key=Config.RIOT_API_KEY)
        # rank_info = tft_watcher.league.by_summoner('asia', summoner['id'])
        # for entry in rank_info:
        #     if entry['queueType'] == 'RANKED_TFT':  # Xác định đúng chế độ xếp hạng TFT
        #         print(f"Rank: {entry['tier']} {entry['rank']}")
        #         print(f"LP: {entry['leaguePoints']}")
        #         print(f"Wins: {entry['wins']}, Losses: {entry['losses']}")
