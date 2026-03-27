from fastapi import HTTPException, Depends
from app.db import Post, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 

import uuid
from app.users import current_active_user


async def delete_post_controller(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user),):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        

        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not allowed to delete this post")

        await session.delete(post)
        await session.commit()

        return {"sucess": True, "message": "Post deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))