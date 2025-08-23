class GameGlobalStatisticsMixin:
    """Mixin class that adds internal statistics
    tracking for the game"""
    
    cached_answers = []
    timeline = [100]

    @property
    def last_score(self) -> dict[str, str] | None:
        try:
            return self.cached_answers[-1]
        except:
            return None

    async def team_answers(self, team_id: str):
        """Return the last answers by the given team"""
        return list(map(lambda x: x['team_id'] == team_id, self.cached_answers))[:5]

    async def register_answer(self, team_id: str, matched: str | None):
        """Registers the answers"""
        self.cached_answers.append({'team_id': team_id, 'matched': matched})

    async def update_timeline(self):
        """The timeline allows us to track the progression for
        correct and incorrect answers globally for all teams"""
        if self.is_started:
            matched = self.last_score['matched']
            value = self.timeline[-1]

            if matched == 'Title' or matched == 'Artist':
                value += 1
                self.timeline.append(value)
            elif matched is None:
                value -= 1
                self.timeline.append(value)
