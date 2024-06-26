from .models.cameraManagement.cameraEntity import Base as CameraBase, engine as camera_engine
from .models.cameraManagement.criteriaEntity import Base as CriteriaBase, engine as criteria_engine
from .models.evaluationCriteriaManagement.emotionEntity import Base as EmotionBase, engine as emotion_engine
from .models.evaluationCriteriaManagement.uniformEntity import Base as UniformBase, engine as uniform_engine
from .models.userManagement.superAdminEntity import Base as SuperAdminBase, engine as super_admin_engine


def create_tables_on_startup():
    # Create the Camera table
    CameraBase.metadata.create_all(bind=camera_engine)
    # Create the Criteria table
    CriteriaBase.metadata.create_all(bind=criteria_engine)
    # Create the Emotion table
    EmotionBase.metadata.create_all(bind=emotion_engine)
    # Create the Uniform table
    UniformBase.metadata.create_all(bind=uniform_engine)
    # Create the SuperAdmin table
    SuperAdminBase.metadata.create_all(bind=super_admin_engine)
