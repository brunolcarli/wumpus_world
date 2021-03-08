import requests


class Query:
    @staticmethod
    def get_top_10():
        url = 'https://flagship-api.herokuapp.com/graphql/'
        payload = '''
        query{
            wumpusScores {
                playerName
                performance
                rounds
                gameDatetime
            }
        }
        '''
        response = requests.post(url, json={'query': payload})

        return response.json()


class Mutation:
    @staticmethod
    def register_score(name, performance, rounds):
        url = 'https://flagship-api.herokuapp.com/graphql/'
        payload = f'''
        mutation {{
            createWumpusScore( input: {{
                playerName: "{name}"
                performance: {performance}
                rounds: {rounds}
            }}) {{
                score {{
                    playerName
                    performance
                    rounds
                    gameDatetime
                }}
            }}
        }}
        '''
        response = requests.post(url, json={'query': payload})

        return response.json()
