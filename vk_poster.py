from vkbottle import User
from pydantic.error_wrappers import ValidationError


class VkPoster():
    def __init__(self, vk_token, limit_count):
        self.user = User(vk_token)
        self.limit_count = limit_count

    async def get_owner_id(self, domain):
        vk_object = await self.user.api.utils.resolve_screen_name(domain)
        owner_id = vk_object.object_id
        if owner_id and vk_object.type.value != 'user':
            owner_id *= -1
        return owner_id

    async def get_posts(self, owner_id, last_post_id, error=False):
        count = self.limit_count
        if last_post_id == 0 or error:
            count = 1
        try:
            posts = await self.user.api.wall.get(
                owner_id=owner_id,
                count=count,
            )
        except ValidationError:
            if not error:
                return await self.get_posts(owner_id, last_post_id, True)
            return []
        return [(post.id, post.text) for post in posts.items if post.id > last_post_id and not post.copy_history][::-1]

    async def repost(self, owner_id, post_id, to_id):
        from_object = f'wall{owner_id}_{post_id}'
        await self.user.api.wall.repost(
            object=from_object,
            group_id=str(abs(to_id))
        )
