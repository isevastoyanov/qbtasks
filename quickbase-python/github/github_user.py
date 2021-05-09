import odin as odin


class GithubUser(odin.Resource):
    """"This class represents a GitHub user which is retrieved from the GitHub REST API.
    See the possible attributes here: https://docs.github.com/en/rest/reference/users#get-a-user"""

    name = odin.StringField()
    location = odin.StringField()
    email = odin.StringField()
    bio = odin.StringField()
    twitter_username = odin.StringField()
