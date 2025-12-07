class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False
        return True

class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value
    
class All:
    def test(self, player):
        return True

class Not:
    def __init__(self, matcher):
        self._matcher = matcher

    def test(self, player):
        return not self._matcher.test(player)

class HasFewerThan:
    def __init__(self, amount, attribute):
        self._amount = amount
        self._attribute = attribute

    def test(self, player):
        return getattr(player, self._attribute) < self._amount

class Or:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        return any(matcher.test(player) for matcher in self._matchers)
    
class QueryBuilder:
    def __init__(self, matchers=None):
        self._matchers = matchers or []

    def build(self):
        if not self._matchers:
            return All()
        if len(self._matchers) == 1:
            return self._matchers[0]
        return And(*self._matchers)

    def plays_in(self, team):
        return QueryBuilder(self._matchers + [PlaysIn(team)])

    def has_at_least(self, amount, attribute):
        return QueryBuilder(self._matchers + [HasAtLeast(amount, attribute)])

    def has_fewer_than(self, amount, attribute):
        return QueryBuilder(self._matchers + [HasFewerThan(amount, attribute)])

    def one_of(self, *builders):
        matchers = [builder.build() for builder in builders]
        return QueryBuilder(self._matchers + [Or(*matchers)])
