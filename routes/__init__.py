from fastapi import APIRouter
from resources.userController import router as userRouter
from resources.authController import router as userAuth
from resources.fbController import router as fbRouter
from resources.instaController import router as igRouter
from resources.linkedinController import router as liRouter
from resources.pinController import router as pinRouter
from resources.projectController import router as proRouter
from resources.smController import router as smRouter
from resources.redditController import router as rdRouter
from resources.ytController import router as ytRouter
from resources.orgController import router as orgRouter
from resources.brandController import router as brandRouter
from resources.productController import router as productRouter
from resources.keywordController import router as KeywordRouter


router = APIRouter()

router.include_router(userRouter, tags=['user'])
router.include_router(userAuth, tags=['Auth'])
router.include_router(orgRouter, tags=['Organisations'])
router.include_router(brandRouter, tags=['Brand'])
router.include_router(productRouter, tags=['Product'])
router.include_router(proRouter, tags=['Project'])
router.include_router(smRouter, tags=['Social_Media'])
router.include_router(fbRouter, tags=['Facebook'])
router.include_router(igRouter, tags=['Instagram'])
router.include_router(liRouter, tags=['Linkedin'])
router.include_router(pinRouter, tags=['Pinterest'])
router.include_router(rdRouter, tags=['Reddit'])
router.include_router(ytRouter, tags=['Youtube'])
router.include_router(KeywordRouter, tags=['SEO-Keywords'])

