from cards import Card
from dataclasses import asdict, astuple, replace

# reminder of what the class looks like
#
# @dataclass
# class Card:
#     summary: str = None
#     owner: str = None
#     done: bool = None
#     id: int = field(default=None, compare=False)


def test_astuple():
    c = Card('do something', 'brian', True, 23)
    assert astuple(c) == ('do something', 'brian', True, 23)


def test_defaults():
    c = Card()
    assert astuple(c) == (None, None, None, None)


def test_asdict():
    c = Card('do something', 'brian', True, 23)
    assert asdict(c) == {'summary': 'do something',
                         'owner': 'brian',
                         'done': True,
                         'id': 23}


def test_from_dict():
    c = Card('do something', 'brian', True, 23)
    d = {'summary': 'do something',
         'owner': 'brian',
         'done': True,
         'id': 23}
    c_from_d = Card(**d)
    assert c_from_d == c
    assert c_from_d.id == c.id


def test_id_not_part_of_comparison():
    c1 = Card('foo', 'brian', False, id=1)
    c2 = Card('foo', 'brian', False, id=2)
    assert c1 == c2


def test_replace():
    c1 = Card('foo', 'brian', True)
    c2 = Card('foo', 'someone else', False)
    c3 = replace(c2, owner='brian', done=True)
    assert c1 == c3
