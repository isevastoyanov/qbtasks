import odin

from freshdesk.freshdesk_contact import FreshdeskContact
from github.github_user import GithubUser


class GithubUserToFreshdeskContact(odin.Mapping):
    """This class is used for mapping between a GithubUser and a FreshdeskContact. If you want to add a new attribute
    that should be mapped all you should do is to add a new entry in the mappings tuple."""

    from_resource = GithubUser
    to_resource = FreshdeskContact

    # If you want a new attribute that should be mapped, add it here.
    mappings = (
        odin.define(from_field='name', to_field='name'),
        odin.define(from_field='bio', to_field='description'),
        odin.define(from_field='location', to_field='address'),
        odin.define(from_field='email', to_field='email'),
        odin.define(from_field='twitter_username', to_field='twitter_id'),
    )
