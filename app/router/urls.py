"""
Project modules routers
"""
from app.views.influencers import Influencer

routers = [
    Influencer
]


def get_routers():
    """
    to get routers
    """
    return routers
