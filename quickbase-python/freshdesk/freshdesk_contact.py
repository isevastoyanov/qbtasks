import odin


class FreshdeskContact(odin.Resource):
    """"This class represents a FreshDesk contact which is retrieved from the Freshdesk REST API.
    See the possible attributes here: https://developers.freshdesk.com/api/#contacts"""

    name = odin.StringField()
    address = odin.StringField()
    email = odin.StringField()
    description = odin.StringField()
    twitter_id = odin.StringField()
