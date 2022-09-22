from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util.format import join_list
import operator
import requests
import statistics

class Jamendo_skill(MycroftSkill):

    def __init__(self):
        super(Jamendo_skill, self).__init__()

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()

    def on_settings_changed(self):
        self.client_id = self.settings.get('client_id', '6750d21f')

    def __get_generic__(self, url, payload):
        payload = {**payload, **{
            'client_id' : self.client_id,
            'format' : 'json'
            }}
        r = requests.get(url, params=payload)
        if r.status_code == 200:
            return r.json()
        else:
            self.speak_dialog(r.reason)
            return {}

    def __get_albums__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/albums', payload)

    def __get_artists__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/artists', payload)

    def __get_autocomplete__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/autocomplete', payload)

    def __get_feeds__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/feeds', payload)

    def __get_playlists__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/playlists', payload)

    def __get_radios__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/radios', payload)

    def __get_tracks__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/tracks', payload)

    def __get_users__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/users', payload)

    def __get_albums_file__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/albums/file', payload)

    def __get_albums_musicinfo__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/albums/musicinfo', payload)

    def __get_albums_tracks__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/albums/tracks', payload)

    def __get_artists_albums__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/artists/albums', payload)

    def __get_artists_locations__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/artists/locations', payload)

    def __get_artists_musicinfo__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/artists/musicinfo', payload)

    def __get_artists_tracks__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/artists/tracks', payload)

    def __get_playlists_file__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/playlists/file', payload)

    def __get_playlists_tracks__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/playlists/tracks', payload)

    def __get_radios_stream__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/radios/stream', payload)

    def __get_reviews_albums__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/reviews/albums', payload)

    def __get_reviews_tracks__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/reviews/tracks', payload)

    def __get_tracks_file__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/tracks/file', payload)

    def __get_tracks_similar__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/tracks/similar', payload)

    def __get_users_albums__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/users/albums', payload)

    def __get_users_artists__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/users/artists', payload)

    def __get_users_tracks__(self, payload):
        return self.__get_generic__('https://api.jamendo.com/v3.0/users/tracks', payload)

    @intent_handler('search_artists_albums.intent')
    def search_artists_albums(self, message):
        artist_name = message.data.get('artist_name')
        r = self.__get_artists_albums__({'limit': 'all', 'name': artist_name})
        albums = [ album.get('name') for artist in r.get('results') for album in artist.get('albums') ]
        if albums:
            self.speak_dialog('search_artists_albums', {
                'artist_name': artist_name,
                'list' : join_list(albums, 'and')
                })
        else:
            self.speak_dialog('no_artists_albums', {
                'artist_name': artist_name
                })

    @intent_handler('search_artists_best_albums.intent')
    def search_artists_best_albums(self, message):
        artist_name = message.data.get('artist_name')
        reviews = {}
        # forse sarebbe meglio contare i like?
        for album in [ album for artist in self.__get_artists_albums__({'limit': 'all', 'name': artist_name}).get('results') for album in artist.get('albums') ]:
            if album_reviews := self.__get_reviews_albums__({'album_id': album.get('id'), 'hasscore': 1, 'limit': 'all'}).get('results'):
                reviews[album.get('name')] = statistics.mean([ float(x.get('score')) for x in album_reviews ])

        bests = sorted(reviews.items(), key=operator.itemgetter(1), reverse=True)[:5]
        if bests:
            self.speak_dialog('search_artists_best_albums', {
                'artist_name': artist_name,
                'count': len(bests),
                'list' : join_list([ x[0] for x in bests ], 'and')
                })
        else:
            # in realtà sarebbe "nessun album con recensioni con punteggio"
            self.speak_dialog('no_artists_albums', {
                'artist_name': artist_name
                })

def create_skill():
    return Jamendo_skill()
