from songs.tests.utils import WSMixin
from blindtest.typings import GameActions
import time


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


class TestAdminConsumer(WSMixin):
    fixtures = ['songs']

    async def test_initial_connection(self):
        instance = await self.create_connection()

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], GameActions.IDLE_RESPONSE.value)
        self.assertIn('code', response)
        self.assertIn('connection_url', response)

        # Start game
        await instance.send_json_to({'action': GameActions.START_GAME.value})
        response = await instance.receive_json_from()
        self.assertEqual(response['action'], GameActions.GAME_STARTED.value)

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], GameActions.SONG_NEW.value)
        self.assertIn('song', response)

        song = response['song']
        self.assertIn('id', song)

        # Correct guess
        await instance.send_json_to({
            'action': GameActions.SUBMIT_GUESS.value,
            'team_or_player_id': '0',
            'title_match': True,
            'artist_match': False
        })
        response = await instance.receive_json_from()
        self.assertEqual(
            response['action'],
            GameActions.GUESS_CORRECT.value, response
        )

        self.assertIn('player_id', response)
        self.assertEqual(response['points'], 1)

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], GameActions.SONG_NEW.value)

        time.sleep(3)

        # Incorrect guess
        await instance.send_json_to({
            'action': GameActions.SUBMIT_GUESS.value,
            'team_or_player_id': '0',
            'title_match': False,
            'artist_match': False
        })
        response = await instance.receive_json_from()

        self.assertEqual(
            response['action'],
            GameActions.GUESS_INCORRECT.value
        )
        self.assertIn('song', response)

        await instance.disconnect()
