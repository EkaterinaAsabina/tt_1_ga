from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd

transport = AIOHTTPTransport(url="https://spacex-production.up.railway.app/")

client = Client(transport=transport, fetch_schema_from_transport=True)

def get_missions():
    query = gql(
        """
        query Data {
          launches {
            launch_id: id 
            mission_id
            mission_name
          }
        }
    """
    )
    result = client.execute(query)
    df = pd.json_normalize(result['launches'])

    return df

def get_launches():
    query = gql(
        """
        query Launches {
          launches {
            launch_id: id
            rocket {
              rocket {
                rocket_id: id
              }
            }
            links {
              wikipedia
              video_link
              reddit_recovery
              reddit_media
              reddit_launch
              presskit
              reddit_campaign
              mission_patch_small
              mission_patch
              article_link
            }
          }
        }
        """
    )

    result = client.execute(query)

    df = pd.json_normalize(result['launches'])
    df.columns = ['launch_id', 'rocket_id', 'wikipedia', 'video_link', 'reddit_recovery', 'reddit_media',
              'reddit_launch', 'presskit', 'reddit_campaign', 'mission_patch_small', 'mission_patch', 'article_link']

    return df

def get_rockets():
    query = gql(
        """
        query Rockets {
          rockets {
            rocket_id: id
            rocket_name: name
          }
        }
    """
    )
    result = client.execute(query)
    df = pd.json_normalize(result['rockets'])

    return df
