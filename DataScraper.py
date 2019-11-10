import requests
import json
import pandas as pd
import datetime

class DataScraper():

    def __init__(self,
                 game=None,
                 api_key=None):

        if game is None:
            raise ValueError('Specify a game!')

        self.game = game
        self.api_key = api_key

    def get_api_key(self,
                    filename='apikey.txt'):

        key = open(filename, 'r').read().rstrip('\n')

        return key

    def call_trn_api(self,
                     api_key=None,
                     platform=None,
                     name=None):

        if self.api_key is None:
            api_key = self.get_api_key()

        headers = {"TRN-Api-Key": api_key,
                   "Accept": 'application/vnd.api+json'}

        if self.game.lower() == 'fortnite':

            profile_req = requests.get('https://api.fortnitetracker.com/v1/profile/' + platform + '/' + name, headers=headers)

            if profile_req.status_code != 200:
                raise ValueError('Bad API call')

            profile_data = json.loads(profile_req.text)

            account_id = profile_data['accountId']

            match_req = requests.get('https://api.fortnitetracker.com/v1/profile/account/' + account_id + '/matches', headers=headers)

            match_data = json.loads(match_req.text)

            match_df = pd.DataFrame(data=match_data)

            match_df['datetime'] = match_df.apply(lambda row: datetime.datetime.strptime(row['dateCollected'], '%Y-%m-%dT%H:%M:%S.%f0'), axis=1)

            match_df['hour'] = match_df.apply(lambda row: row['datetime'].hour, axis=1)

            match_df['minute'] = match_df.apply(lambda row: row['datetime'].minute, axis=1)

            match_df['day_of_week'] = match_df.apply(lambda row: row['datetime'].strftime("%A"), axis=1)

        if self.game.lower() == 'apex':

            if platform == 'pc':
                platform = 'origin'

            profile_req = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/' + platform + '/' + name, headers=headers)

            profile_data = json.loads(profile_req.text)

            session_req = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/' + platform + '/' + name + '/sessions', headers=headers)

            session_data = json.loads(session_req.text)

        return match_df

    def aggregate_game_data(self, df):

        print(df.head)

if __name__ == '__main__':

    ds = DataScraper(game='fortnite')

    #ds.call_trn_api(game='apex', platform='pc', name='visstsm')

    ds.call_trn_api(platform='pc', name='drlupo')

