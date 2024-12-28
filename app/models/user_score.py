import mongoengine as me


class UserScore(me.Document):
    user = me.ReferenceField("User")
    game = me.ReferenceField("Game")
    score = me.IntField(0)
    meta = {"collection": "score"}
