from channels.testing import WebsocketCommunicator
from django.test import override_settings


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class TestPlayerConsumer(WSMixin):
    async def test_initial_connection(self):
        instance = WebsocketCommunicator(
            self.app,
            '/ws/single-player/1235abc/connect'
        )
        state, _ = await instance.connect()

        self.assertTrue(state)

        response = await instance.receive_json_from()
        self.assertEqual(response['action'], 'idle_connect')
        self.assertIn('player', response)

        player = response['player']
        self.assertIn('id', player)
        self.assertIn('name', player)

        # Update player
        # FIXME: The channel layer is timoutting here...
        # await instance.send_json_to({
        #     'action': 'update_player',
        #     'name': 'New Player Name'
        # })
        # response = await instance.receive_json_from()

        await instance.disconnect()
