
from fastapi import File, UploadFile, Form, Depends, APIRouter
from app.db import get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import current_active_user

from app.modules.posts.controllers.createPostController import create_post_controller
from app.modules.posts.controllers.getPostsController import get_posts_controller
from app.modules.posts.controllers.deletePostsController import delete_post_controller

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
): return await create_post_controller(file=file, caption=caption, user=user, session=session)

@router.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await get_posts_controller(session=session, user=user)


@router.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user),):
    return await delete_post_controller(post_id=post_id, session=session, user=user)


    