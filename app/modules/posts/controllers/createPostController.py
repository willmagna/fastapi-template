from fastapi import HTTPException, File, UploadFile, Form, Depends
from app.db import Post, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession


from app.images import imagekit
import shutil, os,  tempfile
from app.users import current_active_user

async def create_post_controller(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):

    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        
        upload_result = imagekit.files.upload(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            tags=["backend-upload"]
        )


        if upload_result.url is not None:
            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url,
                file_type=upload_result.file_type,
                file_name=upload_result.name
            )

            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()