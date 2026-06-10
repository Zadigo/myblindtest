from dataclasses import dataclass


@dataclass
class ChannelModel:
    channel_id: str

    def __repr__(self):
        return f'<ChannelModel [{self.channel_id}]>'

    def __hash__(self):
        return hash((self.channel_id,))
